from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import re
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional

app = FastAPI(title="DISCO-ML Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GRAPHDB_URL = "http://localhost:7200"
DEFAULT_REPO = "disco-ml"

# --- Models ---

class ArgumentInput(BaseModel):
    author: str
    timestamp: str
    classification: str
    argument: str

class DecisionTicketInput(BaseModel):
    version_id: str
    filename: Optional[str] = None
    author: str
    timestamp: str
    status: str
    lifecycle_stage: Optional[str] = None
    lifecycle_artifact: Optional[str] = None
    schema_data: Dict[str, Any]

# --- Helper Functions ---

async def execute_sparql_query(repository_id: str, query: str):
    """Executes a SPARQL SELECT query."""
    url = f"{GRAPHDB_URL}/repositories/{repository_id}"
    headers = {
        "Accept": "application/sparql-results+json",
        "Content-Type": "application/sparql-query"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, content=query, headers=headers, timeout=10.0)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=f"GraphDB query failed: {response.text}")

async def execute_sparql_update(repository_id: str, update_query: str):
    """Executes a SPARQL UPDATE query."""
    url = f"{GRAPHDB_URL}/repositories/{repository_id}/statements"
    headers = {
        "Content-Type": "application/sparql-update"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, content=update_query, headers=headers, timeout=10.0)
        if response.status_code not in [200, 204]:
            raise HTTPException(status_code=response.status_code, detail=f"GraphDB update failed: {response.text}")
        return {"status": "ok"}

# --- Endpoints ---

@app.get("/")
async def root():
    return {"message": "DISCO-ML Backend API is running"}

@app.post("/test/upload-ticket")
async def upload_ticket(ticket: DecisionTicketInput):
    """
    Maps a formalized Decision Ticket to RDF and uploads it to GraphDB 
    according to the defined SHACL constraints.
    """
    # Determine the unique key for URIs (filename preferred, else version_id)
    ticket_key = ticket.filename or ticket.version_id
    if ticket_key.endswith(".json"):
        ticket_key = ticket_key[:-5]
        
    # Extract numeric part from issue_8726_v1 or pr_1234_v2
    parts = ticket_key.split("_")
    issue_number = parts[0] # Fallback
    for p in parts:
        if p.isdigit():
            issue_number = p
            break
    # Helper to normalize timestamps for xsd:dateTime
    def norm_dt(dt_str):
        return (dt_str or "").replace(" ", "T")
    
    # URI generation
    graph_uri = f"https://example.com/graphs/{ticket_key}"
    person_uri = f"https://example.com/persons/{urllib.parse.quote(ticket.author)}"
    issue_uri = f"https://example.com/issues/{issue_number}"
    desc_uri = f"https://example.com/descriptions/{ticket_key}"
    decision_uri = f"https://example.com/decisions/{ticket_key}"
    
    # Escape quotes in text content
    issue_text = (ticket.schema_data.get("Issue") or "").replace('"', '\\"')
    decision_text = (ticket.schema_data.get("Decision") or "").replace('"', '\\"')
    rationale_text = (ticket.schema_data.get("Rationale") or "").replace('"', '\\"')
    
    triples = f"""
    <{person_uri}> a schema:Person ;
        schema:name "{ticket.author}" .
    
    # Issue
    <{issue_uri}> a sioc_arg:Issue ;
        adr:hasAuthor <{person_uri}> ;
        adr:hasTimeStamp "{norm_dt(ticket.timestamp)}"^^xsd:dateTime ;
        adr:hasDescription <{desc_uri}> .
        
    <{desc_uri}> a adr:IssueDescription ;
        schema:text \"\"\"{issue_text}\"\"\" .
        
    # Decision
    <{decision_uri}> a schema:Decision ;
        adr:decides <{issue_uri}> ;
        adr:hasAuthor <{person_uri}> ;
        adr:hasTimeStamp "{norm_dt(ticket.timestamp)}"^^xsd:dateTime ;
        schema:name \"\"\"{decision_text}\"\"\" ;
        schema:text \"\"\"{rationale_text}\"\"\" .
    """
    
    # Arguments
    arguments = ticket.schema_data.get("Argument", [])
    if isinstance(arguments, list):
        for i, arg in enumerate(arguments):
            classification = arg.get("classification", "Neutral")
            
            # Skip if classification is NA
            if classification.upper() == "NA":
                continue
                
            arg_author_name = arg.get('author', 'unknown')
            arg_author_uri = f"https://example.com/persons/{urllib.parse.quote(arg_author_name)}"
            arg_uri = f"https://example.com/arguments/{ticket_key}_{i}"
            arg_text = arg.get("argument", "").replace('"', '\\"')
            
            # Map classification to UI-friendly type and SHACL stance property
            if classification.lower() == "pro":
                arg_type = "supports"
                stance_prop = "adr:agrees_with"
            elif classification.lower() == "con":
                arg_type = "opposes"
                stance_prop = "adr:disagrees_with"
            else:
                arg_type = "neutral"
                stance_prop = "adr:neutral_towards"
            
            triples += f"""
            <{arg_author_uri}> a schema:Person ;
                schema:name "{arg_author_name}" .
            <{arg_uri}> a sioc_arg:Argument ;
                schema:about <{decision_uri}> ;
                adr:hasAuthor <{arg_author_uri}> ;
                adr:hasTimeStamp "{norm_dt(arg.get('timestamp'))}"^^xsd:dateTime ;
                schema:text \"\"\"{arg_text}\"\"\" .
            """
            
            triples += f"<{decision_uri}> {stance_prop} <{arg_uri}> .\n"
            
    # Load the upload template
    template_path = Path(__file__).parent / "upload_template.ru"
    if not template_path.exists():
        raise HTTPException(status_code=500, detail="Upload template not found")
        
    try:
        with open(template_path, "r") as f:
            upload_template = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading upload template: {str(e)}")
        
    clear_query = f"CLEAR GRAPH <{graph_uri}>"
    await execute_sparql_update(DEFAULT_REPO, clear_query)
    
    # Format the update query using the template
    update_query = upload_template.replace("{{GRAPH_URI}}", graph_uri).replace("{{TRIPLES}}", triples)
    
    return await execute_sparql_update(DEFAULT_REPO, update_query)

@app.get("/health/graphdb")
async def check_graphdb_health():
    # ... existing code ...
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{GRAPHDB_URL}/protocol", timeout=5.0)
            if response.status_code == 200:
                return {"status": "ok", "message": "GraphDB is accessible", "version": response.text}
            else:
                response_root = await client.get(f"{GRAPHDB_URL}/", timeout=5.0)
                if response_root.status_code == 200:
                    return {"status": "ok", "message": "GraphDB is accessible"}
                return {"status": "error", "message": f"GraphDB returned status code {response.status_code}"}
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Could not connect to GraphDB: {str(e)}")

@app.get("/repositories")
async def get_repositories():
    # ... existing code ...
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Accept": "application/json"}
            response = await client.get(f"{GRAPHDB_URL}/repositories", headers=headers, timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                results = []
                if "results" in data and "bindings" in data["results"]:
                    for binding in data["results"]["bindings"]:
                        results.append({
                            "id": binding.get("id", {}).get("value"),
                            "title": binding.get("title", {}).get("value"),
                            "uri": binding.get("uri", {}).get("value")
                        })
                return {"status": "ok", "repositories": results}
            else:
                raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch repositories: {response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Could not connect to GraphDB: {str(e)}")

@app.get("/data/tickets")
async def get_tickets_data():
    # ... existing code ...
    template_path = Path(__file__).parent / "data_acquisition_template.ru"
    if not template_path.exists():
        raise HTTPException(status_code=500, detail="SPARQL template not found")
    try:
        with open(template_path, "r") as f:
            query_template = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading template: {str(e)}")
    query = query_template
    query = re.sub(r"FROM\s+<[^>]+>", "", query, flags=re.IGNORECASE)
    base_uri = "https://example.com/graphs/"
    query = re.sub(r"WHERE\s*\{", f"WHERE {{\n    GRAPH ?g {{\n        FILTER(STRSTARTS(STR(?g), \"{base_uri}\"))", query, flags=re.IGNORECASE)
    query = query.rstrip()
    if query.endswith("}"):
        query = query[:-1] + "\n    }\n}"
    results = await execute_sparql_query(DEFAULT_REPO, query)
    
    # Process results into the frontend-expected format
    tickets_map = {}
    if "results" in results and "bindings" in results["results"]:
        for binding in results["results"]["bindings"]:
            graph_uri = binding.get("g", {}).get("value")
            issue_uri = binding.get("issue", {}).get("value")
            if not graph_uri:
                continue
                
            ticket_id = issue_uri.split("/")[-1]
            
            if ticket_id not in tickets_map:
                tickets_map[ticket_id] = {
                    "id": ticket_id,
                    "title": binding.get("issueLabel", {}).get("value"),
                    "status": binding.get("status", {}).get("value") or "open",
                    "bucket": binding.get("phase", {}).get("value") or "Miscellaneous",
                    "owner": {
                        "id": binding.get("issueAuthor", {}).get("value").split("/")[-1],
                        "name": binding.get("issueAuthorName", {}).get("value")
                    },
                    "createdAt": binding.get("issueTime", {}).get("value"),
                    "updatedAt": "",
                    "tags": [],
                    "currentVersionIndex": 0,
                    "versions": []
                }
            
            # Version processing
            version_id = graph_uri.split("/")[-1]
            version = next((v for v in tickets_map[ticket_id]["versions"] if v["versionId"] == version_id), None)
            
            if not version:
                version = {
                    "versionId": version_id,
                    "decision": binding.get("decisionLabel", {}).get("value"),
                    "rationale": binding.get("rationale", {}).get("value"),
                    "context": binding.get("issueLabel", {}).get("value"),
                    "timestamp": binding.get("issueTime", {}).get("value"),
                    "arguments": []
                }
                tickets_map[ticket_id]["versions"].append(version)
                
            # Argument processing
            arg_uri = binding.get("arg", {}).get("value")
            if arg_uri:
                arg_id = arg_uri.split("/")[-1]
                if not any(a["id"] == arg_id for a in version["arguments"]):
                    version["arguments"].append({
                        "id": arg_id,
                        "content": binding.get("comment", {}).get("value"),
                        "type": binding.get("stance", {}).get("value") or "neutral",
                        "author": binding.get("argAuthorName", {}).get("value"),
                        "createdAt": binding.get("argTime", {}).get("value")
                    })
                    
    # Final assembly: Sort versions and keep ONLY the latest one
    processed_results = []
    for ticket in tickets_map.values():
        # Natural sort for versions (e.g., v2 comes before v10)
        def get_v_num(v_obj):
            v_id = v_obj["versionId"]
            match = re.search(r"_v(\d+)", v_id)
            return int(match.group(1)) if match else 0
            
        ticket["versions"].sort(key=get_v_num)
        
        # Set top-level decision/rationale from the latest version
        latest = ticket["versions"][-1]
        
        # Only provide the most recent version as requested
        ticket["versions"] = [latest]
        ticket["decision"] = latest["decision"]
        ticket["rationale"] = latest["rationale"]
        ticket["description"] = latest["context"]
        ticket["author"] = latest.get("author", ticket["owner"]["name"])
        ticket["arguments"] = latest["arguments"]
        ticket["currentVersionIndex"] = 0
        
        processed_results.append(ticket)
            
    return {
        "status": "ok", 
        "count": len(processed_results),
        "data": processed_results
    }

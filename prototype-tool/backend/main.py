from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import re
import urllib.parse
from pathlib import Path
from typing import List, Dict, Any, Optional

from models import DecisionTicketInput, ArgumentInput
from sparql_builder import build_upload_query

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

# --- Helper Functions ---

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
    template_path = Path(__file__).parent / "upload_template.ru"
    
    try:
        graph_uri, update_query = build_upload_query(ticket, template_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building SPARQL query: {str(e)}")
        
    clear_query = f"CLEAR GRAPH <{graph_uri}>"
    await execute_sparql_update(DEFAULT_REPO, clear_query)
    
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
            # print(f"DEBUG: Binding keys: {binding.keys()}") # Commented out but ready if needed
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
                    "versions": [],
                    "cost": "",
                    "risk": ""
                }
            
            # Version processing
            version_id = graph_uri.split("/")[-1]
            version = next((v for v in tickets_map[ticket_id]["versions"] if v["versionId"] == version_id), None)
            
            if not version:
                version = {
                    "versionId": version_id,
                    "decision": binding.get("decisionLabel", {}).get("value") or "",
                    "rationale": binding.get("rationaleText", {}).get("value") or "",
                    "cost": binding.get("costText", {}).get("value") or "",
                    "risk": binding.get("riskText", {}).get("value") or "",
                    "context": binding.get("issueBody", {}).get("value") or binding.get("issueLabel", {}).get("value"),
                    "author": binding.get("issueAuthorName", {}).get("value") or "unknown",
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
        
        # Set top-level fields from the latest version
        latest = ticket["versions"][-1]
        
        ticket["decision"] = latest.get("decision", "")
        ticket["rationale"] = latest.get("rationale", "")
        ticket["cost"] = latest.get("cost", "")
        ticket["risk"] = latest.get("risk", "")
        
        ticket["description"] = latest.get("context", "")
        ticket["author"] = latest.get("author", ticket["owner"]["name"])
        ticket["arguments"] = latest["arguments"]
        ticket["currentVersionIndex"] = len(ticket["versions"]) - 1
        
        processed_results.append(ticket)
            
    return {
        "status": "ok", 
        "count": len(processed_results),
        "data": processed_results
    }

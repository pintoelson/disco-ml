import urllib.parse
from pathlib import Path
from models import DecisionTicketInput

def build_upload_query(ticket: DecisionTicketInput, template_path: Path) -> tuple[str, str]:
    """
    Constructs the SPARQL update query and returns (graph_uri, update_query).
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
    rationale_uri = f"https://example.com/rationales/{ticket_key}"
    cost_uri = f"https://example.com/costs/{ticket_key}"
    risk_uri = f"https://example.com/risks/{ticket_key}"
    
    # Escape quotes in text content
    issue_obj = ticket.schema_data.get("Issue")
    if isinstance(issue_obj, dict):
        # If it's the new structured Issue object, separate title and body
        issue_title = (issue_obj.get('title', '')).replace('"', '\\"')
        issue_body = (issue_obj.get('body', '')).replace('"', '\\"')
    else:
        issue_title = str(issue_obj or "").split("\n")[0]
        issue_body = str(issue_obj or "")
        
    issue_title = issue_title.replace('"', '\\"')
    issue_body = issue_body.replace('"', '\\"')
    decision_text = (ticket.schema_data.get("Decision") or "").replace('"', '\\"')
    
    rationale_text = (ticket.schema_data.get("Rationale") or "").replace('"', '\\"')
    cost_text = (ticket.schema_data.get("Cost") or "").replace('"', '\\"')
    risk_text = (ticket.schema_data.get("Risk") or "").replace('"', '\\"')
    
    triples = f"""
    <{person_uri}> a schema:Person ;
        schema:name "{ticket.author}" .
    
    # Issue
    <{issue_uri}> a sioc_arg:Issue ;
        schema:name "{issue_title}" ;
        adr:hasAuthor <{person_uri}> ;
        adr:hasTimeStamp "{norm_dt(ticket.timestamp)}"^^xsd:dateTime ;
        adr:hasDescription <{desc_uri}> .
        
    <{desc_uri}> a adr:IssueDescription ;
        schema:text \"\"\"{issue_body}\"\"\" .
        
    # Decision
    <{decision_uri}> a schema:Decision ;
        adr:decides <{issue_uri}> ;
        adr:hasAuthor <{person_uri}> ;
        adr:hasTimeStamp "{norm_dt(ticket.timestamp)}"^^xsd:dateTime ;
        schema:text \"\"\"{decision_text}\"\"\" ;
        schema:name \"\"\"{decision_text[:100]}\"\"\" .
    """

    if rationale_text:
        triples += f"""
    <{rationale_uri}> a adr:Rationale ;
        schema:text \"\"\"{rationale_text}\"\"\" .
    <{decision_uri}> adr:hasRationale <{rationale_uri}> .
    """

    if cost_text:
        triples += f"""
    <{cost_uri}> a adr:Cost ;
        schema:text \"\"\"{cost_text}\"\"\" .
    <{decision_uri}> adr:hasCost <{cost_uri}> .
    """

    if risk_text:
        triples += f"""
    <{risk_uri}> a adr:Risk ;
        schema:text \"\"\"{risk_text}\"\"\" .
    <{decision_uri}> adr:hasRisk <{risk_uri}> .
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
    if not template_path.exists():
        raise FileNotFoundError(f"Upload template not found at {template_path}")
        
    with open(template_path, "r") as f:
        upload_template = f.read()
        
    # Format the update query using the template
    update_query = upload_template.replace("{{GRAPH_URI}}", graph_uri).replace("{{TRIPLES}}", triples)
    
    return graph_uri, update_query

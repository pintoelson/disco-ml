import urllib.parse
from pathlib import Path
from models import IngestionPayload

def build_upload_query(ticket: IngestionPayload, template_path: Path) -> tuple[str, str]:
    """
    Constructs the SPARQL update query and returns (graph_uri, update_query).
    """
    # Determine the unique key for URIs from nested decision_ticket
    ticket_key = ticket.decision_ticket.filename or "unknown_ticket"
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
    
    # Issue handling
    issue_obj = ticket.decision_ticket.Issue
    if isinstance(issue_obj, str):
        # Legacy flat string
        issue_title = issue_obj.split("\n")[0].replace('"', '\\"')
        issue_body = issue_obj.replace('"', '\\"')
        author_name = "unknown"
        issue_ts = ticket.decision_ticket.timestamp
    else:
        # Structured IssueInput
        issue_title = issue_obj.title.replace('"', '\\"')
        issue_body = issue_obj.body.replace('"', '\\"')
        author_name = issue_obj.author
        issue_ts = issue_obj.timestamp

    # URI generation
    graph_uri = f"https://example.com/graphs/{ticket_key}"
    person_uri = f"https://example.com/persons/{urllib.parse.quote(author_name)}"
    issue_uri = f"https://example.com/issues/{issue_number}"
    desc_uri = f"https://example.com/descriptions/{ticket_key}"
    decision_uri = f"https://example.com/decisions/{ticket_key}"
    rationale_uri = f"https://example.com/rationales/{ticket_key}"
    cost_uri = f"https://example.com/costs/{ticket_key}"
    risk_uri = f"https://example.com/risks/{ticket_key}"
    
    # Helper to safely escape quotes in text content
    def escape(val):
        return str(val or "").replace('"', '\\"')
        
    decision_obj = ticket.decision_ticket.Decision
    decision_text = None
    decision_name = "Pending Decision"
    decision_authors = []
    
    if decision_obj:
        decision_text = escape(decision_obj.decision)
        if decision_text:
            decision_name = decision_text[:100]
        decision_authors = decision_obj.authors or []
    
    rationale_text = escape(ticket.decision_ticket.Rationale)
    cost_text = escape(ticket.decision_ticket.Cost)
    risk_text = escape(ticket.decision_ticket.Risk)
    
    triples = f"""
    <{person_uri}> a schema:Person ;
        schema:name "{escape(author_name)}" .
    
    # Issue
    <{issue_uri}> a sioc_arg:Issue ;
        schema:name "{issue_title}" ;
        adr:hasAuthor <{person_uri}> ;
        adr:hasTimeStamp "{norm_dt(issue_ts)}"^^xsd:dateTime ;
        adr:hasDescription <{desc_uri}> .
        
    <{desc_uri}> a adr:IssueDescription ;
        schema:text \"\"\"{issue_body}\"\"\" .
        
    # Decision
    <{decision_uri}> a schema:Decision ;
        adr:decides <{issue_uri}> ;
        adr:hasTimeStamp "{norm_dt(ticket.decision_ticket.timestamp)}"^^xsd:dateTime ;
        schema:name "{decision_name}" .
    """

    # Add Decision Authors
    if not decision_authors:
        # Fallback to issue author if no specific decision authors identified
        triples += f"<{decision_uri}> adr:hasAuthor <{person_uri}> .\n"
    else:
        for auth in decision_authors:
            d_auth_uri = f"https://example.com/persons/{urllib.parse.quote(auth)}"
            triples += f"""
    <{decision_uri}> adr:hasAuthor <{d_auth_uri}> .
    <{d_auth_uri}> a schema:Person ;
        schema:name "{escape(auth)}" .
    """

    if decision_text:
        triples += f"""
    <{decision_uri}> schema:text \"\"\"{decision_text}\"\"\" .
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
    arguments = ticket.decision_ticket.Argument or []
    for i, arg in enumerate(arguments):
        classification = arg.classification or "Neutral"
        
        arg_author_name = arg.author
        arg_author_uri = f"https://example.com/persons/{urllib.parse.quote(arg_author_name)}"
        arg_uri = f"https://example.com/arguments/{ticket_key}_{i}"
        arg_text = escape(arg.argument)
        
        # Map classification to SHACL stance property
        if classification.lower() == "pro":
            stance_prop = "adr:agrees_with"
        elif classification.lower() == "con":
            stance_prop = "adr:disagrees_with"
        else:
            stance_prop = "adr:neutral_towards"
        
        triples += f"""
        <{arg_author_uri}> a schema:Person ;
            schema:name "{escape(arg_author_name)}" .
        <{arg_uri}> a sioc_arg:Argument ;
            adr:hasAuthor <{arg_author_uri}> ;
            adr:hasTimeStamp "{norm_dt(arg.timestamp)}"^^xsd:dateTime ;
            schema:text \"\"\"{arg_text}\"\"\" .
        """
        
        triples += f"<{decision_uri}> {stance_prop} <{arg_uri}> .\n"
            
    activity_uri = None
    activity_uri = None
    if ticket.ml_elements:
        if ticket.ml_elements.lifecycle_stage:
            stage_class = ticket.ml_elements.lifecycle_stage.value
            activity_uri = f"https://example.com/activities/{ticket_key}"
            triples += f"""
            # Lifecycle Activity
            <{activity_uri}> a mops:{stage_class} ;
                prov:wasAssociatedWith <{person_uri}> .
                
            <{issue_uri}> prov:wasGeneratedBy <{activity_uri}> .
            <{decision_uri}> prov:wasGeneratedBy <{activity_uri}> .
            """

        if ticket.ml_elements.author_roles:
            for author_name, role in ticket.ml_elements.author_roles.items():
                author_uri_role = f"https://example.com/persons/{urllib.parse.quote(author_name)}"
                role_class = role.value
                triples += f"""
            <{author_uri_role}> bridge:hasRole mops:{role_class} .
            """

        # Main Assets
        for asset in (ticket.ml_elements.main_assets or []):
            asset_name = escape(asset.name)
            asset_uri = f"https://example.com/assets/{urllib.parse.quote(asset_name)}"
            asset_type = asset.asset_type.value
            
            location_triple = ""
            location = asset.location
            if location and str(location).lower() != "null":
                safe_location = escape(location)
                location_triple = f';\n            mops:hasLocation "{safe_location}"'
                
            triples += f"""
            # Main Asset
            <{asset_uri}> a mops:{asset_type} ;
                schema:name "{asset_name}" {location_triple} .
            """
            if activity_uri:
                 triples += f"<{asset_uri}> prov:wasGeneratedBy <{activity_uri}> .\n"

        # Mentioned Assets
        for asset in (ticket.ml_elements.mentioned_assets or []):
            asset_name = escape(asset.name)
            asset_uri = f"https://example.com/assets/{urllib.parse.quote(asset_name)}"
            asset_type = asset.asset_type.value
            triples += f"""
            # Mentioned Asset
            <{asset_uri}> a mops:{asset_type} ;
                schema:name "{asset_name}" .
            """

    # Load the upload template
    if not template_path.exists():
        raise FileNotFoundError(f"Upload template not found at {template_path}")
        
    with open(template_path, "r") as f:
        upload_template = f.read()
        
    # Format the update query using the template
    update_query = upload_template.replace("{{GRAPH_URI}}", graph_uri).replace("{{TRIPLES}}", triples)
    
    return graph_uri, update_query

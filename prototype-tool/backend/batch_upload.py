import os
import json
import requests
import re
from pathlib import Path
from collections import defaultdict

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000/api/v1/tickets/upload")
FORMALIZED_DATA_DIR = Path("../../schema_extraction/pipeline/data/bridged/Project-MONAI_MONAI")

STATE_FILE = Path(".ingested_state.json")

# Legacy Mappings moved from Backend to Ingestion Script
STAGE_MAP = {
    "ML Project Initiation": "Business_and_Data_Understanding",
    "Data Preparation": "Data_Engineering",
    "Modeling Development": "Model_Engineering",
    "Model Evaluation": "Model_Evaluation",
    "Model Deployment": "ModelDeployment",
    "Monitoring & Maintenance": "ModelMonitoring"
}

ASSET_MAP = {
    "Dataset": "Dataset",
    "Model": "MLAsset",
    "Code": "MLAsset",
    "Feature Set": "FeatureSet",
    "Provenance": "ProvenanceRecord",
    "NA": "MLAsset"
}

ROLE_MAP = {
    "Data Engineer": "DataEngineer",
    "ML Engineer": "MLEngineer",
    "Data Scientist": "DataScientist",
    "Software Engineer": "SoftwareEngineer",
    "IT Operations Team": "ITOpsTeam",
    "Project Team": "ProjectTeam"
}

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_state(state_set):
    with open(STATE_FILE, "w") as f:
        json.dump(list(state_set), f)

def normalize_payload(payload):
    """Maps legacy human-readable strings to strict ontology class names."""
    # Normalize Stage
    if "lifecycle_stage" in payload and payload["lifecycle_stage"] in STAGE_MAP:
        payload["lifecycle_stage"] = STAGE_MAP[payload["lifecycle_stage"]]
    
    # Normalize Roles
    if "author_roles" in payload and payload["author_roles"]:
        new_roles = {}
        for author, role in payload["author_roles"].items():
            new_roles[author] = ROLE_MAP.get(role, "Role")
        payload["author_roles"] = new_roles
        
    # Normalize Assets
    if "main_assets" in payload and payload["main_assets"]:
        for asset in payload["main_assets"]:
            if "asset_type" in asset:
                asset["asset_type"] = ASSET_MAP.get(asset["asset_type"], "MLAsset")
                
    return payload

def batch_upload_versioned(ticket_limit=10):
    if not FORMALIZED_DATA_DIR.exists():
        print(f"Directory not found: {FORMALIZED_DATA_DIR}")
        return

    json_files = list(FORMALIZED_DATA_DIR.glob("*.json"))
    
    # Group by ticket base name (e.g. pr_8708)
    ticket_groups = defaultdict(list)
    for f in json_files:
        # Match pattern like pr_1234_v1 or issue_1234_v1
        match = re.match(r"(pr|issue)_\d+", f.name)
        if match:
            base = match.group(0)
            ticket_groups[base].append(f)
        else:
            ticket_groups[f.name].append(f)

    # Sort tickets by version count (ascending)
    sorted_tickets = sorted(ticket_groups.items(), key=lambda x: len(x[1]), reverse=False)
    
    print(f"Found {len(ticket_groups)} unique tickets.")
    print(f"Prioritizing tickets with fewest versions...")

    state = load_state()
    total_files_uploaded = 0
    
    for i, (ticket_id, files) in enumerate(sorted_tickets):
        if i >= ticket_limit:
            break
            
        print(f"\n[{i+1}/{ticket_limit}] Ticket: {ticket_id} ({len(files)} versions)")
        
        # Sort files by version number to ensure correct sequence
        files.sort(key=lambda x: x.name)
        
        for file_path in files:
            if file_path.name in state:
                print(f"  Skipping {file_path.name} (already uploaded)")
                continue

            print(f"  Uploading {file_path.name}...", end=" ", flush=True)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                
                if "filename" not in payload:
                    payload["filename"] = file_path.name

                # Strict Ontology Normalization
                payload = normalize_payload(payload)

                response = requests.post(BACKEND_URL, json=payload)
                
                if response.status_code == 200:
                    print("OK")
                    total_files_uploaded += 1
                    state.add(file_path.name)
                    save_state(state)
                else:
                    print(f"FAILED ({response.status_code})")
                    print(f"    Detail: {response.text}")
            except Exception as e:
                print(f"ERROR: {str(e)}")

    print(f"\nBatch upload complete.")
    print(f"Tickets processed: {min(ticket_limit, len(ticket_groups))}")
    print(f"Total files (versions) uploaded: {total_files_uploaded}")

if __name__ == "__main__":
    batch_upload_versioned(10)

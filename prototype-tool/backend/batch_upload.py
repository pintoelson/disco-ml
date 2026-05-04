import os
import json
import requests
import re
from pathlib import Path
from collections import defaultdict

BACKEND_URL = "http://localhost:8000/test/upload-ticket"
FORMALIZED_DATA_DIR = Path("../../schema_extraction/pipeline/data/formalized/Project-MONAI_MONAI")

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

    success_count = 0
    total_files_uploaded = 0
    
    for i, (ticket_id, files) in enumerate(sorted_tickets):
        if i >= ticket_limit:
            break
            
        print(f"\n[{i+1}/{ticket_limit}] Ticket: {ticket_id} ({len(files)} versions)")
        
        # Sort files by version number to ensure correct sequence
        files.sort(key=lambda x: x.name)
        
        for file_path in files:
            print(f"  Uploading {file_path.name}...", end=" ", flush=True)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                
                if "filename" not in payload:
                    payload["filename"] = file_path.name

                response = requests.post(BACKEND_URL, json=payload)
                
                if response.status_code == 200:
                    print("OK")
                    total_files_uploaded += 1
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

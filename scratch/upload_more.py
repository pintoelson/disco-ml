import json
import requests
import os
from pathlib import Path

BACKEND_URL = "http://localhost:8000/test/upload-ticket"
DATA_DIR = Path("schema_extraction/pipeline/data/formalized/Project-MONAI_MONAI")
ALREADY_UPLOADED = ["pr_8672_v1.json", "issue_8726_v1.json"]

def upload_more(limit=5):
    json_files = sorted(list(DATA_DIR.glob("*.json")))
    count = 0
    for f in json_files:
        if f.name in ALREADY_UPLOADED:
            continue
        if count >= limit:
            break
            
        print(f"Uploading {f.name}...")
        with open(f, "r", encoding="utf-8") as file:
            payload = json.load(file)
            
        if "filename" not in payload:
            payload["filename"] = f.name
            
        try:
            r = requests.post(BACKEND_URL, json=payload)
            if r.status_code == 200:
                print(f"  OK")
                count += 1
            else:
                print(f"  FAILED ({r.status_code}): {r.text}")
        except Exception as e:
            print(f"  ERROR: {e}")

if __name__ == "__main__":
    upload_more(5)

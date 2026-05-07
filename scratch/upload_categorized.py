import os
import json
import requests
import re
from pathlib import Path
from collections import defaultdict

BACKEND_URL = "http://localhost:8000/test/upload-ticket"
DATA_DIR = Path("schema_extraction/pipeline/data/formalized/Project-MONAI_MONAI")

def analyze_and_upload():
    if not DATA_DIR.exists():
        print(f"Directory not found: {DATA_DIR}")
        return

    json_files = list(DATA_DIR.glob("*.json"))
    ticket_groups = defaultdict(list)
    
    for f in json_files:
        match = re.match(r"((pr|issue)_\d+)", f.name)
        if match:
            base = match.group(1)
            ticket_groups[base].append(f)
            
    # Categories
    cat1 = [] # 1 version
    cat2 = [] # 2-5 versions
    cat3 = [] # 5+ versions
    
    for base, files in ticket_groups.items():
        files.sort(key=lambda x: x.name)
        count = len(files)
        if count == 1:
            cat1.append((base, files))
        elif 2 <= count <= 5:
            cat2.append((base, files))
        elif count > 5:
            cat3.append((base, files))
            
    print(f"Stats: Cat1 (1): {len(cat1)}, Cat2 (2-5): {len(cat2)}, Cat3 (5+): {len(cat3)}")
    
    to_upload = cat1[:2] + cat2[:2] + cat3[:2]
    
    total_uploaded = 0
    for base, files in to_upload:
        print(f"\nUploading {base} ({len(files)} versions):")
        for f in files:
            print(f"  {f.name}...", end=" ", flush=True)
            with open(f, "r", encoding="utf-8") as file:
                payload = json.load(file)
            if "filename" not in payload:
                payload["filename"] = f.name
            try:
                r = requests.post(BACKEND_URL, json=payload)
                if r.status_code == 200:
                    print("OK")
                    total_uploaded += 1
                else:
                    print(f"FAILED ({r.status_code})")
            except Exception as e:
                print(f"ERROR: {e}")
                
    print(f"\nDone! Total files uploaded: {total_uploaded}")

if __name__ == "__main__":
    analyze_and_upload()

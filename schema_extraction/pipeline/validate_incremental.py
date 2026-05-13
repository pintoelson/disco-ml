import json
import os
from pathlib import Path
import re
from typing import Dict, Any, List

def get_v_num(filename: str) -> int:
    match = re.search(r"_v(\d+)\.json$", filename)
    return int(match.group(1)) if match else 0

def diff_versions(v_prev: Dict[str, Any], v_curr: Dict[str, Any]):
    prev_data = v_prev.get("schema_data", {})
    curr_data = v_curr.get("schema_data", {})
    
    changes = []
    
    # Check simple fields
    fields = ["Decision", "Rationale", "Description", "Cost", "Risk"]
    for field in fields:
        p_val = prev_data.get(field)
        c_val = curr_data.get(field)
        if p_val != c_val:
            if not p_val and c_val:
                changes.append(f"[NEW {field}] {c_val}")
            elif p_val and c_val:
                changes.append(f"[UPDATED {field}] From: \"{p_val[:50]}...\" To: \"{c_val[:50]}...\"")
                
    # Check Arguments (incremental list)
    prev_args = prev_data.get("Argument", [])
    curr_args = curr_data.get("Argument", [])
    
    # Since it's incremental, we just check for new ones at the end
    if len(curr_args) > len(prev_args):
        new_args = curr_args[len(prev_args):]
        for arg in new_args:
            changes.append(f"[ADDED Argument] by {arg.get('author')} ({arg.get('classification')}): \"{arg.get('argument')[:100]}...\"")
            
    return changes

def validate_issue(repo: str, item_prefix: str):
    formalized_dir = Path(__file__).parent / "data" / "formalized" / repo
    if not formalized_dir.exists():
        print(f"Directory not found: {formalized_dir}")
        return
        
    files = [f for f in formalized_dir.glob(f"{item_prefix}_v*.json")]
    files.sort(key=lambda x: get_v_num(x.name))
    
    if not files:
        print(f"No files found for {item_prefix} in {repo}")
        return
        
    print(f"\n{'='*80}")
    print(f" INCREMENTAL VALIDATION REPORT: {item_prefix} in {repo}")
    print(f"{'='*80}\n")
    
    prev_formalized = None
    
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            curr_formalized = json.load(f)
            
        v_num = get_v_num(file_path.name)
        author = curr_formalized.get("author")
        timestamp = curr_formalized.get("timestamp")
        
        if v_num == 1:
            print(f"VERSION 1 (Initial State) - Triggered by {author} at {timestamp}")
            issue = curr_formalized.get("schema_data", {}).get("Issue")
            if issue:
                print(f"  Title: {issue.get('title')}")
            args = curr_formalized.get("schema_data", {}).get("Argument", [])
            print(f"  Initial Arguments: {len(args)}")
        else:
            changes = diff_versions(prev_formalized, curr_formalized)
            print(f"\nVERSION {v_num} - Triggered by {author} at {timestamp}")
            if not changes:
                print("  (No changes detected in schema data)")
            else:
                for change in changes:
                    print(f"  + {change}")
                    
        prev_formalized = curr_formalized

if __name__ == "__main__":
    # Default to the issue we've been working on
    validate_issue("Project-MONAI_MONAI", "issue_8261")

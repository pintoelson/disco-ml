import os
import json
import yaml
from pathlib import Path
from pydantic import ValidationError
from .models import GitHubItem, VersionedItem

def get_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_phase3():
    base_dir = Path(__file__).parent.parent
    config = get_config(base_dir / "config.yaml")
    
    # Path to RAW data (now consuming directly from Phase 1)
    raw_dir = Path(__file__).parent / "data" / "raw"
    versioned_dir = Path(__file__).parent / "data" / "versioned"
    versioned_dir.mkdir(parents=True, exist_ok=True)
    
    for repo_dir in raw_dir.iterdir():
        if not repo_dir.is_dir():
            continue
            
        repo_versioned_dir = versioned_dir / repo_dir.name
        repo_versioned_dir.mkdir(exist_ok=True)
        
        files = list(repo_dir.glob("*.json"))
        print(f"Creating versioned states for {len(files)} items in {repo_dir.name}...")
        
        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            try:
                item = GitHubItem(**data)
            except ValidationError as e:
                print(f"    Validation error on {file_path.name}: {e}")
                continue
            
            # 1. Create v1 (Initial State)
            version_count = 1
            timestamp_str = item.timestamp.strftime("%Y%m%d%H%M%S")
            v1_id = f"{item.id}_v1_{timestamp_str}"
            
            # v1 delta is the issue body
            v1_context = f"# Title: {item.title}\n\n"
            v1_context += f"**Author:** {item.author}\n"
            v1_context += f"**Timestamp:** {item.timestamp}\n\n"
            v1_context += f"## Body\n{item.body}\n"
            
            v1_item = VersionedItem(
                version_id=v1_id,
                parent_id=item.id,
                parent_type=item.item_type,
                parent_number=item.number,
                author=item.author,
                timestamp=item.timestamp,
                status=item.status,
                text_content=v1_context,
                previous_version_id=None
            )
            v1_out_file = repo_versioned_dir / f"{item.item_type}_{item.number}_v1.json"
            with open(v1_out_file, "w", encoding="utf-8") as f:
                f.write(v1_item.model_dump_json(indent=2))
            
            last_version_id = v1_id
            
            # 2. Create subsequent versions for EVERY comment (No filtering)
            sorted_comments = sorted(item.comments, key=lambda x: x.timestamp)
            
            for comment in sorted_comments:
                version_count += 1
                timestamp_str = comment.timestamp.strftime("%Y%m%d%H%M%S")
                version_id = f"{item.id}_v{version_count}_{timestamp_str}"
                
                # Context is ONLY the current comment for delta-based versioning
                comment_context = f"### Comment by {comment.author} at {comment.timestamp}\n{comment.body}"
                
                versioned_item = VersionedItem(
                    version_id=version_id,
                    parent_id=item.id,
                    parent_type=item.item_type,
                    parent_number=item.number,
                    author=comment.author,
                    timestamp=comment.timestamp,
                    status=item.status,
                    text_content=comment_context,
                    previous_version_id=last_version_id
                )
                
                out_file = repo_versioned_dir / f"{item.item_type}_{item.number}_v{version_count}.json"
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(versioned_item.model_dump_json(indent=2))
                
                last_version_id = version_id
            
            print(f"  Created {version_count} versions for {file_path.name}")

if __name__ == "__main__":
    run_phase3()

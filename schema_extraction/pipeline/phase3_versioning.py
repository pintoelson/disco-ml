import json
from pathlib import Path
from pydantic import ValidationError
from .models import GitHubItem, VersionedItem

def format_context(item: GitHubItem, comments_up_to_now: list) -> str:
    context = f"# Title: {item.title}\n\n"
    context += f"**Author:** {item.author}\n"
    context += f"**Timestamp:** {item.timestamp}\n\n"
    context += f"## Body\n{item.body}\n\n"
    context += "## Comments Context\n"
    for c in comments_up_to_now:
        context += f"### Comment by {c.author} at {c.timestamp} (Classification: {c.classification})\n{c.body}\n\n"
    return context.strip()

def run_phase3():
    classified_dir = Path(__file__).parent / "data" / "classified"
    versioned_dir = Path(__file__).parent / "data" / "versioned"
    versioned_dir.mkdir(parents=True, exist_ok=True)
    
    for repo_dir in classified_dir.iterdir():
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
            
            # Always create v1 (just the body, no comments)
            version_count = 1
            timestamp_str = item.timestamp.strftime("%Y%m%d%H%M%S")
            v1_id = f"{item.id}_v1_{timestamp_str}"
            v1_item = VersionedItem(
                version_id=v1_id,
                parent_id=item.id,
                parent_type=item.item_type,
                parent_number=item.number,
                author=item.author,
                timestamp=item.timestamp,
                status=item.status,
                text_content=format_context(item, []),
                trigger_classification="Original Body",
                lifecycle_stage=item.lifecycle_stage,
                lifecycle_artifact=item.lifecycle_artifact,
                lifecycle_justification=item.lifecycle_justification
            )
            v1_out_file = repo_versioned_dir / f"{item.item_type}_{item.number}_v1.json"
            with open(v1_out_file, "w", encoding="utf-8") as f:
                f.write(v1_item.model_dump_json(indent=2))
            
            # Sort comments chronologically just in case
            sorted_comments = sorted(item.comments, key=lambda x: x.timestamp)
            comments_up_to_now = []
            
            for comment in sorted_comments:
                comments_up_to_now.append(comment)
                
                # If comment is relevant, create a version state
                if comment.classification in ["Pro", "Con", "Neutral"]:
                    version_count += 1
                    timestamp_str = comment.timestamp.strftime("%Y%m%d%H%M%S")
                    version_id = f"{item.id}_v{version_count}_{timestamp_str}"
                    
                    versioned_item = VersionedItem(
                        version_id=version_id,
                        parent_id=item.id,
                        parent_type=item.item_type,
                        parent_number=item.number,
                        author=item.author,
                        timestamp=comment.timestamp,
                        status=item.status,
                        text_content=format_context(item, comments_up_to_now),
                        trigger_classification=comment.classification,
                        lifecycle_stage=item.lifecycle_stage,
                        lifecycle_artifact=item.lifecycle_artifact,
                        lifecycle_justification=item.lifecycle_justification
                    )
                    
                    out_file = repo_versioned_dir / f"{item.item_type}_{item.number}_v{version_count}.json"
                    with open(out_file, "w", encoding="utf-8") as f:
                        f.write(versioned_item.model_dump_json(indent=2))
            
            print(f"  Created {version_count} versions for {file_path.name}")

if __name__ == "__main__":
    run_phase3()

import os
import json
from pathlib import Path
from dotenv import load_dotenv
import litellm
from typing import Optional
from pydantic import BaseModel, ValidationError, Field

from .models import GitHubItem, GitHubComment

# Define the structured output format for the LLM
class CommentClassification(BaseModel):
    intent: str  # Pro, Con, Neutral, NA
    justification: Optional[str] = None

class LifecycleClassification(BaseModel):
    mapped_stage: str = Field(alias="Mapped Stage")
    primary_artifact: str = Field(alias="Primary Artifact")
    justification: str = Field(alias="Justification")

def classify_comment(comment_body: str, model: str, prompt_template: str) -> CommentClassification:
    if not comment_body.strip():
        return CommentClassification(intent="NA", justification="Empty comment")
        
    try:
        # Note: double curly braces in the text file are already there for .format()
        content_prompt = prompt_template.format(comment_body=comment_body)
        
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": content_prompt}],
            response_format=CommentClassification,
            api_key=os.environ.get("RWTH_GPT_API_KEY"),
        )
        # Some litellm models return json directly if response_format is provided.
        content = response.choices[0].message.content
        if isinstance(content, str):
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            try:
                data = json.loads(content)
                if 'classification' in data and 'intent' not in data:
                    data['intent'] = data['classification']
                return CommentClassification(**data)
            except json.JSONDecodeError:
                return CommentClassification(intent="NA", justification=f"Failed to parse LLM response: {content[:100]}")
        elif isinstance(content, dict):
            return CommentClassification(**content)
        elif isinstance(content, CommentClassification):
            return content
        else:
             return CommentClassification(intent="NA", justification="Unexpected LLM response format")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"      LLM Classification error: {e}")
        return CommentClassification(intent="NA", justification=f"Error: {str(e)}")

def classify_lifecycle(item: GitHubItem, model: str, prompt_template: str) -> LifecycleClassification:
    try:
        input_json = json.dumps({
            "title": item.title,
            "body": item.body
        })
        content_prompt = prompt_template.format(input_json=input_json)
        
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": content_prompt}],
            response_format=LifecycleClassification,
            api_key=os.environ.get("RWTH_GPT_API_KEY"),
        )
        content = response.choices[0].message.content
        if isinstance(content, str):
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            data = json.loads(content)
            return LifecycleClassification(**data)
        elif isinstance(content, dict):
            return LifecycleClassification(**content)
        else:
            raise ValueError("Unexpected response format")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"      LLM Lifecycle Classification error: {e}")
        return LifecycleClassification(**{
            "Mapped Stage": "Uncertain",
            "Primary Artifact": "N/A",
            "Justification": f"Error: {str(e)}"
        })

def run_phase2():
    base_dir = Path(__file__).parent.parent
    load_dotenv(base_dir.parent / ".env")
    
    prompts_dir = base_dir / "prompts"
    with open(prompts_dir / "comment_classification.txt", "r") as f:
        comment_prompt = f.read()
    with open(prompts_dir / "lifecycle_classification.txt", "r") as f:
        lifecycle_prompt = f.read()

    raw_dir = Path(__file__).parent / "data" / "raw"
    classified_dir = Path(__file__).parent / "data" / "classified"
    classified_dir.mkdir(parents=True, exist_ok=True)
    
    # The user specifically requested rwth_gpt/gpt-oss-120b
    model_name = "rwth_gpt/gpt-oss-120b"
    print(f"Using model: {model_name} for Phase 2")
    
    for repo_dir in raw_dir.iterdir():
        if not repo_dir.is_dir():
            continue
            
        repo_classified_dir = classified_dir / repo_dir.name
        repo_classified_dir.mkdir(exist_ok=True)
        
        files = list(repo_dir.glob("*.json"))
        print(f"Classifying items for {len(files)} items in {repo_dir.name}...")
        
        for file_path in files:
            print(f"  Processing {file_path.name}")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            try:
                item = GitHubItem(**data)
            except ValidationError as e:
                print(f"    Validation error on {file_path.name}: {e}")
                continue
            
            # Lifecycle classification
            lifecycle = classify_lifecycle(item, model_name, lifecycle_prompt)
            item.lifecycle_stage = lifecycle.mapped_stage
            item.lifecycle_artifact = lifecycle.primary_artifact
            item.lifecycle_justification = lifecycle.justification

            # Comment classification
            for comment in item.comments:
                classification = classify_comment(comment.body, model_name, comment_prompt)
                comment.classification = classification.intent
                comment.justification = classification.justification
                
            out_file = repo_classified_dir / file_path.name
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(item.model_dump_json(indent=2))

if __name__ == "__main__":
    run_phase2()

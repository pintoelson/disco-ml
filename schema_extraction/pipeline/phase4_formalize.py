import os
import json
import yaml
from pathlib import Path
from dotenv import load_dotenv
from contextgem import Document, DocumentLLM, StringConcept, JsonObjectConcept
from pydantic import ValidationError

from .models import VersionedItem, DecisionFormalization

def get_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def extract_decision_concepts(versioned_item: VersionedItem, llm, schema):
    # Prepend a global instruction to ensure consistent extraction across versions
    system_instruction = (
        "INSTRUCTION: You are extracting the CURRENT STATE of an architectural decision from a chronological discussion. "
        "Maintain all established consensus, rationales, costs, and risks identified in earlier parts of the text "
        "unless they are explicitly contradicted or updated in later comments. DO NOT return null for these fields "
        "if the information was already established in the history.\n\n"
    )
    doc = Document(raw_text=system_instruction + versioned_item.text_content)
    
    TYPE_MAP = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
    }

    concepts = []
    for item in schema:
        if item.get('type') == 'JsonObjectConcept':
            structure = {
                k: TYPE_MAP.get(v, v) for k, v in item['structure'].items()
            }
            concepts.append(JsonObjectConcept(
                name=item['name'],
                description=item['description'],
                structure=structure,
                singular_occurrence=item.get('singular_occurrence', True)
            ))
        else:
            concepts.append(StringConcept(
                name=item['name'], 
                description=item['description'],
                singular_occurrence=item.get('singular_occurrence', True)
            ))
    doc.concepts = concepts

    doc = llm.extract_all(doc)

    findings = {}
    for concept in doc.concepts:
        singular = concept.singular_occurrence
        if concept.extracted_items:
            if singular:
                findings[concept.name] = concept.extracted_items[0].value
            else:
                findings[concept.name] = [item.value for item in concept.extracted_items]
        else:
            findings[concept.name] = None if singular else []
            
    return findings

def run_phase4():
    base_dir = Path(__file__).parent.parent
    load_dotenv(base_dir.parent / ".env")
    
    config_path = base_dir / "config.yaml"
    config = get_config(config_path)
    schema = config.get('extraction_schema', [])
    
    if not schema:
        print("No extraction schema found in config.yaml.")
        return

    # The user specifically requested rwth_gpt/gpt-oss-120b
    model_name = "rwth_gpt/gpt-oss-120b"
    print(f"Using model: {model_name} for Phase 4")
    
    llm = DocumentLLM(
        model=model_name,
        api_key=os.environ.get("RWTH_GPT_API_KEY"),
    )

    versioned_dir = Path(__file__).parent / "data" / "versioned"
    formalized_dir = Path(__file__).parent / "data" / "formalized"
    formalized_dir.mkdir(parents=True, exist_ok=True)
    
    for repo_dir in versioned_dir.iterdir():
        if not repo_dir.is_dir():
            continue
            
        repo_formalized_dir = formalized_dir / repo_dir.name
        repo_formalized_dir.mkdir(exist_ok=True)
        
        files = list(repo_dir.glob("*.json"))
        print(f"Formalizing decisions for {len(files)} versions in {repo_dir.name}...")
        
        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            try:
                versioned_item = VersionedItem(**data)
            except ValidationError as e:
                print(f"    Validation error on {file_path.name}: {e}")
                continue
                
            out_file = repo_formalized_dir / file_path.name
            if out_file.exists():
                print(f"  Skipping {file_path.name} (already formalized)")
                continue
                
            print(f"  Extracting schema for {file_path.name}")
            try:
                findings = extract_decision_concepts(versioned_item, llm, schema)
                decision = DecisionFormalization(
                    version_id=versioned_item.version_id,
                    filename=file_path.name,
                    author=versioned_item.author,
                    timestamp=versioned_item.timestamp,
                    status=versioned_item.status,
                    lifecycle_stage=versioned_item.lifecycle_stage,
                    lifecycle_artifact=versioned_item.lifecycle_artifact,
                    schema_data=findings
                )
                
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(decision.model_dump_json(indent=2))
            except Exception as e:
                print(f"    Failed to extract from {file_path.name}: {e}")

if __name__ == "__main__":
    run_phase4()

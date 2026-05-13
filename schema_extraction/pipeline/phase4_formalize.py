import os
import json
import yaml
import litellm
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
from .models import VersionedItem, DecisionFormalization
from contextgem import Document, DocumentLLM, StringConcept, JsonObjectConcept
from pydantic import create_model, Field

def get_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def build_schema_from_config(config: Dict[str, Any]) -> List[Any]:
    schema = []
    for concept_cfg in config['extraction_schema']:
        name = concept_cfg['name']
        desc = concept_cfg['description']
        singular = concept_cfg.get('singular_occurrence', False)
        
        if concept_cfg.get('type') == 'JsonObjectConcept':
            fields = {}
            for field_name, field_type_raw in concept_cfg['structure'].items():
                # Extract description from "type (desc)" pattern
                if "(" in field_type_raw:
                    field_type_str = field_type_raw.split("(")[0].strip()
                    field_desc = field_type_raw.split("(")[1].strip(" )")
                else:
                    field_type_str = field_type_raw
                    field_desc = f"The {field_name} of the {name}."
                
                type_map = {"str": str, "int": int, "float": float, "bool": bool, "list": List[str]}
                py_type = type_map.get(field_type_str, str)
                
                fields[field_name] = (py_type, Field(default=None, description=field_desc))
            
            DynamicModel = create_model(f"{name}Model", **fields)
            schema.append(JsonObjectConcept(
                name=name,
                description=desc,
                structure=DynamicModel,
                singular_occurrence=singular
            ))
        else:
            schema.append(StringConcept(
                name=name,
                description=desc,
                singular_occurrence=singular
            ))
    return schema

def extract_decision_concepts(version_item: VersionedItem, model_name: str, config: Dict[str, Any], cumulative_state: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Uses ContextGem to extract concepts from a single version fragment.
    """
    # 1. Prepare Informed Context
    current_decision = (cumulative_state or {}).get("Decision", "No decision established yet.")
    context_str = (
        f"### CURRENT KNOWLEDGE BASE (v1 to v(n-1))\n"
        f"CURRENT DECISION: {current_decision}\n"
        f"FULL STATE:\n{json.dumps(cumulative_state, indent=2) if cumulative_state else 'Empty (This is v1)'}"
    )
    
    fragment_text = (
        f"{context_str}\n\n"
        f"### NEW FRAGMENT (TO EXTRACT FROM)\n"
        f"Author: {version_item.author}\n"
        f"Timestamp: {version_item.timestamp}\n"
        f"Content:\n{version_item.text_content}"
    )

    # 2. Build Schema
    schema = build_schema_from_config(config)
    
    # 3. Setup ContextGem
    doc = Document(raw_text=fragment_text)
    doc.add_concepts(schema)
    
    llm = DocumentLLM(
        model=model_name,
        api_key=os.getenv("RWTH_GPT_API_KEY")
    )
    
    # 4. Extract
    doc = llm.extract_all(doc)
    
    # 5. Collect findings
    findings = {}
    for concept in doc.concepts:
        items = concept.extracted_items
        # Map "Interaction" back to "Argument" for output consistency
        concept_name = "Argument" if concept.name == "Interaction" else concept.name
        
        if concept.singular_occurrence:
            val = items[0].value if items else None
            if hasattr(val, "model_dump"):
                val = val.model_dump()
            
            # Post-processing for Decision authors (convert str to list)
            if concept_name == "Decision" and isinstance(val, dict):
                authors_raw = val.get("authors")
                if isinstance(authors_raw, str):
                    val["authors"] = [a.strip() for a in authors_raw.split(",") if a.strip()]
            
            findings[concept_name] = val
        else:
            findings[concept_name] = [i.value.model_dump() if hasattr(i.value, "model_dump") else i.value for i in items]
    
    return findings

def merge_findings(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    """Merges new delta findings into the cumulative established state."""
    merged = previous.copy() if previous else {}
    
    # Update single fields if current has new data
    for key in ["Issue", "Decision", "Rationale", "Description", "Cost", "Risk"]:
        val = current.get(key)
        if val and val != "null" and val != "None":
            # (Note: findings are already dumped to dict in extract_decision_concepts now)
                
            # For Issue, we only update subfields that are not null
            if key == "Issue" and isinstance(val, dict):
                if "Issue" not in merged: merged["Issue"] = {}
                for k, v in val.items():
                    if v: merged["Issue"][k] = v
            elif key == "Decision" and isinstance(val, dict):
                if "Decision" not in merged or not isinstance(merged["Decision"], dict):
                    merged["Decision"] = {"decision": None, "authors": []}
                
                # Update text if new one is provided
                if val.get("decision"):
                    merged["Decision"]["decision"] = val["decision"]
                
                # Merge authors
                new_authors = val.get("authors", [])
                if isinstance(new_authors, list):
                    existing_authors = set(merged["Decision"].get("authors", []))
                    for a in new_authors:
                        if a and a not in existing_authors:
                            merged["Decision"]["authors"].append(a)
            else:
                merged[key] = val
            
    # Merge Arguments
    new_args = current.get("Argument", [])
    if isinstance(new_args, list) and len(new_args) > 0:
        if "Argument" not in merged:
            merged["Argument"] = []
        # Basic de-duplication based on text (since LLM might repeat if not careful)
        existing_texts = {a.get("argument", "") for a in merged["Argument"]}
        for arg in new_args:
            if arg.get("argument") not in existing_texts:
                merged["Argument"].append(arg)
                
    return merged

def run_phase4():
    base_dir = Path(__file__).parent.parent
    load_dotenv(base_dir.parent / ".env")
    config = get_config(base_dir / "config.yaml")
    llm = config.get('extraction_model', 'rwth_gpt/mistralai-mistral-small-4-119b')
    
    versioned_dir = Path(__file__).parent / "data" / "versioned"
    formalized_dir = Path(__file__).parent / "data" / "formalized"
    formalized_dir.mkdir(parents=True, exist_ok=True)
    
    for repo_dir in versioned_dir.iterdir():
        if not repo_dir.is_dir():
            continue
            
        repo_formalized_dir = formalized_dir / repo_dir.name
        repo_formalized_dir.mkdir(exist_ok=True)
        
        issue_versions: Dict[str, List[Path]] = {}
        for v_file in repo_dir.glob("*.json"):
            parts = v_file.stem.split("_")
            issue_key = f"{parts[0]}_{parts[1]}"
            if issue_key not in issue_versions:
                issue_versions[issue_key] = []
            issue_versions[issue_key].append(v_file)
            
        for issue_key, versions in issue_versions.items():
            versions.sort(key=lambda x: int(x.stem.split("_v")[-1]))
            print(f"Formalizing decisions for {issue_key} ({len(versions)} versions)...")
            
            cumulative_state = {}
            for v_path in versions:
                print(f"  Incremental extraction for {v_path.name}")
                with open(v_path, "r", encoding="utf-8") as f:
                    v_data = json.load(f)
                v_item = VersionedItem(**v_data)
                
                delta_findings = extract_decision_concepts(v_item, llm, config, cumulative_state if cumulative_state else None)
                cumulative_state = merge_findings(delta_findings, cumulative_state)
                
                # Nest metadata inside decision_ticket
                decision_ticket_data = cumulative_state.copy()
                decision_ticket_data["filename"] = v_path.name
                decision_ticket_data["status"] = v_item.status
                decision_ticket_data["timestamp"] = v_item.timestamp.isoformat() if hasattr(v_item.timestamp, "isoformat") else str(v_item.timestamp)
                
                formalized_item = DecisionFormalization(
                    decision_ticket=decision_ticket_data
                )
                
                out_file = repo_formalized_dir / v_path.name
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(formalized_item.model_dump_json(indent=2))

if __name__ == "__main__":
    run_phase4()

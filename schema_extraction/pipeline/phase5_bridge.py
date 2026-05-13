import os
import json
import yaml
import litellm
from pathlib import Path
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from .models import VersionedItem, DecisionFormalization, BridgedDecision, MLAsset
from contextgem import Document, DocumentLLM, StringConcept, JsonObjectConcept
from pydantic import create_model, Field

def get_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def build_schema_from_config(config_list: List[Dict[str, Any]]) -> List[Any]:
    schema = []
    for concept_cfg in config_list:
        name = concept_cfg['name']
        desc = concept_cfg['description']
        singular = concept_cfg.get('singular_occurrence', False)
        
        if concept_cfg.get('type') == 'JsonObjectConcept':
            fields = {}
            for field_name, field_type_raw in concept_cfg['structure'].items():
                if "(" in field_type_raw:
                    field_type_str = field_type_raw.split("(")[0].strip()
                    field_desc = field_type_raw.split("(")[1].strip(" )")
                else:
                    field_type_str = field_type_raw
                    field_desc = f"The {field_name} of the {name}."
                
                type_map = {"str": str, "int": int, "float": float, "bool": bool, "list": List[str]}
                base_type = type_map.get(field_type_str, str)
                py_type = Optional[base_type]
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

def run_bridge_mapping(formalized_item: DecisionFormalization, raw_item: VersionedItem, model_name: str, prompt_template: str, config: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Uses ContextGem to map a single version to the ontology bridge."""
    
    fragment_text = prompt_template.format(
        formalized_json=json.dumps(formalized_item.decision_ticket, indent=2),
        raw_text=raw_item.text_content
    )

    schema = build_schema_from_config(config)
    
    doc = Document(raw_text=fragment_text)
    doc.add_concepts(schema)
    
    llm = DocumentLLM(
        model=model_name,
        api_key=os.getenv("RWTH_GPT_API_KEY")
    )
    
    doc = llm.extract_all(doc)
    
    findings = {}
    for concept in doc.concepts:
        items = concept.extracted_items
        if concept.singular_occurrence:
            findings[concept.name] = items[0].value if items else "NA"
        else:
            findings[concept.name] = [i.value for i in items]
            
    return findings

def run_phase5():
    base_dir = Path(__file__).parent.parent
    load_dotenv(base_dir.parent / ".env")
    config = get_config(base_dir / "config.yaml")
    llm = config.get('extraction_model', 'rwth_gpt/mistralai-mistral-small-4-119b')
    
    with open(base_dir / "prompts" / "bridge_mapping.txt", "r") as f:
        prompt_template = f.read()
    
    versioned_dir = Path(__file__).parent / "data" / "versioned"
    formalized_dir = Path(__file__).parent / "data" / "formalized"
    bridged_dir = Path(__file__).parent / "data" / "bridged"
    bridged_dir.mkdir(parents=True, exist_ok=True)
    
    for repo_dir in formalized_dir.iterdir():
        if not repo_dir.is_dir():
            continue
            
        repo_bridged_dir = bridged_dir / repo_dir.name
        repo_bridged_dir.mkdir(exist_ok=True)
        
        issue_versions: Dict[str, List[Path]] = {}
        for f_file in repo_dir.glob("*.json"):
            parts = f_file.stem.split("_")
            issue_key = f"{parts[0]}_{parts[1]}"
            if issue_key not in issue_versions:
                issue_versions[issue_key] = []
            issue_versions[issue_key].append(f_file)
            
        for issue_key, versions in issue_versions.items():
            versions.sort(key=lambda x: int(x.stem.split("_v")[-1]))
            print(f"Mapping ontology bridge for {issue_key} ({len(versions)} versions)...")
            
            cumulative_roles = {}
            cumulative_main_assets = []
            cumulative_mentioned_assets = []
            
            for f_path in versions:
                v_path = versioned_dir / repo_dir.name / f_path.name
                if not v_path.exists():
                    print(f"Warning: Versioned file not found for {f_path.name}")
                    continue
                    
                print(f"  Mapping bridge for {f_path.name}")
                
                with open(f_path, "r") as f:
                    f_data = json.load(f)
                formalized_item = DecisionFormalization(**f_data)
                
                with open(v_path, "r") as f:
                    v_data = json.load(f)
                raw_item = VersionedItem(**v_data)
                
                bridge_findings = run_bridge_mapping(formalized_item, raw_item, llm, prompt_template, config['bridge_schema'])
                
                # Accumulate roles
                current_author = raw_item.author
                current_role = bridge_findings.get("author_role", "NA")
                if current_role and current_role != "NA":
                    cumulative_roles[current_author] = current_role
                
                # Helper for asset accumulation
                def accumulate_assets(new_assets_raw, target_list, fragment_author=None):
                    for na in new_assets_raw:
                        na_dict = na.model_dump() if hasattr(na, "model_dump") else na
                        if not na_dict.get("name") or na_dict.get("name") == "NA":
                            continue
                        
                        # Parse discussed_by if it's a string
                        new_authors = []
                        if "discussed_by" in na_dict and isinstance(na_dict["discussed_by"], str):
                            # Replace ' and ' with comma to split uniformly
                            raw_authors = na_dict["discussed_by"].replace(" and ", ",").replace("&", ",")
                            new_authors = [a.strip().strip("'\"") for a in raw_authors.split(",") if a.strip()]
                        elif "discussed_by" in na_dict and isinstance(na_dict["discussed_by"], list):
                            new_authors = [str(a).strip().strip("'\"") for a in na_dict["discussed_by"] if str(a).strip()]
                        
                        # Post-process location to nullify placeholders
                        loc = na_dict.get("location")
                        if loc and any(word in loc.lower() for word in ["fragment", "text", "document", "formalized", "raw", "placeholder"]):
                            na_dict["location"] = None
                        elif loc and loc.lower() in ["n/a", "na", "null", "none"]:
                            na_dict["location"] = None

                        # Auto-inject fragment author if provided
                        if fragment_author and fragment_author not in new_authors:
                            new_authors.append(fragment_author)
                            
                        is_duplicate = False
                        for existing in target_list:
                            if existing.name.lower() == na_dict["name"].lower() and existing.asset_type == na_dict["asset_type"]:
                                # Update location if new one found
                                if na_dict.get("location") and not existing.location:
                                    existing.location = na_dict["location"]
                                
                                # Update state if new one found
                                if na_dict.get("current_state") and na_dict["current_state"] != "NA":
                                    existing.current_state = na_dict["current_state"]
                                    
                                # Merge authors
                                for author in new_authors:
                                    if author not in existing.discussed_by:
                                        existing.discussed_by.append(author)
                                        
                                is_duplicate = True
                                break
                        
                        if not is_duplicate:
                            # Create new asset with authors list
                            asset_data = na_dict.copy()
                            asset_data["discussed_by"] = new_authors
                            target_list.append(MLAsset(**asset_data))

                # Accumulate both lists
                accumulate_assets(bridge_findings.get("main_assets", []), cumulative_main_assets, fragment_author=raw_item.author)
                accumulate_assets(bridge_findings.get("mentioned_assets", []), cumulative_mentioned_assets)
                
                # Inject roles into decision_ticket
                decision_ticket = formalized_item.decision_ticket.copy()
                if "Issue" in decision_ticket:
                    issue_author = decision_ticket["Issue"].get("author")
                    if issue_author in cumulative_roles:
                        decision_ticket["Issue"]["author_role"] = cumulative_roles[issue_author]
                
                if "Argument" in decision_ticket:
                    for arg in decision_ticket["Argument"]:
                        arg_author = arg.get("author")
                        if arg_author in cumulative_roles:
                            arg["author_role"] = cumulative_roles[arg_author]

                bridged_item = BridgedDecision(
                    decision_ticket=decision_ticket,
                    ml_elements={
                        "lifecycle_stage": bridge_findings.get("lifecycle_stage", "Uncertain"),
                        "main_assets": [a.model_copy() for a in cumulative_main_assets],
                        "mentioned_assets": [a.model_copy() for a in cumulative_mentioned_assets],
                        "author_roles": cumulative_roles.copy()
                    }
                )
                
                out_file = repo_bridged_dir / f_path.name
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(bridged_item.model_dump_json(indent=2))

if __name__ == "__main__":
    run_phase5()

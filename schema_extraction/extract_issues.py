import os
import json
import yaml
from pathlib import Path
from contextgem import Document, DocumentLLM, StringConcept, JsonObjectConcept

def get_config(config_path="config.yaml"):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def load_dotenv(dotenv_path="../.env"):
    if os.path.exists(dotenv_path):
        print("Loading environment variables from .env...")
        with open(dotenv_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")

def extract_issue_concepts(issue_path, repo_output_dir, llm, schema):
    # Load the issue content
    with open(issue_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the document
    doc = Document(raw_text=content)

    # Type mapping for JsonObjectConcept structure
    TYPE_MAP = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
    }

    # Define the concepts to extract from schema
    concepts = []
    for item in schema:
        if item.get('type') == 'JsonObjectConcept':
            # Convert structure types from strings to Python types
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

    # Extract information
    print(f"    Extracting concepts from {issue_path.name}...")
    doc = llm.extract_all(doc)

    # Prepare findings
    findings = {}
    for i, concept in enumerate(doc.concepts):
        # schema_item = schema[i]
        singular = concept.singular_occurrence # Use the attribute from the concept object
        
        if concept.extracted_items:
            if singular:
                findings[concept.name] = concept.extracted_items[0].value
            else:
                findings[concept.name] = [item.value for item in concept.extracted_items]
        else:
            findings[concept.name] = None if singular else []

    # Save to directory if quality threshold is met
    total_fields = len(findings)
    null_count = sum(1 for v in findings.values() if v is None or (isinstance(v, list) and len(v) == 0))
    
    # If more than 50% of extracted schema is null, do not save
    if total_fields > 0 and (null_count / total_fields) > 0.5:
        print(f"    Skipping {issue_path.name}: Quality threshold not met ({null_count}/{total_fields} null fields)")
        return
        
    output_path = repo_output_dir / f"{issue_path.stem}_extracted.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2)

def main():
    load_dotenv()
    # Define paths
    base_dir = Path("/home/elson/Files/Automated_Ontology/schema_extraction")
    config_path = base_dir / "config.yaml"
    issues_base_dir = base_dir / "issues"
    output_base_dir = base_dir / "issues_extracted"

    # Load configuration
    config = get_config(config_path)
    schema = config.get('extraction_schema', [])
    
    if not schema:
        print("No extraction schema found in config.yaml.")
        return

    # Configure the LLM
    model_name = os.environ.get("RWTH_GPT_MODEL", "rwth_gpt/gpt-oss-120b")
    if "/" not in model_name:
        model_name = f"rwth_gpt/{model_name}"
    print(f"Using model: {model_name}")
    
    llm = DocumentLLM(
        model=model_name,
        api_key=os.environ.get("RWTH_GPT_API_KEY"),
    )

    if not issues_base_dir.exists():
        print("Issues directory not found.")
        return

    # Iterate through each repository directory
    for repo_dir in issues_base_dir.iterdir():
        if not repo_dir.is_dir():
            continue

        print(f"Processing repository: {repo_dir.name}")
        
        # Mirror the directory structure in output
        repo_output_dir = output_base_dir / repo_dir.name
        repo_output_dir.mkdir(parents=True, exist_ok=True)

        # Get all markdown issues in this repo
        issues = sorted(list(repo_dir.glob("*.md")))
        
        if not issues:
            print(f"  No issues found for {repo_dir.name}.")
            continue

        print(f"  Found {len(issues)} issues.")

        for issue_path in issues:
            # Skip if already extracted to save time
            output_path = repo_output_dir / f"{issue_path.stem}_extracted.json"
            if output_path.exists():
                print(f"    Skipping {issue_path.name} (already extracted)")
                continue

            try:
                extract_issue_concepts(issue_path, repo_output_dir, llm, schema)
            except Exception as e:
                print(f"    Failed to process {issue_path.name}: {e}")

    print("\nExtraction process complete.")

if __name__ == "__main__":
    main()

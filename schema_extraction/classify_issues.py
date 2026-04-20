import os
import json
import yaml
from pathlib import Path
import litellm

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

def classify_issue(issue_json, prompt_template, model_name):
    # Prepare the prompt
    prompt = prompt_template.replace("{input_json}", json.dumps(issue_json, indent=2))
    
    try:
        response = litellm.completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            api_key=os.environ.get("RWTH_GPT_API_KEY"),
        )
        
        content = response.choices[0].message.content
        
        # Clean up potential markdown formatting
        if content.startswith("```json"):
            content = content.split("```json")[1].split("```")[0].strip()
        elif content.startswith("```"):
            content = content.split("```")[1].split("```")[0].strip()
        
        # Try to find the first '{' and last '}' if parsing fails
        try:
            classification = json.loads(content)
        except json.JSONDecodeError:
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            if start_idx != -1 and end_idx != -1:
                content = content[start_idx:end_idx+1]
                classification = json.loads(content)
            else:
                raise
                
        return classification
    except Exception as e:
        print(f"    Error classifying/parsing response: {e}")
        return None

def main():
    load_dotenv()
    
    # Define paths
    base_dir = Path("/home/elson/Files/Automated_Ontology/schema_extraction")
    input_dir = base_dir / "issues_extracted"
    output_dir = Path("/home/elson/Files/Automated_Ontology/prototype-tool/decision-tickets")
    prompt_path = base_dir / "prompts" / "issue_classification.txt"
    
    if not prompt_path.exists():
        print(f"Prompt file not found at {prompt_path}")
        return

    # Load the prompt template
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()
        
    # Configure the model
    model_name = os.environ.get("RWTH_GPT_MODEL", "rwth_gpt/gpt-oss-120b")
    if "/" not in model_name:
        model_name = f"rwth_gpt/{model_name}"
    
    print(f"Using model: {model_name}")
    
    if not input_dir.exists():
        print(f"Input directory {input_dir} not found.")
        return

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Iterate through each repository directory
    for repo_dir in input_dir.iterdir():
        if not repo_dir.is_dir():
            continue
            
        print(f"Processing repository: {repo_dir.name}")
        
        # Get all extracted JSON files
        json_files = sorted(list(repo_dir.glob("*.json")))
        
        if not json_files:
            print(f"  No extracted JSONs found for {repo_dir.name}.")
            continue

        print(f"  Found {len(json_files)} issues to classify.")

        for json_file in json_files:
            output_file = output_dir / json_file.name
            
            # Skip if already classified
            if output_file.exists():
                print(f"    Skipping {json_file.name} (already classified in {output_dir})")
                continue
                
            print(f"    Classifying {json_file.name}...")
            try:
                with open(json_file, 'r') as f:
                    issue_data = json.load(f)
                
                classification = classify_issue(issue_data, prompt_template, model_name)
                
                if classification:
                    # Merge classification into original data
                    issue_data.update(classification)
                    
                    with open(output_file, 'w') as f:
                        json.dump(issue_data, f, indent=2)
                else:
                    print(f"    Failed to classify {json_file.name}")
            except Exception as e:
                print(f"    Error processing {json_file.name}: {e}")

    print("\nClassification process complete.")

if __name__ == "__main__":
    main()

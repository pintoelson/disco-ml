import os
import json
from pathlib import Path
from contextgem import Document, DocumentLLM, StringConcept

def extract_issue_concepts(issue_path, output_dir, llm):
    # Load the issue content
    with open(issue_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Define the document
    doc = Document(raw_text=content)

    # Define the concepts to extract
    doc.concepts = [
        StringConcept(name="Issue", description="A short summary of the problem or topic discussed."),
        StringConcept(name="Decision", description="The final outcome, resolution, or proposed path forward discussed in the issue."),
        StringConcept(name="Rationale", description="The reasoning, justification, or context behind the decision or proposal."),
        StringConcept(name="Author", description="The username of the person who created the issue."),
        StringConcept(name="Status", description="The current status of the issue (e.g., open, closed)."),
        StringConcept(name="Description", description="A detailed explanation of the issue's content."),
        StringConcept(name="Time stamp", description="The creation or modification date of the issue, if available."),
        StringConcept(name="Cost", description="Any mention of effort, resource usage, or financial cost associated with the issue or its resolution."),
        StringConcept(name="Risk", description="Any mention of potential problems, side effects, or downsides associated with a decision or proposal.")
    ]

    # Extract information
    print(f"Extracting concepts from {issue_path.name}...")
    doc = llm.extract_all(doc)

    # Prepare findings
    findings = {}
    for concept in doc.concepts:
        if concept.extracted_items:
            findings[concept.name] = concept.extracted_items[0].value
        else:
            findings[concept.name] = None

    # Save to directory
    output_path = output_dir / f"{issue_path.stem}_extracted.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2)
    
    print(f"Results saved to {output_path}")

def main():
    # Define paths
    base_dir = Path("/home/elson/Files/Automated_Ontology/schema_extraction")
    issues_dir = base_dir / "issues" / "pallets_click"
    output_dir = base_dir / "issues_extracted"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Configure the LLM (initialize once)
    llm = DocumentLLM(
        model="rwth_gpt/gpt-oss-120b",
        api_key=os.environ.get("RWTH_GPT_API_KEY"),
    )

    # Get all markdown issues
    issues = sorted(list(issues_dir.glob("*.md")))
    
    if not issues:
        print("No issues found in the source directory.")
        return

    print(f"Found {len(issues)} issues. Starting extraction...")

    for issue_path in issues:
        # Check if already processed to save time/tokens if needed
        # output_path = output_dir / f"{issue_path.stem}_extracted.json"
        # if output_path.exists():
        #     print(f"Skipping {issue_path.name} (already processed)")
        #     continue
            
        try:
            extract_issue_concepts(issue_path, output_dir, llm)
        except Exception as e:
            print(f"Failed to process {issue_path.name}: {e}")

    print("\nAll extractions complete.")

if __name__ == "__main__":
    main()

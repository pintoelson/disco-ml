import os
from contextgem import Document, DocumentLLM, StringConcept

def test_multi_extraction():
    text = """
    We discussed several ideas for the project:
    1. Migration to Python 3.12 for better performance.
    2. Using Click for CLI interactions as it's more robust than argparse.
    3. Implementing a thorough CI/CD pipeline with GitHub Actions.
    """

    doc = Document(raw_text=text)
    doc.concepts = [
        StringConcept(
            name="Idea",
            description="A specific idea or proposal mentioned for the project.",
            singular_occurrence=False # This is the default, but being explicit for the test
        )
    ]

    llm = DocumentLLM(
        model="rwth_gpt/gpt-oss-120b",
        api_key=os.environ.get("RWTH_GPT_API_KEY"),
    )

    print("Extracting multiple ideas...")
    doc = llm.extract_all(doc)

    idea_concept = doc.concepts[0]
    print(f"Concept: {idea_concept.name}")
    print(f"Number of items extracted: {len(idea_concept.extracted_items)}")
    
    for i, item in enumerate(idea_concept.extracted_items):
        print(f"  {i+1}: {item.value}")

if __name__ == "__main__":
    test_multi_extraction()

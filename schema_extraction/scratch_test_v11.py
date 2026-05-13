import os
import json
import yaml
from contextgem import Document, JsonObjectConcept, DocumentLLM
from pydantic import Field, create_model
from typing import List, Dict, Any

# Mock build_schema_from_config
def build_schema_from_config(config):
    # Just the Interaction part
    fields = {
        "author": (str, Field(default=None, description="GitHub username")),
        "timestamp": (str, Field(default=None, description="ISO timestamp")),
        "classification": (str, Field(default=None, description="Stance vs CURRENT DECISION: Pro, Con, or Neutral")),
        "argument": (str, Field(default=None, description="Technical content of the comment"))
    }
    InteractionModel = create_model("InteractionModel", **fields)
    return [
        JsonObjectConcept(
            name="Interaction",
            description="CONVERSATION LOG: Extract EVERY comment from the NEW FRAGMENT. This is a historical record, so NO fragment should be skipped. Label status checks as Neutral.",
            structure=InteractionModel,
            singular_occurrence=False
        )
    ]

def test_v11():
    fragment = """
### CURRENT KNOWLEDGE BASE (v1 to v10)
CURRENT DECISION: Standardize the way of getting model weights from Trainer
FULL STATE: {}

### NEW FRAGMENT (TO EXTRACT FROM)
Author: holgerroth
Timestamp: 2023-02-13 18:46:16
Content:
@Nic-Ma, @ericspod, any updates on this topic?
"""
    schema = build_schema_from_config(None)
    doc = Document(raw_text=fragment)
    doc.add_concepts(schema)
    
    llm = DocumentLLM(
        model="rwth_gpt/mistralai-mistral-small-4-119b",
        api_key=os.getenv("RWTH_GPT_API_KEY")
    )
    
    doc = llm.extract_all(doc)
    
    print("Findings:")
    for concept in doc.concepts:
        print(f"{concept.name}: {[i.value for i in concept.extracted_items]}")

if __name__ == "__main__":
    test_v11()

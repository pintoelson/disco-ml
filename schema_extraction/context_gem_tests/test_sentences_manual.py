# Quick Start Example - Manual sentence segmentation to avoid SaT model download

import os
from contextgem import Document, DocumentLLM, StringConcept, Paragraph, Sentence

# Define the document structure manually to avoid downloading the 428MB SaT model
# Each paragraph contains its own list of pre-segmented sentences.
p1 = Paragraph(raw_text="Consultancy Agreement", sentences=[Sentence(raw_text="Consultancy Agreement")])
p2 = Paragraph(raw_text="This agreement between Company A (Supplier) and Company B (Customer)...", sentences=[Sentence(raw_text="This agreement between Company A (Supplier) and Company B (Customer)...")])
p3 = Paragraph(raw_text="The term of the agreement is 1 year from the Effective Date...", sentences=[Sentence(raw_text="The term of the agreement is 1 year from the Effective Date...")])
p4 = Paragraph(raw_text="The Supplier shall provide consultancy services as described in Annex 2...", sentences=[Sentence(raw_text="The Supplier shall provide consultancy services as described in Annex 2...")])
p5 = Paragraph(raw_text="The Customer shall pay the Supplier within 30 calendar days of receiving an invoice...", sentences=[Sentence(raw_text="The Customer shall pay the Supplier within 30 calendar days of receiving an invoice...")])
p6 = Paragraph(raw_text="The purple elephant danced gracefully on the moon while eating ice cream.", sentences=[Sentence(raw_text="The purple elephant danced gracefully on the moon while eating ice cream.")])
p7 = Paragraph(raw_text="Time-traveling dinosaurs will review all deliverables before acceptance.", sentences=[Sentence(raw_text="Time-traveling dinosaurs will review all deliverables before acceptance.")])
p8 = Paragraph(raw_text="This agreement is governed by the laws of Norway...", sentences=[Sentence(raw_text="This agreement is governed by the laws of Norway...")])

doc = Document(paragraphs=[p1, p2, p3, p4, p5, p6, p7, p8])

# Attach a document-level concept with sentence-level references
doc.concepts = [
    StringConcept(
        name="Anomalies",
        description="Anomalies in the document",
        add_references=True,
        reference_depth="sentences", # This is now safe as we provided pre-segmented sentences
        add_justifications=True,
        justification_depth="brief",
    )
]

# Define an LLM for extracting information
llm = DocumentLLM(
    model="rwth_gpt/gpt-oss-120b",
    api_key=os.environ.get("RWTH_GPT_API_KEY"),
)

# Extract information from the document
print('Extracting Documents with manual sentence segmentation...')
doc = llm.extract_all(doc)

# Access extracted information
anomalies_concept = doc.concepts[0]
for item in anomalies_concept.extracted_items:
    print("Anomaly:")
    print(f"  {item.value}")
    print("Reference sentences:")
    for s in item.reference_sentences:
        print(f"  - {s.raw_text}")
    print()

import sys
import os
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from schema_extraction.pipeline.phase1_extract import run_phase1
from schema_extraction.pipeline.phase3_versioning import run_phase3
from schema_extraction.pipeline.phase4_formalize import run_phase4
from schema_extraction.pipeline.phase5_bridge import run_phase5

def run_batch():
    issue_numbers = [8261, 5371]
    
    print("--- Starting Phase 1: Extraction ---")
    for num in issue_numbers:
        run_phase1(issue_number=num)
    
    print("\n--- Starting Phase 3: Versioning ---")
    run_phase3()
    
    print("\n--- Starting Phase 4: Formalization ---")
    run_phase4()
    
    print("\n--- Starting Phase 5: Ontology Bridge ---")
    run_phase5()
    
    print("\n--- Batch Pipeline Complete ---")

if __name__ == "__main__":
    run_batch()

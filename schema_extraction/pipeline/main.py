import argparse
from .phase1_extract import run_phase1
# Phase 2 (Classification) has been eliminated to simplify the pipeline.
from .phase3_versioning import run_phase3
from .phase4_formalize import run_phase4
from .phase5_bridge import run_phase5

def main():
    parser = argparse.ArgumentParser(description="Run the GitHub Extraction Pipeline")
    parser.add_argument("--phase", type=int, choices=[1, 3, 4, 5], help="Run a specific phase (1, 3, 4, or 5)")
    parser.add_argument("--limit", type=int, default=10, help="Limit number of issues to fetch in Phase 1 (default: 10, use 0 for no limit)")
    parser.add_argument("--number", type=int, help="Fetch a specific issue/PR number in Phase 1")
    args = parser.parse_args()

    if args.phase:
        if args.phase == 1:
            print("--- Running Phase 1: Raw Extraction ---")
            run_phase1(limit=args.limit, issue_number=args.number)
        elif args.phase == 3:
            print("--- Running Phase 3: Versioned State Reconstruction ---")
            run_phase3()
        elif args.phase == 4:
            print("--- Running Phase 4: Schema-Aligned Formalization ---")
            run_phase4()
        elif args.phase == 5:
            print("--- Running Phase 5: Ontology Bridge Mapping ---")
            run_phase5()
    else:
        print("--- Running Full 4-Phase Pipeline ---")
        print("\n--- Phase 1: Raw Extraction ---")
        run_phase1(limit=args.limit, issue_number=args.number)
        print("\n--- Phase 3: Versioned State Reconstruction ---")
        run_phase3()
        print("\n--- Phase 4: Schema-Aligned Formalization ---")
        run_phase4()
        print("\n--- Phase 5: Ontology Bridge Mapping ---")
        run_phase5()

if __name__ == "__main__":
    main()

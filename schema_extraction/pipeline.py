import subprocess
import sys
from pathlib import Path

def run_script(script_name):
    print(f"\n>>> Running {script_name}...")
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f">>> {script_name} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f">>> Error running {script_name}: {e}")
        sys.exit(1)

def main():
    base_dir = Path("/home/elson/Files/Automated_Ontology/schema_extraction")
    
    # 1. Fetch issues from GitHub
    run_script(str(base_dir / "get_issues.py"))
    
    # 2. Extract concepts from issues
    run_script(str(base_dir / "extract_issues.py"))
    
    # 3. Classify issues into MLOps stages
    run_script(str(base_dir / "classify_issues.py"))
    
    print("\nPipeline execution finished.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
OntoCast Master Pipeline Orchestrator
Usage:
  python3 run_pipeline.py -i input/MLOPS -p prompts/mlops.txt -d https://example.com/mlops
"""

import argparse
import os
import subprocess
import pathlib
import sys
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='\033[1;34m[PIPELINE]\033[0m %(message)s')
logger = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(description="OntoCast Master Pipeline Orchestrator")
    parser.add_argument("-i", "--input", required=True, help="Path to input directory containing PDFs")
    parser.add_argument("-p", "--prompt", default="", help="Path to custom instruction file (.txt)")
    parser.add_argument("-d", "--domain", help="Current domain namespace (e.g. https://example.com/domain)")
    parser.add_argument("-n", "--dataset", default="default_project", help="Dataset identifier for Fuseki/Versioning")
    parser.add_argument("-m", "--mode", choices=["owl2", "rdf-star"], default="owl2", help="Provenance mode")
    parser.add_argument("-e", "--env-file", default=".env.test", help="Path to environment file")
    parser.add_argument("--clear-cache", action="store_true", help="Clear the .cache directory before starting")

    return parser.parse_args()

def run_step(name, command, cwd=None, env=None):
    logger.info(f"Starting Step: {name}...")
    try:
        # We use shell=True to allow for sourcing if needed, but here we just run the CLI
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output
        for line in process.stdout:
            print(f"  \033[90m{line.strip()}\033[0m")
            
        process.wait()
        if process.returncode != 0:
            logger.error(f"Step '{name}' failed with exit code {process.returncode}")
            return False
        logger.info(f"âœ… Step '{name}' completed successfully.")
        return True
    except Exception as e:
        logger.error(f"Error executing step '{name}': {e}")
        return False

def find_latest_ontology(workspace_dir):
    """Find the most recently modified .ttl file starting with 'ontology_'."""
    workspace_path = pathlib.Path(workspace_dir)
    ttl_files = list(workspace_path.glob("ontology_*.ttl"))
    if not ttl_files:
        return None
    # Sort by modification time
    ttl_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return ttl_files[0]

def main():
    args = parse_args()
    project_root = pathlib.Path(__file__).parent.absolute()
    workspace_dir = project_root / "workspace"
    env_file = project_root / args.env_file
    
    # 1. Pre-computation Logic: Dataset and Domain
    logger.info("Initializing context...")
    
    # Resolve paths to absolute to avoid issues with different CWD
    if args.input:
        args.input = str(pathlib.Path(args.input).absolute())
    if args.prompt:
        args.prompt = str(pathlib.Path(args.prompt).absolute())
    
    # Environment Setup
    current_env = os.environ.copy()
    
    # Load .env.test into current_env
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    current_env[key] = value

    current_env["FUSEKI_DATASET"] = args.dataset
    if args.domain:
        current_env["CURRENT_DOMAIN"] = args.domain
    elif "CURRENT_DOMAIN" not in current_env:
        current_env["CURRENT_DOMAIN"] = "https://example.com/"
    current_env["PROVENANCE_MODE"] = args.mode
    
    # 2. Cache Management
    if args.clear_cache:
        cache_dir = project_root / "cache"
        if cache_dir.exists():
            logger.info(f"Clearing cache directory: {cache_dir}")
            subprocess.run(f"rm -rf {cache_dir}", shell=True)

    # 3. Execution Pass
    # Resolve the ontocast binary path
    ontocast_bin = "ontocast"
    possible_venv_bin = project_root.parent / ".venv" / "bin" / "ontocast"
    if possible_venv_bin.exists():
        ontocast_bin = str(possible_venv_bin)
        logger.info(f"Using ontocast binary from venv: {ontocast_bin}")
    
    if args.prompt:
        ontocast_cmd = f"{ontocast_bin} --env-file {env_file} --input-path {args.input} --instruction-file {args.prompt} --provenance-mode {args.mode}"
    else:
        ontocast_cmd = f"{ontocast_bin} --env-file {env_file} --input-path {args.input} --provenance-mode {args.mode}"

    
    success = run_step("Ontology Extraction", ontocast_cmd, cwd=project_root, env=current_env)
    
    if not success:
        sys.exit(1)

    # 4. Identify Output
    latest_ttl = find_latest_ontology(workspace_dir)
    if not latest_ttl:
        logger.error("Could not find any generated ontology in the workspace.")
        sys.exit(1)
        
    logger.info(f"Identified latest artifact: {latest_ttl.name}")

    # 5. Validation Pass
    python_bin = sys.executable
    possible_venv_python = project_root.parent / ".venv" / "bin" / "python3"
    if possible_venv_python.exists():
        python_bin = str(possible_venv_python)
        logger.info(f"Using python binary from venv for validation: {python_bin}")

    validation_cmd = f"{python_bin} test_output_ontology.py {latest_ttl}"
    success = run_step("Automated Validation", validation_cmd, cwd=project_root)

    
    if success:
        logger.info("\n" + "="*50)
        logger.info("ðŸŽ‰ PIPELINE SUCCESS")
        logger.info(f"Domain: {args.domain}")
        logger.info(f"Artifact: {latest_ttl}")
        logger.info("="*50)
    else:
        logger.warning("\n" + "="*50)
        logger.info("âš  PIPELINE FINISHED WITH VALIDATION WARNINGS")
        logger.info(f"Artifact: {latest_ttl}")
        logger.info("="*50)

if __name__ == "__main__":
    main()

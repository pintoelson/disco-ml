# GitHub Architectural Decision Extraction Pipeline

This document provides a comprehensive overview of the automated pipeline designed to extract, classify, and formalize Architectural Design Decisions (ADDs) from GitHub repositories. 

The pipeline is organized into four distinct sequential phases, residing within the `schema_extraction/pipeline/` package.

---

## 1. System Overview and Architecture

The primary goal of this system is to trace how technical decisions evolve over time in open-source repositories. It takes raw GitHub interactions (Issues, Pull Requests, Discussions) and decomposes them into a series of **Versioned Decision Artifacts** based on a predefined schema.

### Core Technologies
- **Python / Pydantic**: For strict data validation and state management between phases.
- **LiteLLM**: Used for raw comment intent classification using models like `rwth_gpt/gpt-oss-120b`.
- **ContextGem**: A specialized LLM-wrapper used to precisely extract complex, nested JSON schemas from large textual contexts.

### Directory Structure
```text
schema_extraction/
├── config.yaml                  # Target repositories and extraction schema definition
├── pipeline/
│   ├── main.py                  # CLI Orchestrator
│   ├── models.py                # Pydantic schemas (GitHubItem, VersionedItem, etc.)
│   ├── phase1_extract.py        # Raw data fetching
│   ├── phase2_classify.py       # Semantic intent classification
│   ├── phase3_versioning.py     # Temporal state reconstruction
│   ├── phase4_formalize.py      # Final schema extraction
│   └── data/                    # Artifact storage directory
│       ├── raw/                 # Phase 1 Outputs
│       ├── classified/          # Phase 2 Outputs
│       ├── versioned/           # Phase 3 Outputs
│       └── formalized/          # Phase 4 Outputs
```

---

## 2. Pipeline Phases

### Phase 1: Raw Extraction (`phase1_extract.py`)
This phase connects to the GitHub REST and GraphQL APIs to pull repository data.
- **Target**: Repositories defined in `config.yaml` (e.g., `Project-MONAI/MONAI`).
- **Process**: It fetches Issues, PRs, and Discussions (with pagination) and subsequently pulls all associated comments for each item. It skips items that have already been downloaded to ensure robustness during long-running extractions.
- **Output**: Strict JSON instances of the `GitHubItem` Pydantic model saved to `data/raw/`.

### Phase 2: Argumentation Classification (`phase2_classify.py`)
This phase evaluates the semantic intent behind every individual comment within an issue/PR.
- **Process**: Using `litellm` and the model `rwth_gpt/gpt-oss-120b`, each comment is evaluated independently.
- **Categories**: 
  - `Pro`: Supports a proposed decision/approach.
  - `Con`: Opposes an approach or highlights constraints.
  - `Neutral`: Asks for clarification or provides factual data without a stance.
  - `NA`: Social discourse ("LGTM", "Thanks", CI/CD bot updates).
- **Output**: Updated `GitHubItem` JSONs with the `classification` and `justification` appended to every comment, saved to `data/classified/`.

### Phase 3: Versioned State Reconstruction (`phase3_versioning.py`)
This phase reconstructs the exact state of knowledge at specific points in time to capture the evolution of the rationale.
- **`v1` (Base State)**: For every issue, an initial `v1` state is created. This state contains *only* the original issue body. Crucially, the Author and Timestamp metadata of the original issue are explicitly injected into the text header so downstream extraction models capture them accurately.
- **Subsequent States (`v2`, `v3`, etc.)**: The script iterates through the comments chronologically. Every time it encounters a relevant classified comment (`Pro`, `Con`, or `Neutral`), it snapshots the state. This snapshot includes the original issue body plus all comments made up to that specific timestamp.
- **Output**: Isolated `VersionedItem` JSONs saved to `data/versioned/`.

### Phase 4: Schema-Aligned Formalization (`phase4_formalize.py`)
This phase uses the `ContextGem` library to perform heavy semantic extraction.
- **Process**: It loads the complex `extraction_schema` from `config.yaml` (which demands fields like *Issue*, *Decision*, *Rationale*, *Description*, and an array of *Argument* objects). 
- **Execution**: The textual state of each Versioned Item is fed into ContextGem. Because Phase 3 explicitly tagged the comments in the text prompt (e.g., `### Comment by {Author} at {Time} (Classification: Pro)`), ContextGem accurately pulls the `classification` tag into the final JSON array.
- **Output**: The finalized Architectural Design Decision JSONs, representing specific temporal iterations, saved to `data/formalized/`.

---

## 3. Running the Pipeline

The pipeline is orchestrated via the `main.py` CLI script. Because large repositories contain thousands of issues, the pipeline can be run safely in the background.

**Run a specific limit (Testing)**
```bash
../.venv/bin/python -m pipeline.main --limit 10
```

**Run the full repository**
Passing `--limit 0` removes the limit, engaging the API pagination loop until the entire repository is fetched.
```bash
nohup ../.venv/bin/python -m pipeline.main --limit 0 > pipeline.log 2>&1 &
```

**Run Individual Phases**
Useful for debugging or re-running a specific step without re-fetching data:
```bash
../.venv/bin/python -m pipeline.main --phase 3
```

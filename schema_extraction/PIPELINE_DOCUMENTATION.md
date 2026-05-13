# GitHub Architectural Decision Extraction Pipeline

This document provides a comprehensive overview of the automated pipeline designed to extract and version Architectural Design Decisions (ADDs) from GitHub repositories.

The pipeline is organized into **four distinct sequential phases**, following a streamlined "Extract -> Version -> Formalize -> Bridge" architecture.

---

## 1. System Overview and Architecture

The primary goal of this system is to trace how technical decisions evolve over time in open-source repositories. It processes raw GitHub interactions (Issues, Pull Requests) and decomposes them into a series of **Versioned Decision Artifacts** based on a predefined schema, enriched with MLOps lifecycle context.

### Core Technologies
- **Python / Pydantic**: For strict data validation and state management between phases.
- **LiteLLM / ContextGem**: Used for robust extraction and mapping using models like `rwth_gpt/mistralai-mistral-small-4-119b`.
- **Incremental Formalization**: A design pattern where the system carries forward previous findings and only extracts new info from discussion deltas.

### Directory Structure
```text
schema_extraction/
├── config.yaml                  # Target repositories, model config, and schema definition
├── PIPELINE_DOCUMENTATION.md    # This file
├── pipeline/
│   ├── main.py                  # CLI Orchestrator
│   ├── models.py                # Pydantic schemas (GitHubItem, VersionedItem, etc.)
│   ├── phase1_extract.py        # Phase 1: Raw data fetching
│   ├── phase3_versioning.py     # Phase 2: Temporal state reconstruction (Delta-based)
│   ├── phase4_formalize.py      # Phase 3: Final schema extraction (Informed Incremental)
│   ├── phase5_bridge.py         # Phase 4: Ontology mapping and asset extraction
│   ├── validate_incremental.py  # Human-readable validation tool
│   └── data/                    # Artifact storage directory
│       ├── raw/                 # Phase 1 Outputs
│       ├── versioned/           # Phase 2 Outputs (Deltas)
│       ├── formalized/          # Phase 3 Outputs (Cumulative)
│       └── bridged/             # Phase 4 Outputs (Enriched)
```

---

## 2. Pipeline Phases

### Phase 1: Raw Extraction (`phase1_extract.py`)
Fetches repository data via GitHub APIs.
- **Process**: Fetches Issues and PRs (with pagination) and all associated comments.
- **Key Feature**: Supports fetching a specific issue/PR using the `--number` flag for targeted analysis.
- **Output**: JSON instances of the `GitHubItem` model in `data/raw/`.

### Phase 2: Delta-Based Versioning (`phase3_versioning.py`)
Reconstructs the timeline of the decision by treating every comment as a versioned delta.
- **No Discarding**: Unlike previous versions, NO comments are discarded at this stage. Every interaction is preserved for analysis in the formalization phase.
- **`v1` (Base State)**: Contains the original issue body and metadata.
- **Deltas (`v2+`)**: For each comment, a new version is created containing **only** that specific comment's text and metadata.
- **Output**: `VersionedItem` JSONs in `data/versioned/`.

### Phase 4: Formalization (Engine: ContextGem)
The formalization phase transforms versioned deltas into structured architectural decision records.
- **Detailed Docs**: [PHASE4_DETAIL.md](PHASE4_DETAIL.md)

### Phase 5: Ontology Bridge (`phase5_bridge.py`)
Bridges the technical decisions to the MLOps ontology by extracting lifecycle stages, assets, and author roles.
- **Detailed Docs**: [PHASE5_DETAIL.md](PHASE5_DETAIL.md)
- **Multi-Context**: Analyzes both the Phase 4 formalized JSON and the Phase 3 raw text fragment.
- **Asset Tracking**: Extracts name, type (Dataset, Model, etc.), and link for any discussed ML assets.
- **Role Identification**: Classifies authors into roles like "Data Scientist" or "ML Engineer".
- **Output**: Enriched `BridgedDecision` JSONs in `data/bridged/`.

---

## 3. Design Decisions & Rationale

| Decision | Rationale |
| :--- | :--- |
| **Phase 2 Elimination** | Removing the early classification phase prevents data loss. We process all comments as potential evidence, letting the more context-aware Phase 3 decide on relevance and stance. |
| **Delta Storage** | Storing only the "new" fragment in each version file focuses the LLM intensely on the latest evidence without being overwhelmed by history. |
| **Informed Context** | Prepending the previous state allows the LLM to understand what a "Pro" or "Con" argument is relative to. |
| **Direct LiteLLM Usage** | Moved from specialized wrappers to direct LiteLLM calls for Phase 4 to improve reliability and support standard JSON mode/prompting across different providers. |
| **Metadata Removal** | Removed all lifecycle and MLOps-specific metadata from the models to simplify the extraction schema and focus purely on architectural design decisions. |

---

## 4. Running and Validating

**Run full pipeline for a specific item:**
```bash
./.venv/bin/python3 -m schema_extraction.pipeline.main --number 8261
```

**Validate and View Progress:**
The `validate_incremental.py` script provides a human-readable diff of how the decision evolved:
```bash
./.venv/bin/python3 -m schema_extraction.pipeline.validate_incremental
```

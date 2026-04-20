# OntoCast Codebase Patch Explanation

This document explains the technical modifications applied to the `ontocast` package (installed in `.venv`) and the rationale behind each change to support high-precision MLOps ontology extraction.

## 1. Model Validation & Compatibility
**File**: `ontocast/config.py`
- **Change**: Added `GPT_OSS_120B`, `MIXTRAL_8X22B`, `MISTRAL_SMALL_3_2_24B`, `E5_MISTRAL_7B`, and `QWEN3_EMBEDDING_8B` to the `OpenAIModel` enum.
- **Rationale**: The user is using various custom/fine-tuned models through their API provider that were not recognized by the original Pydantic validation schema, causing `ValidationError`.

## 2. Prompt Template Fix
**File**: `ontocast/prompt/render_ontology.py`
- **Change**: Escaped the `{prefix_instruction}` placeholder using double braces `{{ }}` in the f-string template.
- **Rationale**: The template was attempting to interpolate the `prefix_instruction` too early, before the actual instruction was ready, leading to a `KeyError`.

## 3. Parallel Processing (Multiprocessing)
**File**: `ontocast/onto/rdfgraph.py`
- **Change**: 
    - Implemented a custom `__deepcopy__` for the `RDFGraph` class.
    - Optimized the `copy()` method to use native `pyoxigraph` quad iteration instead of `rdflib` triple extraction.
- **Rationale**: `RDFGraph` uses `pyoxigraph` as a back-end, which is not picklable. This caused crashes in the parallel pipelines (`asyncio.gather` with multiprocessing workers). The custom copy logic ensures safe cloning across worker boundaries.

## 4. RDF-Star Hashing Stability
**File**: `ontocast/onto/ontology.py`
- **Change**: Patched `_compute_and_set_hash` to filter out RDF-star triple terms (`<< >>`) before the hashing process.
- **Rationale**: `rdflib`'s default JSON-LD and N-Quads serializers (used for canonical hashing) do not yet support RDF-star triple terms natively. Including them caused a `TypeError` during ontology versioning/hashing.

## 5. Domain-Specific Instruction Injection
**File**: `ontocast/cli/serve.py`
- **Change**: Added the `--instruction-file` CLI argument and passed its content to the `AgentState`.
- **Rationale**: This allows users to inject large, domain-specific instruction payloads (like the 500-word `prompt.txt`) directly into the LLM's system prompt without modifying the core source code.

## 6. OWL 2 (Standard RDF 1.1) Output Support
**Multiple Files**: `enum.py`, `state.py`, `config.py`, `serve.py`, `rewriter.py`, `node_factories.py`, `normalize_ontology.py`.
- **Change**: 
    - Added `ProvenanceMode` (rdf-star vs owl2).
    - Propagated this mode through the entire state graph.
    - Updated `Rewriter._add_reified_provenance` to skip RDF-star reification when `owl2` is selected.
- **Rationale**: Many standard OWL 2 tools (like Protégé HermiT) do not yet support RDF-star. This toggle allows users to generate "clean" OWL files for traditional semantic reasoning while retaining RDF-star support for internal provenance tracking if needed.

---
**Note**: All changes are applied to the local installation in `.venv/lib/python3.12/site-packages/ontocast/`.

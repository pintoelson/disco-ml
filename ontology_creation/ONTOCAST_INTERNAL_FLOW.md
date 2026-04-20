# OntoCast Architecture & Integration Guide

This document explains the internal logic of the OntoCast pipeline, including the specific patches made to support specialized domains (MLOps, ADR) and standards-compliant outputs (OWL 2).

---

## 1. Core Workflow: The "How" and "Why"

OntoCast is designed as a **Stateful Graph Agent**. It doesn't just "summarize"; it attempts to model the semantic structure of a document as a formal knowledge graph.

### Step 1: Document Decomposition (Chunking)
- **What:** The pipeline splits PDFs into discrete **Content Units**.
- **The Strategy:** It uses **Token-aware Sliding Windows** with a configured overlap (typically 10-15%).
- **Why:** Full-text processing exceeds LLM limits. Sliding windows ensure that relationships spanning across two chunks (e.g., a subject in paragraph A and its predicate in paragraph B) are not lost, maintaining semantic continuity.

### Step 2: Agentic Extraction (The "Brain")
- **How:** For each unit, the agent performs a specialized extraction pass.
- **CHANGE (Custom Instructions):** We added the `--instruction-file` flag. This allows you to bypass the generic extraction and force the LLM to look for specific primitives:
    - **MLOps:** Models, Pipelines, Training Runs.
    - **Architecture:** Decisions, Rationale, Trade-offs.
- **Why:** This ensures the resulting graph is "Grounded" in your specific domain vocabulary.

### Step 3: Global Aggregation & Consolidation
- **How:** The **Aggregator (Rewriter)** performs a multi-phase merge:
    1. **Triple Verification:** Checks every salvaged triple against the base schema.
    2. **Canonicalization:** Resolves synonyms (e.g., merging "ML Pipeline" and "Machine Learning Pipeline" into a single URI if the LLM identifies them as identical).
    3. **Conflict Resolution:** If units provide contradictory axioms (e.g., different parent classes), the Rewriter uses a "Consolidation Pass" where an LLM agent reviews the conflicting graph segments to pick the most logically sound structure.
- **CHANGE (OWL 2 Provenance):** By default, OntoCast uses RDF-star (reified triples) for unit tracing. We added the `PROVENANCE_MODE=owl2` toggle to strip metadata and ensure compatibility with standard tools like **Protégé** and **HermiT**.

---

## 2. Fresh vs. Updated Ontologies

The system uses a **"Seed & Grow"** strategy managed via the `ONTOCAST_ONTOLOGY_DIRECTORY`.

### Fresh Ontologies (The Scratch Run)
- **Flow:** `Input -> [No Seed Found] -> Extraction -> v1.0.0`
- **Logic:** If the seeding directory is empty, the system performs a "Discovery" pass. It identifies the core classes from the text and assigns them a new Namespace based on your `CURRENT_DOMAIN` and the first meaningful ID it encounters (e.g., `addo` or `aepo`).
- **CHANGE (Custom Domain):** We enabled `CURRENT_DOMAIN` configuration in [.env.test](file:///home/elson/Files/Automated_Ontology/test_ontocast/.env.test). This ensures that even a fresh run is correctly branded under your own URI (e.g., `https://example.com/mlops/`).

### Updated Ontologies (Incremental Growth)
- **Flow:** `Input + [v1.0.1 Seed] -> Context Injection -> Delta Extraction -> v1.0.2`
- **Logic:** 
    1. The system loads existing [.ttl](file:///home/elson/Files/Automated_Ontology/test_ontocast/constraints.shacl.ttl) files from the `ONTOCAST_ONTOLOGY_DIRECTORY`.
    2. **Multiple File Handling:** If multiple files exist, OntoCast uses **Semantic Version Discovery**. It parses the `vX.X.X` suffix in filenames and selects the highest version matching your target "Ontology ID" (e.g., `addo`).
    3. It injects this "Base Knowledge" into the LLM's prompt.
    4. The LLM is instructed: *"Use these existing classes. Do not create duplicates. Only add what is missing or more specific."*
    5. The **Rewriter** merges new findings and saves the incremented version.

---

## 3. Key System Patches (Summary of Changes)

| Component | Change Type | Purpose |
| :--- | :--- | :--- |
| [ontocast/cli/serve.py](file:///home/elson/Files/Automated_Ontology/.venv/lib/python3.12/site-packages/ontocast/cli/serve.py) | **FEATURE** | Added `--instruction-file` and `--provenance-mode` to allow CLI-level control over the LLM's goal and the RDF output format. |
| [ontocast/config.py](file:///home/elson/Files/Automated_Ontology/.venv/lib/python3.12/site-packages/ontocast/config.py) | **COMPATIBILITY** | Patched the [OpenAIModel](file:///home/elson/Files/Automated_Ontology/.venv/lib/python3.12/site-packages/ontocast/config.py#29-47) enum to support `mistralai-mistral-small-4-119b`, allowing use of your specialized local/private LLM providers. |
| [ontocast/tool/agg/rewriter.py](file:///home/elson/Files/Automated_Ontology/.venv/lib/python3.12/site-packages/ontocast/tool/agg/rewriter.py) | **LOGIC** | Modified the graph merger to respect the `owl2` mode, preventing the generation of triple-terms that break standard OWL parsers. |
| [test_ontocast/.env.test](file:///home/elson/Files/Automated_Ontology/test_ontocast/.env.test) | **OPERATIONAL** | Configured `CURRENT_DOMAIN` as a global variable to ensure all URIs match your organization's naming scheme. |

---

## 4. Troubleshooting & FAQ

**Q: Why do I see "Bad syntax (objectList expected)" in the logs?**
- **A:** This happens when the LLM tries to use advanced OWL 2 axioms (like `TransitiveProperty`) incorrectly in the Turtle format. The OntoCast agent detects this and performs a **Salvage Operation**, rescuing the valid architectural links while discarding the broken syntax.

**Q: Where is my data actually stored?**
- **A:** 
    - `workspace/`: Temporal drafts and intermediate artifacts.
    - [ontologies/](file:///home/elson/Files/Automated_Ontology/.venv/lib/python3.12/site-packages/ontocast/tool/ontology_manager.py#423-462): The "Stable Library". Move files here to use them as seeds for the next run.
    - `cache/`: Token-level LLM cache (managed via `DiskCache`) to prevent re-extracting the same chunks.

**Q: How do I change the name of the ontology?**
- **A:** The system identifies the base ID (like `mlopsc` or `addo`) from the text. If you want a specific name, mention it prominently in your `--instruction-file`.

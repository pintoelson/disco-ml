# 🏗️ OntoCast: Professional Usage Guide

This guide provides a streamlined workflow for extracting high-fidelity ontologies from technical literature.

---

## 🚀 Quick Start (The "One-Liner")

To process a directory of PDFs into a clean, OWL 2 compliant ontology:

```bash
ontocast --env-file .env.test \
  --input-path ./input/MLOPS \
  --instruction-file prompts/mlops.txt \
  --provenance-mode owl2
```

---

## 📁 Workspace Layout

| Directory | Purpose | Retention |
| :--- | :--- | :--- |
| `input/` | Source PDFs (grouped by domain) | User Managed |
| `workspace/` | Ephemeral drafts (`v1.0.x`) and temporary triples | Cleanup regularly |
| `ontologies/` | **Source of Truth**. Move verified `.ttl` files here to use as Seeds. | **Permanent** |
| `cache/` | Token-level LLM responses & PDF fragments | Keeps costs low |

---

## 🔄 Primary Workflows

### 1. Fresh Run (Discovery)
Use this when starting a new domain (e.g., first time reading MLOps papers).
- **Setup:** Ensure `ONTOCAST_ONTOLOGY_DIRECTORY` is empty or points to a new folder.
- **Action:** Point `--input-path` to the new PDF folder.
- **Output:** Generates `version 1.0.0` or `1.0.1`.

### 2. Incremental Update (Evolution)
Use this to grow your ontology with new papers.
- **Setup:** Place your previous "Base" ontology in the `ontologies/` folder.
- **Action:** Run the command with the new PDFs in the input path.
- **Output:** Version bumps (e.g., `1.0.1` -> `1.0.2`), merging new concepts into the base.

---

## ⚙️ Key Configuration (.env.test)

> [!IMPORTANT]
> Always verify these tokens before running to avoid namespace pollution.

- `CURRENT_DOMAIN`: Your root URI (e.g., `https://example.com/mlops/core`).
- `PROVENANCE_MODE`: Set to `owl2` for Protégé/Reasoner compatibility.
- `RENDER_MODE`: Set to `ontology` to skip fact extraction and save tokens.

---

## 🛡️ Best Practices for Error-Free Output

### 1. Instruction Discipline
Do not list every class you want in the `--instruction-file`. Instead, describe the **goals**.
- **Bad:** "Extract classes: Model, Dataset, Pipeline."
- **Good:** "Focus on the MLOps lifecycle activities and the artifacts produced at each stage (Data, Training, Deployment)."

### 2. Namespace Hygiene
Always update `CURRENT_DOMAIN` when switching domains (e.g., from `architecture/decisions` to `mlops/pipeline`). Mixing domains in one extraction leads to fragmented URIs.

### 3. Version Control Strategy
- **DO NOT** track `workspace/` or `cache/` in Git (too large).
- **DO track** the `ontologies/` folder and your `prompts/` library. This allows you to roll back if an extraction goes "off the rails."

### 4. Validation First
After every extraction, run the automated validation script:
```bash
python3 test_output_ontology.py workspace/ontology_rmops_1.0.1.ttl
```
If it reports `Syntactic Error`, the agent will usually fix it in the next "Actionable Logic" pass, but manual inspection in Protégé is recommended for `v1.0.0` releases.

### 5. Seeding for Consistency
If the LLM starts hallucinating new names for existing concepts, increase the `context` by explicitly placing a manual "Schema Definition" file in the `ontologies/` folder before running.

You are in PLAN mode.

IMPORTANT:
- Do NOT use or mention any tools
- Do NOT attempt to write files
- Do NOT mention next steps or task completion
- Output plain structured text only


I am building a frontend-only prototype for a research thesis tool.
The goal is rapid iteration and visual believability, not production readiness.

### Context
The tool is a Jira-like system where each “ticket” represents a decision.
Each ticket contains a decision knowledge graph (KG) that evolves over time.

Each ticket:
- Looks like a structured decision table (similar to Jira / ADRs)
- Has multiple versions (V1 → V2 → V3), representing decision evolution
- Each version corresponds to a different knowledge graph

The frontend must:
- Display a list of decision tickets
- Allow selecting a ticket
- Show ticket metadata in a table-like layout
- Show a version timeline (decision evolution)
- Visualize the knowledge graph for the selected version

### Knowledge Graph Concept
The knowledge graph contains:
- Nodes:
  - Decision
  - Argument
  - Agent (person/system)
  - Artifact (dataset, model, document)
- Edges:
  - supports
  - opposes
  - createdBy
  - usesArtifact
  - evolvesTo (between versions, not inside a graph)

Graph visualization is for understanding and explanation, not correctness.

### Important Constraints
- FRONTEND ONLY (no backend, no GraphDB, no SPARQL)
- Use mocked / hardcoded data
- React-based architecture
- Focus on layout, components, and interaction flow
- Visual clarity > technical correctness
- This is for screenshots, demos, and thesis figures

### Existing Context
I already have:
- A decision ticket represented as a table (fields like decision, rationale, arguments, owner, status)
- This table should conceptually map to the knowledge graph visualization

### What I want from you (PLAN ONLY)
1. Propose a clear frontend component hierarchy
2. Propose page layout(s) (Dashboard, Ticket view, etc.)
3. Define responsibilities of each component
4. Suggest how mocked data should be structured
5. Explain how the decision table maps to graph nodes and edges
6. Identify which components are “core” vs “nice to have”
7. Propose an iteration plan (v0 → v1 → v2)

Do NOT:
- Generate code
- Choose backend technologies
- Optimize performance
- Over-engineer state management

Your output should be a structured plan using:
- Headings
- Bullet points
- Clear component names

Assume this plan will be used to guide rapid vibe-coding iterations.

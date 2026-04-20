# DISCO-ML: Decision Knowledge Graph Explorer

## Tool Description

DISCO-ML is a frontend-only prototype for a research thesis tool that visualizes decision tickets as evolving knowledge graphs. It's designed for screenshots, demos, and thesis figures rather than production use.

### Core Concept

The tool is a Jira-like system where each "ticket" represents a decision. Each ticket contains a decision knowledge graph that evolves over time through multiple versions (V1 → V2 → V3). Each version corresponds to a different knowledge graph state.

### Key Features

1. **Decision Tickets** - Structured decision records similar to ADRs (Architecture Decision Records)
   - Each ticket has metadata: title, status, owner, tags, creation/update dates
   - Tickets belong to buckets (Model Training, Model Evaluation, Model Deployment)

2. **Version Timeline** - Decision evolution tracking
   - Multiple versions per ticket showing how decisions changed over time
   - Parent-child relationships between versions (evolvesTo)

3. **Knowledge Graph Visualization** - Visual representation of decision components
   - Nodes: Decision, Argument, Agent, Artifact
   - Edges: supports, opposes, createdBy, usesArtifact, evolvesTo

4. **Three Main Views**
   - Dashboard: Kanban-style bucket view
   - Timeline: Reverse chronological list with expandable version history
   - Graph: Statistics and combined graph view

---

## Feature Table

| Feature Name | Feature Description | Accountable Agent | Date | Notes | Affected Files |
|-------------|---------------------|------------------|------|-------|----------------|
| Dark/Light Mode Toggle | Theme switcher with Sun/Moon icons in header | MiniMax M2.5 Free  | 12-02-2026 | Persists in localStorage | `components/theme-toggle.tsx`, `components/layout/header.tsx` |
| Dashboard with Buckets | Kanban-style view with 3 columns (Model Training, Model Evaluation, Model Deployment) | MiniMax M2.5 Free  | 12-02-2026 | Drag-and-drop planned for future | `components/dashboard/ticket-grid.tsx` |
| Decision Ticket Cards | Cards showing ticket ID, title, status, rationale snippet, version count, owner. Clicking on a card opens a popup with the ticket details. | MiniMax M2.5 Free & Gemini | 12-02-2026 | Was navigating to a new page, now opens a popup. | `components/dashboard/ticket-grid.tsx` |
| Decision Ticket Popup | A popup that shows all the details of a decision ticket on top of the current view. | Gemini | 12-02-2026 | Includes Overview, Arguments, Artifacts, and Graph View tabs | `components/decision-ticket/ticket-details.tsx`, `components/dashboard/ticket-grid.tsx` |
| Status Filter | Filter dashboard tickets by status (draft/proposed/accepted/rejected/deprecated) | MiniMax M2.5 Free  | 12-02-2026 | Clickable status badges | `components/dashboard/ticket-grid.tsx` |
| Search | Global search across ticket titles, IDs, and tags | MiniMax M2.5 Free  | 12-02-2026 | Filters in real-time | `components/dashboard/ticket-grid.tsx` |
| Version Timeline | Left panel showing all versions as vertical timeline | MiniMax M2.5 Free  | 12-02-2026 | Click to switch version | `components/decision-ticket/ticket-details.tsx` |
| Decision Table | ADR-style display (decision, rationale, context, arguments) | MiniMax M2.5 Free  | 12-02-2026 | Updates based on selected version | `components/decision-ticket/ticket-table.tsx` |
| Arguments Section | Shows supporting and opposing arguments with visual distinction | MiniMax M2.5 Free  | 12-02-2026 | Green for supports, red for opposes | `components/decision-ticket/ticket-details.tsx` |
| Knowledge Graph Panel | React Flow visualization of decision nodes and edges | MiniMax M2.5 Free  | 12-02-2026 | Node types color-coded | `components/graph/knowledge-graph.tsx` |
| Timeline Page | Reverse chronological list of all tickets | MiniMax M2.5 Free  | 12-02-2026 | Sorted by updatedAt | `app/timeline/page.tsx` |
| Expandable Version History | Click to see all versions within a ticket card on Timeline page | MiniMax M2.5 Free  | 12-02-2026 | Current version highlighted | `app/timeline/page.tsx` |
| Graph View | Statistics dashboard showing node counts by type | MiniMax M2.5 Free  | 12-02-2026 | Placeholder for combined graph | `app/graph/page.tsx`, `components/graph/knowledge-graph.tsx` |
| Sidebar Navigation | Persistent sidebar with links to Dashboard, Timeline, Graph | MiniMax M2.5 Free  | 12-02-2026 | Sticky positioning | `components/layout/sidebar.tsx` |
| Dark Mode Support | Comprehensive dark mode styling across all components | MiniMax M2.5 Free  | 12-02-2026 | Uses Tailwind dark: classes | `app/globals.css`, `components/theme-toggle.tsx` |

---

## Technical Stack

- **Framework**: Next.js 16 with React 19
- **Styling**: Tailwind CSS 4 with shadcn components
- **Graph Visualization**: React Flow
- **Icons**: Lucide React
- **Language**: TypeScript

---

## Routes

| Path | Description |
|------|-------------|
| `/` | Dashboard with bucket view |
| `/timeline` | Reverse chronological ticket list |
| `/graph` | Graph statistics view |

---

## Data Structure

### Ticket
- id, title, status, bucket, owner, createdAt, updatedAt, tags, versions[], currentVersionIndex

### Version
- versionId, decision, rationale, context, arguments[], artifacts[], parentVersionId

### Node Types
- Decision (blue), Argument (green/red), Agent (purple), Artifact (orange)

### Edge Types
- supports (green), opposes (red), createdBy, usesArtifact, evolvesTo
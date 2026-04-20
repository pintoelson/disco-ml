export type NodeType = "decision" | "argument" | "agent" | "artifact";
export type EdgeType = "supports" | "opposes" | "neutral" | "createdBy" | "usesArtifact" | "evolvesTo";
export type TicketStatus = "draft" | "proposed" | "accepted" | "rejected" | "deprecated" | "Decided" | "open";
export type TicketBucket = 
  | "ML Project Initiation"
  | "Data Preparation"
  | "Modeling Development"
  | "Model Evaluation"
  | "Model Deployment"
  | "Monitoring & Maintenance"
  | "Miscellaneous"
  | "Uncertain";

export interface Agent {
  id: string;
  name: string;
  role?: string;
  avatarUrl?: string;
}

export interface Artifact {
  id: string;
  name: string;
  type: "dataset" | "model" | "document" | "code";
  url?: string;
}

export interface GraphNode {
  id: string;
  type: NodeType;
  label: string;
  metadata?: Record<string, unknown>;
  versionId?: string;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: EdgeType;
  label?: string;
}

export interface Argument {
  id: string;
  content: string;
  type: "supports" | "opposes" | "neutral";
  author: string;
  createdAt: string;
  timestamp?: string;
  argument?: string; // Original field from JSON
}

export interface TicketVersion {
  versionId: string;
  decision: string;
  rationale: string;
  context: string;
  cost?: string;
  risk?: string;
  arguments: Argument[];
  artifacts: Artifact[];
  parentVersionId: string | null;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface DecisionTicket {
  id: string;
  title: string;          // Mapping for 'Issue'
  decision: string;
  rationale: string;
  status: string;
  description: string;
  timestamp: string;      // Mapping for 'Time stamp'
  cost?: string;
  risk?: string;
  author: string;
  arguments: Argument[];
  
  // Keep these for dashboard compatibility (mapped in sync script)
  bucket: TicketBucket;
  owner: Agent;
  createdAt: string;
  updatedAt: string;
  tags: string[];
  versions: TicketVersion[];
  currentVersionIndex: number;
}

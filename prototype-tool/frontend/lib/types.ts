export type NodeType = "decision" | "argument" | "agent" | "artifact";
export type EdgeType = "supports" | "opposes" | "neutral" | "createdBy" | "usesArtifact" | "evolvesTo";
export type TicketStatus = "draft" | "proposed" | "accepted" | "rejected" | "deprecated" | "Decided" | "open" | "closed";

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
}

export interface TicketVersion {
  versionId: string;
  decision: string;
  rationale: string;
  cost?: string;
  risk?: string;
  context: string;
  timestamp: string;
  arguments: Argument[];
}

export interface DecisionTicket {
  id: string;
  title: string;
  status: string;
  bucket: TicketBucket;
  owner: {
    id: string;
    name: string;
  };
  createdAt: string;
  updatedAt?: string;
  tags?: string[];
  currentVersionIndex: number;
  versions: TicketVersion[];
  
  // Dashboard convenience fields
  decision: string;
  rationale: string;
  cost?: string;
  risk?: string;
  description: string;
  author: string;
  arguments: Argument[];
}

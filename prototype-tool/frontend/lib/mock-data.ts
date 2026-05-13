import { DecisionTicket } from "./types";
import syncedTickets from "./tickets-data.json";

export const mockTickets: DecisionTicket[] = [
  ...syncedTickets as DecisionTicket[],
];

export function generateGraphFromTicket(ticket: DecisionTicket) {
  const version = ticket.versions[ticket.currentVersionIndex];
  const nodes = [];
  const edges = [];

  const decisionNodeId = `decision-${ticket.id}-${version.versionId}`;
  nodes.push({
    id: decisionNodeId,
    type: "decision",
    label: version.decision,
    versionId: version.versionId,
  });

  nodes.push({
    id: ticket.owner.id,
    type: "agent",
    label: ticket.owner.name,
    metadata: { role: ticket.owner.role },
  });
  edges.push({
    id: `edge-owner-${ticket.id}`,
    source: decisionNodeId,
    target: ticket.owner.id,
    type: "createdBy",
  });

  version.arguments.forEach((arg) => {
    const argNodeId = `arg-${arg.id}`;
    nodes.push({
      id: argNodeId,
      type: "argument",
      label: arg.content,
      metadata: { author: arg.author },
    });
    edges.push({
      id: `edge-${arg.id}`,
      source: argNodeId,
      target: decisionNodeId,
      type: arg.type,
    });
  });

  // @ts-ignore - version.artifacts is removed from types but might still be in data
  if (version.artifacts) {
    // @ts-ignore
    version.artifacts.forEach((art) => {
      const artNodeId = `art-${art.id}`;
      nodes.push({
        id: artNodeId,
        type: "artifact",
        label: art.name,
        metadata: { type: art.type },
      });
      edges.push({
        id: `edge-art-${art.id}`,
        source: decisionNodeId,
        target: artNodeId,
        type: "usesArtifact",
      });
    });
  }

  return { nodes, edges };
}

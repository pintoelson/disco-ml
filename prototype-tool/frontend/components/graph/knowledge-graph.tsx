"use client";

import { FC, useCallback, useMemo, useEffect } from "react";
import ReactFlow, {
  Node,
  Edge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  Position,
  Handle,
  NodeProps,
} from "reactflow";
import "reactflow/dist/style.css";
import { GraphNode, GraphEdge, NodeType } from "../../lib/types";
import { generateGraphFromTicket } from "../../lib/mock-data";

const nodeColors: Record<NodeType, { bg: string; border: string }> = {
  decision: { bg: "#3b82f6", border: "#1d4ed8" },
  argument: { bg: "#22c55e", border: "#16a34a" },
  agent: { bg: "#a855f7", border: "#7c3aed" },
  artifact: { bg: "#f97316", border: "#ea580c" },
};

const CustomNode: FC<NodeProps> = ({ data }) => {
  const color = nodeColors[data.nodeType as NodeType] || nodeColors.decision;

  return (
    <div
      className="px-4 py-2 rounded-lg shadow-md border-2 text-white text-sm font-medium min-w-[120px] text-center"
      style={{ backgroundColor: color.bg, borderColor: color.border }}
    >
      <Handle type="target" position={Position.Top} className="w-3 h-3 !bg-white" />
      <div className="capitalize truncate max-w-[150px]">{String(data.label).length > 15 ? String(data.label).slice(0, 15) + "..." : data.label}</div>
      <div className="text-xs opacity-80">{data.sublabel}</div>
      <Handle type="source" position={Position.Bottom} className="w-3 h-3 !bg-white" />
    </div>
  );
};

const nodeTypes = {
  custom: CustomNode,
};

interface KnowledgeGraphProps {
  ticket: DecisionTicket;
  versionIndex: number;
}

const KnowledgeGraph: FC<KnowledgeGraphProps> = ({ ticket, versionIndex }) => {
  const graphData = useMemo(() => 
    generateGraphFromTicket(ticket, versionIndex),
    [ticket, versionIndex]
  );

  const initialNodes: Node[] = useMemo(() => {
    const nodes: Node[] = [];
    let yOffset = 0;

    graphData.nodes.forEach((node, index) => {
      let xOffset = 0;

      if (node.type === "decision") {
        xOffset = 0;
      } else if (node.type === "agent") {
        xOffset = -200;
      } else if (node.type === "artifact") {
        xOffset = 200;
      } else {
        xOffset = (index % 2 === 0 ? 1 : -1) * 150;
      }

      nodes.push({
        id: node.id,
        type: "custom",
        position: { x: 400 + xOffset, y: 100 + yOffset },
        data: {
          label: node.label,
          sublabel: node.type,
          nodeType: node.type,
        },
      });

      if (node.type !== "decision") {
        yOffset += 80;
      }
    });

    return nodes;
  }, [graphData]);

  const initialEdges: Edge[] = useMemo(() => {
    return graphData.edges.map((edge) => {
      let animated = false;
      let strokeWidth = 1.5;

      if (edge.type === "supports" || edge.type === "opposes") {
        strokeWidth = 2;
        animated = true;
      }

      return {
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: "smoothstep",
        animated,
        label: edge.type,
        style: {
          stroke:
            edge.type === "supports"
              ? "#22c55e"
              : edge.type === "opposes"
              ? "#ef4444"
              : "#6b7280",
          strokeWidth,
        },
        labelStyle: {
          fill: "#6b7280",
          fontSize: 10,
        },
      };
    });
  }, [graphData]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // Update nodes and edges when initial data changes (e.g. version slider moved)
  useEffect(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [initialNodes, initialEdges, setNodes, setEdges]);

  const onConnect = useCallback(
    (params: any) => setEdges((eds) => [...eds, params]),
    [setEdges]
  );

  return (
    <div className="w-full h-full min-h-[400px] overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-left"
      >
        <Background color="#e5e7eb" gap={16} className="dark:bg-gray-900" />
        <Controls className="!bg-white dark:!bg-gray-800 !border-gray-200 dark:!border-gray-700" />
        <MiniMap
          className="!bg-white dark:!bg-gray-800"
          nodeColor={(node) => {
            const color = nodeColors[(node.data as any).nodeType as NodeType];
            return color?.bg || "#3b82f6";
          }}
        />
      </ReactFlow>
    </div>
  );
};

export default KnowledgeGraph;

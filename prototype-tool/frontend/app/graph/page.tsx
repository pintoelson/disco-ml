"use client";

import { FC, useMemo } from "react";
import { mockTickets, generateGraphFromTicket } from "../../lib/mock-data";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import {
  Network,
  GitBranch,
  User,
  FileText,
  Database,
  Cpu,
} from "lucide-react";
import { ClientOnly } from "../../components/ui/client-only";

const GraphViewPage: FC = () => {
  const allNodes = useMemo(() => {
    const nodes: ReturnType<typeof generateGraphFromTicket>["nodes"] = [];
    const edges: ReturnType<typeof generateGraphFromTicket>["edges"] = [];

    mockTickets.forEach((ticket) => {
      const { nodes: ticketNodes, edges: ticketEdges } =
        generateGraphFromTicket(ticket);
      nodes.push(...ticketNodes);
      edges.push(...ticketEdges);
    });

    return { nodes, edges };
  }, []);

  const nodeCounts = {
    decision: allNodes.nodes.filter((n) => n.type === "decision").length,
    argument: allNodes.nodes.filter((n) => n.type === "argument").length,
    agent: allNodes.nodes.filter((n) => n.type === "agent").length,
    artifact: allNodes.nodes.filter((n) => n.type === "artifact").length,
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Knowledge Graph</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Unified view of all decision tickets and their relationships
        </p>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <Card className="dark:bg-gray-800 dark:border-gray-700">
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <ClientOnly fallback={<div className="w-5 h-5" />}>
                  <GitBranch className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </ClientOnly>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{nodeCounts.decision}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Decisions</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="dark:bg-gray-800 dark:border-gray-700">
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                <ClientOnly fallback={<div className="w-5 h-5" />}>
                  <Network className="w-5 h-5 text-green-600 dark:text-green-400" />
                </ClientOnly>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{nodeCounts.argument}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Arguments</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="dark:bg-gray-800 dark:border-gray-700">
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                <ClientOnly fallback={<div className="w-5 h-5" />}>
                  <User className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                </ClientOnly>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{nodeCounts.agent}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Agents</p>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card className="dark:bg-gray-800 dark:border-gray-700">
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center">
                <ClientOnly fallback={<div className="w-5 h-5" />}>
                  <FileText className="w-5 h-5 text-orange-600 dark:text-orange-400" />
                </ClientOnly>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{nodeCounts.artifact}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Artifacts</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="dark:bg-gray-800 dark:border-gray-700">
        <CardHeader>
          <CardTitle className="flex items-center justify-between text-gray-900 dark:text-gray-100">
            <span className="flex items-center gap-2">
              <ClientOnly fallback={<div className="w-5 h-5" />}>
                <Network className="w-5 h-5" />
              </ClientOnly>
              Combined Knowledge Graph
            </span>
            <Badge variant="outline" className="dark:border-gray-600 dark:text-gray-400">
              {allNodes.nodes.length} nodes • {allNodes.edges.length} edges
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-5 gap-2 mb-4 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-blue-500" />
              <span className="text-gray-700 dark:text-gray-300">Decision</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-green-500" />
              <span className="text-gray-700 dark:text-gray-300">Argument (Supports)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-red-500" />
              <span className="text-gray-700 dark:text-gray-300">Argument (Opposes)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-purple-500" />
              <span className="text-gray-700 dark:text-gray-300">Agent</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 rounded bg-orange-500" />
              <span className="text-gray-700 dark:text-gray-300">Artifact</span>
            </div>
          </div>

          <div className="border rounded-lg bg-gray-50 dark:bg-gray-900/50 p-8 text-center border-gray-200 dark:border-gray-700">
            <ClientOnly fallback={<div className="w-16 h-16 mx-auto mb-3" />}>
              <Network className="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-3" />
            </ClientOnly>
            <p className="text-gray-500 dark:text-gray-400 mb-2">
              Combined graph visualization of all tickets
            </p>
            <p className="text-sm text-gray-400 dark:text-gray-500">
              Navigate between tickets to see individual graphs
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default GraphViewPage;

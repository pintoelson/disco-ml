"use client";

import { FC, useState, useEffect } from "react";
import { DecisionTicket } from "../../lib/types";
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
} from "lucide-react";
import { ClientOnly } from "../../components/ui/client-only";

const GraphViewPage: FC = () => {
  const [tickets, setTickets] = useState<DecisionTicket[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/v1/tickets`)
      .then((res) => res.json())
      .then((resData) => {
        if (resData.status === "ok") {
          setTickets(resData.data);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch tickets", err);
        setLoading(false);
      });
  }, []);

  const stats = {
    decisions: tickets.filter(t => t.decision).length,
    arguments: tickets.reduce((acc, t) => acc + (t.arguments?.length || 0), 0),
    authors: new Set([
      ...tickets.map(t => t.issue?.author),
      ...tickets.flatMap(t => t.arguments?.map(a => a.author) || [])
    ].filter(Boolean)).size,
  };

  if (loading) {
    return <div className="p-6 text-center">Loading graph data...</div>;
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Knowledge Graph</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Unified view of all decision tickets and their relationships
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <Card className="dark:bg-gray-800 dark:border-gray-700">
          <CardContent className="pt-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <ClientOnly fallback={<div className="w-5 h-5" />}>
                  <GitBranch className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </ClientOnly>
              </div>
              <div>
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.decisions}</p>
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
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.arguments}</p>
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
                <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">{stats.authors}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">Unique Authors</p>
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
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="border rounded-lg bg-gray-50 dark:bg-gray-900/50 p-8 text-center border-gray-200 dark:border-gray-700">
            <ClientOnly fallback={<div className="w-16 h-16 mx-auto mb-3" />}>
              <Network className="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-3" />
            </ClientOnly>
            <p className="text-gray-500 dark:text-gray-400 mb-2">
              Graph visualization of the GraphDB results will be available here.
            </p>
            <p className="text-sm text-gray-400 dark:text-gray-500">
              Visualizing the semantic nodes and relationships directly.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default GraphViewPage;

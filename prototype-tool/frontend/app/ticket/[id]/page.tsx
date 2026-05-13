"use client";

import { FC, useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { DecisionTicket, TicketVersion } from "../../../lib/types";
import { Badge } from "../../../components/ui/badge";
import { ArrowLeft, GitBranch, AlertCircle, Link as LinkIcon, User, Calendar, MessageSquare } from "lucide-react";
import { VersionSlider } from "../../../components/timeline/version-slider";
import { ClientOnly } from "../../../components/ui/client-only";
import { Card, CardContent, CardHeader, CardTitle } from "../../../components/ui/card";

export default function TicketTimelinePage() {
  const params = useParams();
  const ticketId = params.id as string;
  const [ticket, setTicket] = useState<DecisionTicket | null>(null);
  const [loading, setLoading] = useState(true);
  
  // Chronological list of versions
  const [chronoVersions, setChronoVersions] = useState<TicketVersion[]>([]);
  const [selectedIndex, setSelectedIndex] = useState<number>(0);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/v1/tickets`)
      .then((res) => res.json())
      .then((resData) => {
        if (resData.status === "ok") {
          const found = resData.data.find((t: DecisionTicket) => t.id === ticketId);
          if (found) {
            setTicket(found);
            // Sort versions chronologically (oldest first)
            const sorted = [...found.versions].sort(
              (a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
            );
            setChronoVersions(sorted);
            // Default to most recent
            setSelectedIndex(sorted.length - 1);
          }
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch tickets", err);
        setLoading(false);
      });
  }, [ticketId]);

  const currentVersion = chronoVersions[selectedIndex];



  if (loading) {
    return <div className="flex h-full items-center justify-center p-6 text-gray-500">Loading ticket details...</div>;
  }

  if (!ticket || chronoVersions.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-6 text-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Ticket not found</h1>
        <Link href="/" className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
          Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] overflow-hidden bg-gray-50 dark:bg-gray-900">
      {/* Top Header */}
      <div className="flex-none bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex items-center justify-between z-10 shadow-sm">
        <div className="flex items-center gap-4">
          <Link href="/" className="p-2 -ml-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-700">
            <ClientOnly fallback={<div className="w-5 h-5"/>}><ArrowLeft className="w-5 h-5" /></ClientOnly>
          </Link>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs font-bold bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 px-2 py-0.5 rounded">
                #{ticket.id}
              </span>
              <Badge variant="outline" className="text-[10px] uppercase tracking-wider font-semibold border-blue-200 text-blue-700 dark:border-blue-800 dark:text-blue-400">
                {ticket.status}
              </Badge>
              <Badge className="text-[10px] bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400 border-none shadow-none">
                {ticket.bucket}
              </Badge>
            </div>
            <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100 leading-tight">
              {ticket.title}
            </h1>
          </div>
        </div>
        <div className="flex gap-2">
          {/* Controls like edit/share could go here */}
        </div>
      </div>

      {/* Main Workspace Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left/Center: Graph Area */}
        <div className="flex-1 relative bg-[#f8f9fa] dark:bg-[#0a0a0a] overflow-hidden flex flex-col items-center justify-center border-r border-gray-200 dark:border-gray-800">
          {/* GRAPH PLACEHOLDER */}
          <div className="text-center space-y-4 p-8 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-2xl max-w-md">
            <div className="w-16 h-16 bg-blue-100 dark:bg-blue-900/50 rounded-xl mx-auto flex items-center justify-center">
              <GitBranch className="w-8 h-8 text-blue-600 dark:text-blue-400" />
            </div>
            <h2 className="text-xl font-bold text-gray-800 dark:text-gray-200">Graph View (Coming Soon)</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              The React Flow visualization will be implemented here. It will display the ontological nodes for Version {currentVersion.versionId.split('_v').pop()}.
            </p>
          </div>
        </div>

        {/* Right: Details Panel */}
        <div className="w-[450px] flex-none bg-white dark:bg-gray-800 overflow-y-auto flex flex-col shadow-[-4px_0_15px_-3px_rgba(0,0,0,0.05)] z-10">
          <div className="p-6 space-y-8">
            <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-700">
              <h2 className="text-lg font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                Version Details
                <Badge className="bg-blue-100 text-blue-700 hover:bg-blue-100 border-none dark:bg-blue-900/40 dark:text-blue-400">
                  v{currentVersion.versionId.split('_v').pop()}
                </Badge>
              </h2>
              <span className="text-xs font-medium text-gray-500 flex items-center gap-1.5">
                <Calendar className="w-3.5 h-3.5" />
                {new Date(currentVersion.timestamp).toLocaleDateString()}
              </span>
            </div>

            {/* Decision & Rationale */}
            <div className="space-y-6">
              <Card className="border-blue-100 dark:border-blue-900/50 shadow-sm rounded-xl overflow-hidden">
                <CardHeader className="pb-3 bg-blue-50/50 dark:bg-blue-900/10 border-b border-blue-100 dark:border-blue-900/30">
                  <CardTitle className="text-sm font-semibold flex items-center gap-2 text-blue-800 dark:text-blue-300">
                    <ClientOnly fallback={<div className="w-4 h-4" />}>
                      <GitBranch className="w-4 h-4" />
                    </ClientOnly>
                    Decision Summary
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-4 bg-white dark:bg-gray-800">
                  <p className="text-[15px] text-gray-800 dark:text-gray-200 leading-relaxed font-medium">
                    {currentVersion.decision || "No decision summary recorded for this version."}
                  </p>
                </CardContent>
              </Card>

              <div className="space-y-3">
                <h3 className="text-xs font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2 uppercase tracking-widest">
                  <ClientOnly fallback={<div className="w-3.5 h-3.5" />}>
                    <AlertCircle className="w-3.5 h-3.5 text-orange-500" />
                  </ClientOnly>
                  Rationale
                </h3>
                <div className="bg-gray-50 dark:bg-gray-900/40 p-4 rounded-xl border border-gray-200 dark:border-gray-800 text-[14px] text-gray-700 dark:text-gray-300 leading-relaxed italic shadow-sm">
                  {currentVersion.rationale || "No rationale provided."}
                </div>
              </div>
            </div>

            {/* Cost & Risk */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <h3 className="text-[10px] font-bold text-gray-500 dark:text-gray-400 flex items-center gap-1.5 uppercase tracking-widest">
                  <LinkIcon className="w-3 h-3 text-purple-500" />
                  Cost Impact
                </h3>
                <div className={`p-3 rounded-xl border text-xs leading-normal shadow-sm ${
                  currentVersion.cost 
                    ? "bg-purple-50/40 dark:bg-purple-900/10 border-purple-100 dark:border-purple-900/30 text-gray-800 dark:text-gray-200 font-medium"
                    : "bg-gray-50/50 dark:bg-gray-900/20 border-gray-100 dark:border-gray-800 text-gray-400 italic"
                }`}>
                  {currentVersion.cost || "Not specified"}
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-[10px] font-bold text-gray-500 dark:text-gray-400 flex items-center gap-1.5 uppercase tracking-widest">
                  <AlertCircle className="w-3 h-3 text-red-500" />
                  Risk Exposure
                </h3>
                <div className={`p-3 rounded-xl border text-xs leading-normal shadow-sm ${
                  currentVersion.risk 
                    ? "bg-red-50/40 dark:bg-red-900/10 border-red-100 dark:border-red-900/30 text-gray-800 dark:text-gray-200 font-medium"
                    : "bg-gray-50/50 dark:bg-gray-900/20 border-gray-100 dark:border-gray-800 text-gray-400 italic"
                }`}>
                  {currentVersion.risk || "Not specified"}
                </div>
              </div>
            </div>

            {/* Arguments */}
            <div className="space-y-4 pt-4 border-t border-gray-100 dark:border-gray-800">
              <h3 className="text-sm font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                Arguments ({currentVersion.arguments?.length || 0})
              </h3>
              
              {!currentVersion.arguments || currentVersion.arguments.length === 0 ? (
                <div className="flex flex-col items-center justify-center py-8 text-gray-400 bg-gray-50 dark:bg-gray-900/30 rounded-xl border border-dashed border-gray-200 dark:border-gray-700">
                  <MessageSquare className="w-6 h-6 opacity-20 mb-2" />
                  <p className="text-xs">No arguments for this version.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {[...currentVersion.arguments]
                    .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime())
                    .map((arg, idx) => (
                    <div
                      key={arg.id || idx}
                      className={`flex gap-3 p-3.5 rounded-xl border transition-all shadow-sm ${
                        arg.type === 'supports' ? 'bg-green-50/30 border-green-200 dark:bg-green-900/10 dark:border-green-900/30' :
                        arg.type === 'opposes' ? 'bg-red-50/30 border-red-200 dark:bg-red-900/10 dark:border-red-900/30' :
                        'bg-gray-50/50 border-gray-200 dark:bg-gray-800/30 dark:border-gray-700'
                      }`}
                    >
                      <div className="mt-0.5">
                        {arg.type === 'supports' ? (
                          <GitBranch className="w-3.5 h-3.5 text-green-600 dark:text-green-400" />
                        ) : arg.type === 'opposes' ? (
                          <AlertCircle className="w-3.5 h-3.5 text-red-600 dark:text-red-400" />
                        ) : (
                          <MessageSquare className="w-3.5 h-3.5 text-gray-600 dark:text-gray-400" />
                        )}
                      </div>
                      <div className="flex-1 space-y-1.5">
                        <p className="text-[13px] text-gray-800 dark:text-gray-200 leading-snug font-medium">
                          {arg.content}
                        </p>
                        <div className="flex items-center justify-between mt-2">
                          <span className="text-[10px] font-semibold text-gray-500 dark:text-gray-400 flex items-center gap-2">
                            <span className="flex items-center gap-1">
                              <User className="w-2.5 h-2.5" />
                              {arg.author}
                            </span>
                            {arg.createdAt && (
                              <span className="flex items-center gap-1 opacity-70">
                                <Calendar className="w-2.5 h-2.5" />
                                {new Date(arg.createdAt).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                              </span>
                            )}
                          </span>
                          <Badge variant="outline" className={`text-[9px] uppercase font-bold py-0 h-4 border-0 ${
                            arg.type === 'supports' ? 'bg-green-100 text-green-700 dark:bg-green-900/50 dark:text-green-400' :
                            arg.type === 'opposes' ? 'bg-red-100 text-red-700 dark:bg-red-900/50 dark:text-red-400' : ''
                          }`}>
                            {arg.type}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Timeline Panel */}
      <div className="flex-none">
        <VersionSlider 
          versions={chronoVersions} 
          selectedIndex={selectedIndex} 
          onChange={setSelectedIndex} 
        />
      </div>
    </div>
  );
}

import { FC } from "react";
import { DecisionTicket } from "../../lib/types";
import { Badge } from "../ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Separator } from "../ui/separator";
import { Calendar, User, FileText, Link as LinkIcon, AlertCircle, CheckCircle2, XCircle, GitBranch, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "../ui/card";
import { DialogHeader, DialogTitle, DialogDescription } from "../ui/dialog";
import { ClientOnly } from "../ui/client-only";
import { formatDate } from "../../lib/utils";

interface Props {
  ticket: DecisionTicket;
}

export const TicketDetails: FC<Props> = ({ ticket }) => {
  const version = ticket.versions[ticket.currentVersionIndex];

  const statusColors: Record<string, string> = {
    draft: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
    proposed: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    accepted: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    rejected: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
    deprecated: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400",
    Decided: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    open: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    closed: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
    idea: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
  };

  return (
    <div className="flex flex-col h-full max-h-[80vh]">
      <DialogHeader className="mb-4">
        <div className="flex items-start justify-between">
          <div>
            <DialogTitle className="text-xl font-bold flex items-center gap-2">
              {ticket.title}
              <Badge className={`ml-2 ${statusColors[ticket.status]}`}>{ticket.status}</Badge>
            </DialogTitle>
            <DialogDescription className="text-sm text-gray-500 mt-1 flex items-center gap-2">
              <span className="font-mono text-xs bg-gray-100 dark:bg-gray-800 px-1 py-0.5 rounded">{ticket.id}</span>
              {ticket.createdAt && (
                <>
                  <span>•</span>
                  <span>{formatDate(ticket.createdAt)}</span>
                </>
              )}
              <span>•</span>
              <span className="flex items-center gap-1">
                <ClientOnly fallback={<div className="w-3 h-3" />}>
                  <User className="w-3 h-3" />
                </ClientOnly>
                {ticket.owner.name}
              </span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <ClientOnly fallback={<div className="w-3 h-3" />}>
                  <Calendar className="w-3 h-3" />
                </ClientOnly>
                Updated {ticket.updatedAt}
              </span>
            </DialogDescription>
          </div>
        </div>
      </DialogHeader>

      <Tabs defaultValue="overview" className="flex-1 overflow-hidden flex flex-col">
        <TabsList className="grid w-full grid-cols-4 mb-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="arguments">Arguments</TabsTrigger>
          <TabsTrigger value="artifacts">Artifacts</TabsTrigger>
          <TabsTrigger value="graph">Graph View</TabsTrigger>
        </TabsList>

        <div className="flex-1 overflow-y-auto pr-2 space-y-4">
          {/* Overview Tab */}
          <TabsContent value="overview" className="mt-0 space-y-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base font-medium flex items-center gap-2">
                  <ClientOnly fallback={<div className="w-4 h-4" />}>
                    <GitBranch className="w-4 h-4 text-blue-500" />
                  </ClientOnly>
                  Current Decision (v{version.versionId})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed font-medium">
                  {version.decision}
                </p>
              </CardContent>
            </Card>

            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 flex items-center gap-2">
                <ClientOnly fallback={<div className="w-4 h-4" />}>
                  <FileText className="w-4 h-4" />
                </ClientOnly>
                Rationale
              </h3>
              <div className="bg-gray-50 dark:bg-gray-900/50 p-4 rounded-lg border text-sm text-gray-600 dark:text-gray-400">
                {version.rationale}
              </div>
            </div>

            <div className="space-y-2">
              <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">Context</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {version.context}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 pt-2">
              <div className="space-y-2 p-3 bg-blue-50/50 dark:bg-blue-900/10 border border-blue-100 dark:border-blue-900/30 rounded-lg">
                <h3 className="text-sm font-semibold text-blue-900 dark:text-blue-100 flex items-center gap-2">
                   Cost
                </h3>
                <p className="text-sm text-blue-800/80 dark:text-blue-200/80">
                  {version.cost || "No cost data available"}
                </p>
              </div>
              <div className="space-y-2 p-3 bg-orange-50/50 dark:bg-orange-900/10 border border-orange-100 dark:border-orange-900/30 rounded-lg">
                <h3 className="text-sm font-semibold text-orange-900 dark:text-orange-100 flex items-center gap-2">
                  Risk
                </h3>
                <p className="text-sm text-orange-800/80 dark:text-orange-200/80">
                  {version.risk || "No risk data available"}
                </p>
              </div>
            </div>
          </TabsContent>

          {/* Arguments Tab */}
          <TabsContent value="arguments" className="mt-0 space-y-3">
            {version.arguments.length === 0 ? (
              <div className="text-center py-8 text-gray-500 text-sm">No arguments recorded yet.</div>
            ) : (
              version.arguments.map((arg) => (
                <div
                  key={arg.id}
                  className={`flex gap-3 p-3 rounded-lg border ${arg.type === 'supports'
                    ? 'bg-green-50/50 border-green-100 dark:bg-green-900/10 dark:border-green-900/30'
                    : 'bg-red-50/50 border-red-100 dark:bg-red-900/10 dark:border-red-900/30'
                    }`}
                >
                  <div className="mt-0.5">
                    {arg.type === 'supports' ? (
                      <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-600 dark:text-red-400" />
                    )}
                  </div>
                  <div>
                    <p className="text-sm text-gray-800 dark:text-gray-200">{arg.content}</p>
                    <p className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                      <ClientOnly fallback={<div className="w-3 h-3" />}>
                        <User className="w-3 h-3" />
                      </ClientOnly>
                      {arg.author} {arg.createdAt && `• ${formatDate(arg.createdAt)}`}
                    </p>
                  </div>
                </div>
              ))
            )}
          </TabsContent>

          {/* Artifacts Tab */}
          <TabsContent value="artifacts" className="mt-0 h-full">
            {version.artifacts.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-12 text-gray-500 gap-2">
                <ClientOnly fallback={<div className="w-8 h-8" />}>
                  <AlertCircle className="w-8 h-8 opacity-50" />
                </ClientOnly>
                <p className="text-sm">No artifacts linked to this version.</p>
              </div>
            ) : (
              <div className="grid gap-2">
                {version.artifacts.map((art) => (
                  <a
                    key={art.id}
                    href={art.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 p-3 rounded-md border hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors group"
                  >
                    <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-blue-600 dark:text-blue-400 group-hover:bg-blue-100 dark:group-hover:bg-blue-900/40 transition-colors">
                      <ClientOnly fallback={<div className="w-4 h-4" />}>
                        <LinkIcon className="w-4 h-4" />
                      </ClientOnly>
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{art.name}</p>
                      <p className="text-xs text-gray-500 uppercase tracking-wider">{art.type}</p>
                    </div>
                  </a>
                ))}
              </div>
            )}
          </TabsContent>

          {/* Graph View Tab */}
          <TabsContent value="graph" className="mt-0 h-full">
            <div className="flex flex-col items-center justify-center py-12 text-gray-500 gap-4">
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-full">
                <ClientOnly fallback={<div className="w-8 h-8" />}>
                  <GitBranch className="w-8 h-8 opacity-50" />
                </ClientOnly>
              </div>
              <div className="text-center space-y-2">
                <p className="font-medium text-gray-900 dark:text-gray-100">Decision Graph Visualization</p>
                <p className="text-sm max-w-xs mx-auto">
                  Explore the full decision knowledge graph and its evolution history.
                </p>
              </div>
              <a
                href="#"
                className="mt-2 inline-flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm font-medium transition-colors"
              >
                View Graph History
                <LinkIcon className="w-4 h-4" />
              </a>
            </div>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
};

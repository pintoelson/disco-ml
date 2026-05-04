import { FC } from "react";
import { DecisionTicket } from "../../lib/types";
import { Badge } from "../ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import { Calendar, User, FileText, Link as LinkIcon, AlertCircle, GitBranch, MessageSquare } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { DialogHeader, DialogTitle, DialogDescription } from "../ui/dialog";
import { ClientOnly } from "../ui/client-only";

interface Props {
  ticket: DecisionTicket;
}

export const TicketDetails: FC<Props> = ({ ticket }) => {
  return (
    <div className="flex flex-col h-full max-h-[85vh]">
      <DialogHeader className="mb-6">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-bold bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 px-2 py-1 rounded">
                #{ticket.id}
              </span>
              <Badge variant="outline" className="text-xs uppercase tracking-wider font-semibold border-blue-200 text-blue-700">
                {ticket.status}
              </Badge>
              <Badge className="text-xs bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                {ticket.bucket}
              </Badge>
            </div>
            <DialogTitle className="text-2xl font-bold text-gray-900 dark:text-gray-100 leading-tight">
              {ticket.title}
            </DialogTitle>
            <DialogDescription className="text-sm text-gray-500 mt-2 flex items-center gap-4 flex-wrap">
              <span className="flex items-center gap-1.5">
                <ClientOnly fallback={<div className="w-3.5 h-3.5" />}>
                  <Calendar className="w-3.5 h-3.5" />
                </ClientOnly>
                {ticket.createdAt ? new Date(ticket.createdAt).toLocaleString() : "Unknown date"}
              </span>
              <span className="flex items-center gap-1.5">
                <ClientOnly fallback={<div className="w-3.5 h-3.5" />}>
                  <User className="w-3.5 h-3.5" />
                </ClientOnly>
                {ticket.author}
              </span>
            </DialogDescription>
          </div>
        </div>
      </DialogHeader>

      <Tabs defaultValue="overview" className="flex-1 overflow-hidden flex flex-col">
        <TabsList className="grid w-full grid-cols-3 mb-6 bg-gray-100 dark:bg-gray-800/50 p-1 p-1 rounded-lg">
          <TabsTrigger value="overview" className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700 shadow-sm">Overview</TabsTrigger>
          <TabsTrigger value="arguments" className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700 shadow-sm">
            Arguments ({ticket.arguments?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="history" className="data-[state=active]:bg-white dark:data-[state=active]:bg-gray-700 shadow-sm">History</TabsTrigger>
        </TabsList>

        <div className="flex-1 overflow-y-auto pr-2 space-y-6">
          {/* Overview Tab */}
          <TabsContent value="overview" className="mt-0 space-y-6">
            <div className="grid grid-cols-1 gap-6">
              <Card className="border-blue-100 dark:border-blue-900/50 shadow-sm">
                <CardHeader className="pb-3 bg-blue-50/30 dark:bg-blue-900/10">
                  <CardTitle className="text-sm font-semibold flex items-center gap-2 text-blue-800 dark:text-blue-300">
                    <ClientOnly fallback={<div className="w-4 h-4" />}>
                      <GitBranch className="w-4 h-4" />
                    </ClientOnly>
                    Decision Summary
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-4">
                  <p className="text-base text-gray-800 dark:text-gray-200 leading-relaxed font-medium">
                    {ticket.decision}
                  </p>
                </CardContent>
              </Card>

              <div className="space-y-3">
                <h3 className="text-sm font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2 uppercase tracking-wide">
                  <ClientOnly fallback={<div className="w-4 h-4" />}>
                    <AlertCircle className="w-4 h-4 text-orange-500" />
                  </ClientOnly>
                  Rationale
                </h3>
                <div className="bg-gray-50 dark:bg-gray-900/30 p-4 rounded-xl border border-gray-200 dark:border-gray-800 text-sm text-gray-700 dark:text-gray-300 leading-relaxed italic">
                  {ticket.rationale}
                </div>
              </div>

              <div className="space-y-3">
                <h3 className="text-sm font-bold text-gray-900 dark:text-gray-100 flex items-center gap-2 uppercase tracking-wide">
                  <ClientOnly fallback={<div className="w-4 h-4" />}>
                    <FileText className="w-4 h-4 text-gray-500" />
                  </ClientOnly>
                  Context & Constraints
                </h3>
                <div className="text-sm text-gray-600 dark:text-gray-400 leading-relaxed whitespace-pre-wrap">
                  {ticket.description}
                </div>
              </div>
            </div>
          </TabsContent>

          {/* Arguments Tab */}
          <TabsContent value="arguments" className="mt-0 space-y-4">
            {!ticket.arguments || ticket.arguments.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-16 text-gray-400 gap-2">
                <MessageSquare className="w-8 h-8 opacity-20" />
                <p className="text-sm">No argumentation data captured for this decision.</p>
              </div>
            ) : (
              <div className="space-y-3">
                {ticket.arguments.map((arg, index) => (
                  <div
                    key={arg.id || index}
                    className={`flex gap-4 p-4 rounded-xl border transition-all ${
                      arg.type === 'supports' ? 'bg-green-50/50 border-green-100 dark:bg-green-900/10 dark:border-green-900/30' :
                      arg.type === 'opposes' ? 'bg-red-50/50 border-red-100 dark:bg-red-900/10 dark:border-red-900/30' :
                      'bg-gray-50 dark:bg-gray-800/50 border-gray-200 dark:border-gray-700'
                    }`}
                  >
                    <div className="mt-1">
                      {arg.type === 'supports' ? (
                        <div className="p-1.5 bg-green-100 dark:bg-green-900/50 rounded-full">
                          <GitBranch className="w-4 h-4 text-green-600 dark:text-green-400" />
                        </div>
                      ) : arg.type === 'opposes' ? (
                        <div className="p-1.5 bg-red-100 dark:bg-red-900/50 rounded-full">
                          <AlertCircle className="w-4 h-4 text-red-600 dark:text-red-400" />
                        </div>
                      ) : (
                        <div className="p-1.5 bg-gray-200 dark:bg-gray-700 rounded-full">
                          <MessageSquare className="w-4 h-4 text-gray-600 dark:text-gray-400" />
                        </div>
                      )}
                    </div>
                    <div className="space-y-2 flex-1">
                      <p className="text-sm text-gray-800 dark:text-gray-200 leading-relaxed font-medium">
                        {arg.content}
                      </p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <span className="text-xs font-semibold text-gray-600 dark:text-gray-400 flex items-center gap-1.5">
                            <User className="w-3 h-3" />
                            {arg.author}
                          </span>
                          {arg.createdAt && (
                            <span className="text-xs text-gray-500 flex items-center gap-1">
                              <Calendar className="w-3 h-3" />
                              {new Date(arg.createdAt).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })}
                            </span>
                          )}
                        </div>
                        <Badge variant="outline" className="text-[10px] uppercase font-bold py-0 h-4">
                          {arg.type}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </TabsContent>

          {/* History Tab */}
          <TabsContent value="history" className="mt-0">
             <div className="flex flex-col items-center justify-center py-16 text-gray-500 gap-4">
              <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-full">
                <GitBranch className="w-8 h-8 opacity-40" />
              </div>
              <div className="text-center space-y-1">
                <p className="font-semibold text-gray-900 dark:text-gray-100">Decision Provenance</p>
                <p className="text-sm text-gray-500 max-w-xs mx-auto">
                  Version history and diffs are coming soon. This decision is currently on version <b>{ticket.versions[0]?.versionId.split('_v').pop()}</b>.
                </p>
              </div>
            </div>
          </TabsContent>
        </div>
      </Tabs>
    </div>
  );
};

"use client";

import { FC, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { mockTickets } from "../../lib/mock-data";
import KnowledgeGraph from "../../components/graph/knowledge-graph";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import {
  ArrowLeft,
  History,
  Share2,
  Edit,
  ChevronRight,
  User,
  Calendar,
  Tag,
  Scale,
} from "lucide-react";

const VersionTimeline: FC<{
  versions: typeof mockTickets[0]["versions"];
  currentIndex: number;
  onSelectVersion: (index: number) => void;
}> = ({ versions, currentIndex, onSelectVersion }) => {
  return (
    <Card className="mb-4 dark:bg-gray-800 dark:border-gray-700">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-semibold flex items-center gap-2 text-gray-900 dark:text-gray-100">
          <History className="w-4 h-4" />
          Version History
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="relative">
          <div className="absolute left-3 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700" />
          <div className="space-y-3">
            {versions.map((version, index) => (
              <button
                key={version.versionId}
                onClick={() => onSelectVersion(index)}
                className={`relative flex items-center gap-3 w-full text-left pl-8 ${
                  index === currentIndex ? "" : "opacity-60 hover:opacity-100"
                }`}
              >
                <div
                  className={`absolute left-2 w-2 h-2 rounded-full ${
                    index === currentIndex
                      ? "bg-blue-500 ring-4 ring-blue-100 dark:ring-blue-900"
                      : "bg-gray-300 dark:bg-gray-600"
                  }`}
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-900 dark:text-gray-100">v{version.versionId}</span>
                    {index === versions.length - 1 && (
                      <Badge variant="secondary" className="text-xs dark:bg-gray-700 dark:text-gray-300">
                        Latest
                      </Badge>
                    )}
                    {version.parentVersionId && (
                      <span className="text-xs text-gray-400 dark:text-gray-500">
                        ← v{version.parentVersionId}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mt-0.5">
                    {version.decision}
                  </p>
                </div>
                {index < versions.length - 1 && (
                  <ChevronRight className="w-4 h-4 text-gray-400 dark:text-gray-500" />
                )}
              </button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const DecisionTable: FC<{
  ticket: typeof mockTickets[0];
  versionIndex: number;
}> = ({ ticket, versionIndex }) => {
  const version = ticket.versions[versionIndex];
  const statusColors: Record<string, string> = {
    draft: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
    proposed: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    accepted: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    rejected: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
    deprecated: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400",
  };

  return (
    <Card className="dark:bg-gray-800 dark:border-gray-700">
      <CardHeader className="pb-3">
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="text-xl text-gray-900 dark:text-gray-100">{version.decision}</CardTitle>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{ticket.id}</p>
          </div>
          <Badge className={statusColors[ticket.status]}>{ticket.status}</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Rationale</h4>
          <p className="text-gray-600 dark:text-gray-400">{version.rationale}</p>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Context</h4>
          <p className="text-gray-600 dark:text-gray-400">{version.context}</p>
        </div>

        <Separator className="dark:border-gray-700" />

        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
            <Scale className="w-4 h-4" />
            Arguments ({version.arguments.length})
          </h4>
          <div className="space-y-2">
            {version.arguments.map((arg) => (
              <div
                key={arg.id}
                className={`p-3 rounded-lg border-l-4 ${
                  arg.type === "supports"
                    ? "border-l-green-500 bg-green-50 dark:bg-green-900/20"
                    : "border-l-red-500 bg-red-50 dark:bg-red-900/20"
                }`}
              >
                <span
                  className={`text-xs font-semibold uppercase ${
                    arg.type === "supports"
                      ? "text-green-700 dark:text-green-400"
                      : "text-red-700 dark:text-red-400"
                  }`}
                >
                  {arg.type}
                </span>
                <p className="text-sm mt-1 text-gray-900 dark:text-gray-100">{arg.content}</p>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  — {arg.author} • {arg.createdAt}
                </p>
              </div>
            ))}
          </div>
        </div>

        <Separator className="dark:border-gray-700" />

        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
            <User className="w-4 h-4" />
            Owner
          </h4>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <User className="w-4 h-4 text-blue-600 dark:text-blue-400" />
            </div>
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">{ticket.owner.name}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">{ticket.owner.role}</p>
            </div>
          </div>
        </div>

        <Separator className="dark:border-gray-700" />

        <div className="flex gap-4 text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            <span>Created {ticket.createdAt}</span>
          </div>
          <div className="flex items-center gap-1">
            <Tag className="w-4 h-4" />
            {ticket.tags.map((tag) => (
              <Badge key={tag} variant="outline" className="mr-1 text-xs dark:border-gray-600 dark:text-gray-400">
                {tag}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

const KnowledgeGraphPanel: FC<{
  ticket: typeof mockTickets[0];
}> = ({ ticket }) => {
  return (
    <Card className="h-full dark:bg-gray-800 dark:border-gray-700">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-semibold flex items-center justify-between text-gray-900 dark:text-gray-100">
          <span className="flex items-center gap-2">
            Knowledge Graph
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-2 mb-3 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500" />
            <span className="text-gray-700 dark:text-gray-300">Decision</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-green-500" />
            <span className="text-gray-700 dark:text-gray-300">Argument (Supports)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500" />
            <span className="text-gray-700 dark:text-gray-300">Argument (Opposes)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-purple-500" />
            <span className="text-gray-700 dark:text-gray-300">Agent</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-orange-500" />
            <span className="text-gray-700 dark:text-gray-300">Artifact</span>
          </div>
        </div>

        <KnowledgeGraph ticketId={ticket.id} />
      </CardContent>
    </Card>
  );
};

export default function TicketDetailPage() {
  const params = useParams();
  const ticketId = params.id as string;
  const ticket = mockTickets.find((t) => t.id === ticketId);

  const [versionIndex, setVersionIndex] = useState(
    ticket?.currentVersionIndex ?? 0
  );

  if (!ticket) {
    return (
      <div className="p-6 text-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Ticket not found</h1>
        <Link href="/">
          <Button className="mt-4">Back to Dashboard</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Dashboard
      </Link>

      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{ticket.title}</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Decision knowledge graph evolution
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="dark:border-gray-600 dark:text-gray-300">
            <Edit className="w-4 h-4 mr-1" />
            Edit
          </Button>
          <Button variant="outline" size="sm" className="dark:border-gray-600 dark:text-gray-300">
            <Share2 className="w-4 h-4 mr-1" />
            Share
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-4">
          <VersionTimeline
            versions={ticket.versions}
            currentIndex={versionIndex}
            onSelectVersion={setVersionIndex}
          />
        </div>

        <div className="col-span-8">
          <div className="grid grid-cols-2 gap-4">
            <DecisionTable ticket={ticket} versionIndex={versionIndex} />
            <KnowledgeGraphPanel ticket={ticket} />
          </div>
        </div>
      </div>
    </div>
  );
}

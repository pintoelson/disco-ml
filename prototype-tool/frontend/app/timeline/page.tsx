"use client";

import { FC, useState } from "react";
import Link from "next/link";
import { mockTickets } from "../../lib/mock-data";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import {
  ArrowLeft,
  Clock,
  GitBranch,
  User,
  Scale,
  Tag,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { ClientOnly } from "../../components/ui/client-only";

const TimelinePage: FC = () => {
  const sortedTickets = [...mockTickets].sort(
    (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime()
  );

  const statusColors: Record<string, string> = {
    draft: "bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
    proposed: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",
    accepted: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    rejected: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400",
    deprecated: "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400",
  };

  const bucketColors: Record<string, string> = {
    "Model Training": "bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
    "Model Evaluation": "bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400",
    "Model Deployment": "bg-purple-50 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400",
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Timeline View</h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Reverse chronological view of all decision tickets
        </p>
      </div>

      <div className="relative">
        <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gray-200 dark:bg-gray-700" />
        <div className="space-y-6">
          {sortedTickets.map((ticket, index) => {
            const version = ticket.versions[ticket.currentVersionIndex];
            const supportCount = version.arguments.filter(
              (a) => a.type === "supports"
            ).length;
            const opposeCount = version.arguments.filter(
              (a) => a.type === "opposes"
            ).length;

            return (
              <TimelineCard
                key={ticket.id}
                ticket={ticket}
                supportCount={supportCount}
                opposeCount={opposeCount}
                statusColors={statusColors}
                bucketColors={bucketColors}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
};

interface TimelineCardProps {
  ticket: typeof mockTickets[0];
  supportCount: number;
  opposeCount: number;
  statusColors: Record<string, string>;
  bucketColors: Record<string, string>;
}

const TimelineCard: FC<TimelineCardProps> = ({
  ticket,
  supportCount,
  opposeCount,
  statusColors,
  bucketColors,
}) => {
  const [expanded, setExpanded] = useState(false);
  const reversedVersions = [...ticket.versions].reverse();

  return (
    <div className="relative">
      <div className="absolute left-6 top-8 w-4 h-4 rounded-full bg-blue-500 border-2 border-white dark:border-gray-900 z-10" />
      <Card className="ml-8 hover:shadow-md transition-shadow dark:bg-gray-800 dark:border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <Badge className={`text-xs ${bucketColors[ticket.bucket]}`}>
                  {ticket.bucket}
                </Badge>
                <Badge className={`${statusColors[ticket.status]}`}>
                  {ticket.status}
                </Badge>
              </div>
              <Link
                href={`/ticket/${ticket.id}`}
                className="text-lg font-semibold text-gray-900 dark:text-gray-100 hover:text-blue-600 dark:hover:text-blue-400"
              >
                {ticket.id}: {ticket.title}
              </Link>
              <div className="flex items-center gap-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                <div className="flex items-center gap-1">
                  <ClientOnly fallback={<div className="w-4 h-4" />}>
                    <Clock className="w-4 h-4" />
                  </ClientOnly>
                  <span>Updated {ticket.updatedAt}</span>
                </div>
                <div className="flex items-center gap-1">
                  <ClientOnly fallback={<div className="w-4 h-4" />}>
                    <GitBranch className="w-4 h-4" />
                  </ClientOnly>
                  <span>{ticket.versions.length} version{ticket.versions.length > 1 ? "s" : ""}</span>
                </div>
              </div>
            </div>
            <button
              onClick={() => setExpanded(!expanded)}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              {expanded ? (
                <ClientOnly fallback={<div className="w-5 h-5" />}>
                  <ChevronUp className="w-5 h-5 text-gray-500" />
                </ClientOnly>
              ) : (
                <ClientOnly fallback={<div className="w-5 h-5" />}>
                  <ChevronDown className="w-5 h-5 text-gray-500" />
                </ClientOnly>
              )}
            </button>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
            {ticket.versions[ticket.currentVersionIndex].rationale}
          </p>

          <div className="flex flex-wrap items-center gap-2 mb-3">
            {ticket.tags.map((tag) => (
              <Badge key={tag} variant="outline" className="text-xs dark:border-gray-600 dark:text-gray-400">
                <ClientOnly fallback={<div className="w-3 h-3 mr-1" />}>
                  <Tag className="w-3 h-3 mr-1" />
                </ClientOnly>
                {tag}
              </Badge>
            ))}
          </div>

          <div className="flex items-center justify-between pt-2 border-t dark:border-gray-700">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1">
                <ClientOnly fallback={<div className="w-4 h-4" />}>
                  <User className="w-4 h-4 text-gray-400" />
                </ClientOnly>
                <span className="text-sm text-gray-600 dark:text-gray-400">{ticket.owner.name}</span>
              </div>
              <div className="flex items-center gap-1">
                <ClientOnly fallback={<div className="w-4 h-4" />}>
                  <Scale className="w-4 h-4 text-gray-400" />
                </ClientOnly>
                <span className="text-sm text-green-600 dark:text-green-400">
                  {supportCount} supports
                </span>
                <span className="mx-1 text-gray-300 dark:text-gray-600">•</span>
                <span className="text-sm text-red-600 dark:text-red-400">
                  {opposeCount} opposes
                </span>
              </div>
            </div>
            <Link href={`/ticket/${ticket.id}`}>
              <Button variant="outline" size="sm" className="dark:border-gray-600 dark:text-gray-300">
                View Details
              </Button>
            </Link>
          </div>

          {expanded && (
            <div className="mt-4 pt-4 border-t dark:border-gray-700">
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                Version History
              </h4>
              <div className="space-y-3">
                {reversedVersions.map((version, idx) => (
                  <div
                    key={version.versionId}
                    className={`p-3 rounded-lg border ${
                      idx === 0
                        ? "border-blue-300 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-700"
                        : "border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/50"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-sm text-gray-900 dark:text-gray-100">
                          v{version.versionId}
                        </span>
                        {idx === 0 && (
                          <Badge variant="secondary" className="text-xs">
                            Current
                          </Badge>
                        )}
                      </div>
                      <span className="text-xs text-gray-500 dark:text-gray-400">
                        {ticket.versions.findIndex(v => v.versionId === version.versionId) === 0
                          ? "Latest"
                          : `← v${version.parentVersionId}`}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {version.decision}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default TimelinePage;

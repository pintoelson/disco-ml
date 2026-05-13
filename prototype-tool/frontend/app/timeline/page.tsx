"use client";

import { FC, useState, useEffect } from "react";
import Link from "next/link";
import { DecisionTicket } from "../../lib/types";
import { Card, CardContent, CardHeader } from "../../components/ui/card";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import {
  Clock,
  User,
  Scale,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { ClientOnly } from "../../components/ui/client-only";

const TimelinePage: FC = () => {
  const [tickets, setTickets] = useState<DecisionTicket[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${apiUrl}/api/v1/tickets`)
      .then((res) => res.json())
      .then((resData) => {
        if (resData.status === "ok") {
          const sorted = resData.data.sort(
            (a: DecisionTicket, b: DecisionTicket) => 
              new Date(b.issue?.timestamp || 0).getTime() - new Date(a.issue?.timestamp || 0).getTime()
          );
          setTickets(sorted);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch tickets", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-6 text-center">Loading timeline...</div>;
  }

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
          {tickets.map((ticket) => (
            <TimelineCard key={ticket.id} ticket={ticket} />
          ))}
        </div>
      </div>
    </div>
  );
};

interface TimelineCardProps {
  ticket: DecisionTicket;
}

const TimelineCard: FC<TimelineCardProps> = ({ ticket }) => {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="relative">
      <div className="absolute left-6 top-8 w-4 h-4 rounded-full bg-blue-500 border-2 border-white dark:border-gray-900 z-10" />
      <Card className="ml-8 hover:shadow-md transition-shadow dark:bg-gray-800 dark:border-gray-700">
        <CardHeader className="pb-2">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                {ticket.issue?.phase && (
                  <Badge className="text-xs bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
                    {ticket.issue.phase.split("#").pop()}
                  </Badge>
                )}
              </div>
              <Link
                href={`/ticket/${ticket.id}`}
                className="text-lg font-semibold text-gray-900 dark:text-gray-100 hover:text-blue-600 dark:hover:text-blue-400"
              >
                {ticket.id}: {ticket.issue?.label}
              </Link>
              <div className="flex items-center gap-4 mt-2 text-sm text-gray-500 dark:text-gray-400">
                <div className="flex items-center gap-1">
                  <ClientOnly fallback={<div className="w-4 h-4" />}>
                    <Clock className="w-4 h-4" />
                  </ClientOnly>
                  <span>{ticket.issue?.timestamp}</span>
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
            {ticket.decision?.label}
          </p>

          <div className="flex items-center justify-between pt-2 border-t dark:border-gray-700">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1">
                <ClientOnly fallback={<div className="w-4 h-4" />}>
                  <User className="w-4 h-4 text-gray-400" />
                </ClientOnly>
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {ticket.issue?.author?.split("#").pop() || "Unknown Author"}
                </span>
              </div>
              <div className="flex items-center gap-1">
                <ClientOnly fallback={<div className="w-4 h-4" />}>
                  <Scale className="w-4 h-4 text-gray-400" />
                </ClientOnly>
                <span className="text-sm text-blue-600 dark:text-blue-400">
                  {ticket.arguments?.length || 0} arguments
                </span>
              </div>
            </div>
            <Link href={`/ticket/${ticket.id}`}>
              <Button variant="outline" size="sm" className="dark:border-gray-600 dark:text-gray-300">
                View Details
              </Button>
            </Link>
          </div>

          {expanded && ticket.arguments && ticket.arguments.length > 0 && (
            <div className="mt-4 pt-4 border-t dark:border-gray-700">
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
                Arguments
              </h4>
              <div className="space-y-3">
                {ticket.arguments.map((arg, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/50"
                  >
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {arg.comment}
                    </p>
                    <div className="mt-1 flex items-center justify-between">
                      <span className="text-xs text-gray-500 dark:text-gray-500">
                        {arg.author?.split("#").pop()}
                      </span>
                    </div>
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

"use client";

import { FC, useState, useEffect } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { DecisionTicket } from "../../lib/types";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import {
  ArrowLeft,
  Share2,
  Edit,
  User,
  Calendar,
  Tag,
  Scale,
} from "lucide-react";

export default function TicketDetailPage() {
  const params = useParams();
  const ticketId = params.id as string;
  const [ticket, setTicket] = useState<DecisionTicket | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/data/tickets")
      .then((res) => res.json())
      .then((resData) => {
        if (resData.status === "ok") {
          const found = resData.data.find((t: DecisionTicket) => t.id === ticketId);
          setTicket(found || null);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch tickets", err);
        setLoading(false);
      });
  }, [ticketId]);

  if (loading) {
    return <div className="p-6 text-center">Loading ticket details...</div>;
  }

  if (!ticket) {
    return (
      <div className="p-6 text-center">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Ticket not found</h1>
        <Link href="/decision-ticket">
          <Button className="mt-4">Back to Tickets</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <Link
        href="/decision-ticket"
        className="inline-flex items-center gap-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 mb-4"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Tickets
      </Link>

      <div className="flex justify-between items-start mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{ticket.issue?.label}</h1>
          <p className="text-gray-500 dark:text-gray-400 mt-1">
            Ticket ID: {ticket.id}
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

      <div className="grid grid-cols-1 gap-6">
        <Card className="dark:bg-gray-800 dark:border-gray-700">
          <CardHeader className="pb-3">
            <div className="flex justify-between items-start">
              <div>
                <CardTitle className="text-xl text-gray-900 dark:text-gray-100">{ticket.decision?.label}</CardTitle>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Graph URI: {ticket.graphUri}</p>
              </div>
              {ticket.issue?.phase && (
                <Badge className="bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400">
                  {ticket.issue.phase.split("#").pop()}
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <Separator className="dark:border-gray-700" />

            <div>
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
                <Scale className="w-4 h-4" />
                Arguments ({ticket.arguments?.length || 0})
              </h4>
              <div className="space-y-2">
                {ticket.arguments?.map((arg, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-lg border-l-4 border-l-blue-500 bg-blue-50 dark:bg-blue-900/20"
                  >
                    <p className="text-sm mt-1 text-gray-900 dark:text-gray-100">{arg.comment}</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      — {arg.author.split("#").pop()}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            <Separator className="dark:border-gray-700" />

            <div>
              <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2 flex items-center gap-2">
                <User className="w-4 h-4" />
                Author
              </h4>
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                  <User className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <p className="font-medium text-gray-900 dark:text-gray-100">{ticket.issue?.author?.split("#").pop()}</p>
                </div>
              </div>
            </div>

            <Separator className="dark:border-gray-700" />

            <div className="flex gap-4 text-sm text-gray-500 dark:text-gray-400">
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                <span>Timestamp: {ticket.issue?.timestamp}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

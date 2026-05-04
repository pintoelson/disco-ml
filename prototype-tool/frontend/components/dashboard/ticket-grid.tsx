"use client";

import { FC, useState, useEffect } from "react";
import { DecisionTicket, TicketBucket } from "../../lib/types";
import {
  Card,
  CardContent,
} from "../ui/card";
import { Badge } from "../ui/badge";
import { Button } from "../ui/button";
import {
  Search,
  Filter,
  Plus,
  GitBranch,
  User,
  History,
} from "lucide-react";
import { Dialog, DialogContent } from "../ui/dialog";
import { TicketDetails } from "../decision-ticket/ticket-details";
import { ClientOnly } from "../ui/client-only";

const BUCKETS: TicketBucket[] = [
  "ML Project Initiation",
  "Data Preparation",
  "Modeling Development",
  "Model Evaluation",
  "Model Deployment",
  "Monitoring & Maintenance",
  "Miscellaneous",
  "Uncertain"
];

interface TicketCardProps {
  ticket: DecisionTicket;
  onTicketClick: (ticket: DecisionTicket) => void;
}

const TicketCard: FC<TicketCardProps> = ({ ticket, onTicketClick }) => {
  // Extract version number for display
  const versionId = ticket.versions[0]?.versionId || "v1";
  const versionNum = versionId.includes("_v") ? `v${versionId.split("_v").pop()}` : versionId;

  return (
    <div onClick={() => onTicketClick(ticket)}>
      <Card className="mb-3 hover:shadow-md transition-all cursor-pointer border-l-4 border-l-blue-500 dark:bg-gray-800 dark:border-gray-700 overflow-hidden relative">
        <CardContent className="p-4 space-y-2">
          {/* Version Ribbon */}
          <div className="absolute top-0 right-0 bg-blue-50 dark:bg-blue-900/30 px-2 py-0.5 rounded-bl-lg border-l border-b border-blue-100 dark:border-blue-800 flex items-center gap-1">
             <History className="w-3 h-3 text-blue-600 dark:text-blue-400" />
             <span className="text-[10px] font-bold text-blue-700 dark:text-blue-400 uppercase tracking-tighter">
                {versionNum}
             </span>
          </div>

          <div className="flex justify-between items-start gap-2 pr-12">
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-medium flex gap-2">
                <span>#{ticket.id}</span>
                {ticket.createdAt && <span>• {new Date(ticket.createdAt).toLocaleDateString()}</span>}
              </p>
              <p className="font-semibold text-gray-900 dark:text-gray-100 line-clamp-2 mt-1 leading-tight">
                {ticket.title}
              </p>
            </div>
          </div>

          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 italic leading-snug">
            {ticket.decision}
          </p>

          <div className="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-700">
            <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
              <ClientOnly fallback={<div className="w-3 h-3" />}>
                <GitBranch className="w-3 h-3" />
              </ClientOnly>
              <span>{ticket.arguments?.length || 0}</span>
            </div>
            <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
              <ClientOnly fallback={<div className="w-3 h-3" />}>
                <User className="w-3 h-3 text-blue-600" />
              </ClientOnly>
              <span className="truncate max-w-[80px]">{ticket.author}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

interface BucketColumnProps {
  bucket: TicketBucket;
  tickets: DecisionTicket[];
  onTicketClick: (ticket: DecisionTicket) => void;
}

const BucketColumn: FC<BucketColumnProps> = ({ bucket, tickets, onTicketClick }) => {
  const bucketColors: Record<TicketBucket, { header: string; border: string }> = {
    "ML Project Initiation": { header: "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800", border: "border-blue-400" },
    "Data Preparation": { header: "bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800", border: "border-orange-400" },
    "Modeling Development": { header: "bg-teal-50 dark:bg-teal-900/20 border-teal-200 dark:border-teal-800", border: "border-teal-400" },
    "Model Evaluation": { header: "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800", border: "border-green-400" },
    "Model Deployment": { header: "bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-800", border: "border-purple-400" },
    "Monitoring & Maintenance": { header: "bg-indigo-50 dark:bg-indigo-900/20 border-indigo-200 dark:border-indigo-800", border: "border-indigo-400" },
    "Miscellaneous": { header: "bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800", border: "border-gray-400" },
    "Uncertain": { header: "bg-pink-50 dark:bg-pink-900/20 border-pink-200 dark:border-pink-800", border: "border-pink-400" },
  };

  const colors = bucketColors[bucket];

  return (
    <div className="flex flex-col h-full">
      <div className={`px-4 py-3 rounded-t-lg border-x border-t ${colors.header} flex items-center justify-between`}>
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-gray-100 whitespace-nowrap">{bucket}</h3>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {tickets.length} ticket{tickets.length !== 1 ? "s" : ""}
          </p>
        </div>
      </div>
      <div className={`border-x border-b rounded-b-lg bg-gray-50 dark:bg-gray-900/50 p-2 min-h-[500px] flex-1 ${colors.border}`}>
        {tickets.length === 0 ? (
          <div className="flex items-center justify-center h-32 text-gray-400 dark:text-gray-500 text-sm italic">
            No tickets
          </div>
        ) : (
          tickets.map((ticket) => (
            <TicketCard key={ticket.id} ticket={ticket} onTicketClick={onTicketClick} />
          ))
        )}
      </div>
    </div>
  );
};

const Dashboard: FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [tickets, setTickets] = useState<DecisionTicket[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTicket, setSelectedTicket] = useState<DecisionTicket | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/data/tickets")
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

  const handleTicketClick = (ticket: DecisionTicket) => {
    setSelectedTicket(ticket);
    setIsDialogOpen(true);
  };

  const filteredTickets = tickets.filter((ticket) =>
    ticket.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ticket.decision?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ticket.id?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // ONLY SHOW BUCKETS THAT HAVE TICKETS
  const activeBuckets = BUCKETS.filter(bucket => 
    filteredTickets.some(t => t.bucket === bucket)
  );

  const totalTickets = tickets.length;

  if (loading) {
    return <div className="p-6 text-center text-gray-500">Loading decision dashboard...</div>;
  }

  return (
    <div className="p-6 max-w-[1800px] mx-auto overflow-x-hidden">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 tracking-tight">
          Decision Knowledge Base
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Visualizing the architectural evolution of DISCO-ML components
        </p>
      </div>

      <div className="flex items-center justify-between mb-8 bg-white dark:bg-gray-800 p-4 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="flex items-center gap-4">
          <div className="relative w-96">
            <ClientOnly fallback={<div className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4" />}>
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            </ClientOnly>
            <input
              type="text"
              placeholder="Search by title, decision, or ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-gray-100"
            />
          </div>
          <Button variant="outline" className="flex items-center gap-2 dark:border-gray-700 dark:text-gray-300">
            <ClientOnly fallback={<div className="w-4 h-4" />}>
              <Filter className="w-4 h-4" />
            </ClientOnly>
            Filter By Artifact
          </Button>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex flex-col items-end">
            <span className="text-sm font-semibold text-gray-900 dark:text-gray-100">
              {totalTickets} Tickets
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              Synced from GraphDB
            </span>
          </div>
        </div>
      </div>

      <div className="grid grid-flow-col auto-cols-[350px] gap-6 overflow-x-auto pb-8 scrollbar-hide">
        {activeBuckets.length > 0 ? (
          activeBuckets.map((bucket) => {
            const bucketTickets = filteredTickets.filter((t) => t.bucket === bucket);
            return (
              <BucketColumn 
                key={bucket} 
                bucket={bucket} 
                tickets={bucketTickets} 
                onTicketClick={handleTicketClick} 
              />
            );
          })
        ) : (
          <div className="flex flex-col items-center justify-center py-20 w-full text-gray-400 gap-4">
            <History className="w-12 h-12 opacity-10" />
            <p>No active decision buckets found.</p>
          </div>
        )}
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        {selectedTicket && (
          <DialogContent className="max-w-4xl max-h-[90vh] overflow-hidden">
            <TicketDetails ticket={selectedTicket} />
          </DialogContent>
        )}
      </Dialog>
    </div>
  );
};

export default Dashboard;

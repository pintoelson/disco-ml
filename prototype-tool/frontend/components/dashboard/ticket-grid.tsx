"use client";

import { FC, useState } from "react";
import { mockTickets } from "../../lib/mock-data";
import { DecisionTicket, TicketBucket } from "../../lib/types";
import { formatDate } from "../../lib/utils";
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
    <div onClick={() => onTicketClick(ticket)}>
      <Card className="mb-3 hover:shadow-md transition-all cursor-pointer border-l-4 border-l-blue-500 dark:bg-gray-800 dark:border-gray-700">
        <CardContent className="p-4 space-y-2">
          <div className="flex justify-between items-start gap-2">
            <div>
              <p className="text-xs text-gray-500 dark:text-gray-400 font-medium flex gap-2">
                <span>{ticket.id}</span>
                {ticket.createdAt && <span>• {formatDate(ticket.createdAt)}</span>}
              </p>
              <p className="font-semibold text-gray-900 dark:text-gray-100 line-clamp-2">
                {ticket.title}
              </p>
            </div>
            <Badge className={`text-xs ${statusColors[ticket.status]}`}>
              {ticket.status}
            </Badge>
          </div>

          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
            {version.rationale}
          </p>

          <div className="flex items-center justify-between pt-2">
            <div className="flex items-center gap-1 text-xs text-gray-500 dark:text-gray-400">
              <ClientOnly fallback={<div className="w-3 h-3" />}>
                <GitBranch className="w-3 h-3" />
              </ClientOnly>
              <span>v{version.versionId}</span>
              <span>•</span>
              <span>{ticket.versions.length} version{ticket.versions.length > 1 ? "s" : ""}</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-5 h-5 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <ClientOnly fallback={<div className="w-3 h-3" />}>
                  <User className="w-3 h-3 text-blue-600 dark:text-blue-400" />
                </ClientOnly>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-1">
            {ticket.tags.slice(0, 3).map((tag) => (
              <Badge key={tag} variant="outline" className="text-xs dark:border-gray-600 dark:text-gray-400">
                {tag}
              </Badge>
            ))}
            {ticket.tags.length > 3 && (
              <Badge variant="outline" className="text-xs dark:border-gray-600 dark:text-gray-400">
                +{ticket.tags.length - 3}
              </Badge>
            )}
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
    <div className="flex flex-col">
      <div className={`px-4 py-3 rounded-t-lg border-x border-t ${colors.header} flex items-center justify-between`}>
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-gray-100">{bucket}</h3>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            {tickets.length} ticket{tickets.length !== 1 ? "s" : ""}
          </p>
        </div>
        <button className="p-1 hover:bg-white/50 dark:hover:bg-gray-700/50 rounded transition-colors">
          <ClientOnly fallback={<div className="w-4 h-4" />}>
            <Plus className="w-4 h-4 text-gray-500 dark:text-gray-400" />
          </ClientOnly>
        </button>
      </div>
      <div className={`border-x border-b rounded-b-lg bg-gray-50 dark:bg-gray-900/50 p-2 min-h-[400px] flex-1 ${colors.border}`}>
        {tickets.length === 0 ? (
          <div className="flex items-center justify-center h-32 text-gray-400 dark:text-gray-500 text-sm">
            Drop tickets here
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
  const [selectedTicket, setSelectedTicket] = useState<DecisionTicket | null>(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const handleTicketClick = (ticket: DecisionTicket) => {
    setSelectedTicket(ticket);
    setIsDialogOpen(true);
  };

  const handleDialogClose = () => {
    setIsDialogOpen(false);
    setSelectedTicket(null);
  };

  const filteredTickets = mockTickets.filter((ticket) =>
    ticket.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ticket.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ticket.tags.some((tag) => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const ticketsByBucket = BUCKETS.map((bucket) => ({
    bucket,
    tickets: filteredTickets.filter((t) => t.bucket === bucket),
  }));

  const totalTickets = mockTickets.length;

  return (
    <div className="p-6 max-w-[1600px] mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          Decision Knowledge Base
        </h1>
        <p className="text-gray-500 dark:text-gray-400 mt-1">
          Track and visualize architectural decisions across your ML projects
        </p>
      </div>

      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <div className="relative w-80">
            <ClientOnly fallback={<div className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4" />}>
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            </ClientOnly>
            <input
              type="text"
              placeholder="Search tickets..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900 dark:text-gray-100"
            />
          </div>
          <Button variant="outline" className="flex items-center gap-2 dark:border-gray-700 dark:text-gray-300">
            <ClientOnly fallback={<div className="w-4 h-4" />}>
              <Filter className="w-4 h-4" />
            </ClientOnly>
            Filters
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {totalTickets} total tickets
          </span>
        </div>
      </div>

      {searchQuery && (
        <div className="mb-4 text-sm text-gray-500 dark:text-gray-400">
          Showing {filteredTickets.length} of {totalTickets} tickets
        </div>
      )}

      <div className="flex flex-row overflow-x-auto gap-6 pb-4">
        {ticketsByBucket.map(({ bucket, tickets }) => (
          <div key={bucket} className="min-w-[350px] w-[350px]">
            <BucketColumn bucket={bucket} tickets={tickets} onTicketClick={handleTicketClick} />
          </div>
        ))}
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        {selectedTicket && (
          <DialogContent className="max-w-3xl sm:max-w-[700px]">
            <TicketDetails ticket={selectedTicket} />
          </DialogContent>
        )}
      </Dialog>
    </div>
  );
};

export default Dashboard;

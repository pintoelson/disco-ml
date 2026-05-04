"use client";

import { useState, useEffect } from "react";
import { TicketTable } from "../../components/decision-ticket/ticket-table";
import { PageContainer } from "../../components/layout/page-container";
import { DecisionTicket } from "../../lib/types";

export default function DecisionTicketsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [tickets, setTickets] = useState<DecisionTicket[]>([]);
  const [loading, setLoading] = useState(true);

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
  
  const filteredTickets = tickets.filter((t) => 
    t.issue?.label?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    t.id?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <PageContainer>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Decision Tickets</h2>
        <input
          type="text"
          placeholder="Search tickets..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="border rounded px-3 py-1 text-sm bg-white dark:bg-gray-800"
        />
      </div>
      
      {loading ? (
        <p className="text-gray-500">Loading tickets...</p>
      ) : filteredTickets.length > 0 ? (
        <TicketTable tickets={filteredTickets} />
      ) : (
        <p className="text-gray-500">No tickets found.</p>
      )}
    </PageContainer>
  );
}

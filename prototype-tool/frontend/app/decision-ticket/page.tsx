"use client";

import { useState } from "react";
import { TicketTable } from "../../components/decision-ticket/ticket-table";
import { PageContainer } from "../../components/layout/page-container";
import { mockTickets } from "../../lib/mock-data";

export default function DecisionTicketsPage() {
  const [searchQuery, setSearchQuery] = useState("");
  
  const filteredTickets = mockTickets.filter((t) => 
    t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    t.id.toLowerCase().includes(searchQuery.toLowerCase())
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
      
      {filteredTickets.length > 0 ? (
        <TicketTable tickets={filteredTickets} />
      ) : (
        <p className="text-gray-500">No tickets found.</p>
      )}
    </PageContainer>
  );
}

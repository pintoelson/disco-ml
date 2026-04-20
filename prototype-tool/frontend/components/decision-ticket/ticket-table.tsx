import { FC } from "react";
import { DecisionTicket } from "../../lib/types";

interface Props {
  tickets: DecisionTicket[];
}

export const TicketTable: FC<Props> = ({ tickets }) => (
  <table className="table-auto w-full border-collapse border border-gray-200">
    <thead>
      <tr className="bg-gray-200">
        <th className="border px-4 py-2">Title</th>
        <th className="border px-4 py-2">Decision</th>
        <th className="border px-4 py-2">Timestamp</th>
      </tr>
    </thead>
    <tbody>
      {tickets.map((t) => (
        <tr key={t.id} className="hover:bg-gray-100">
          <td className="border px-4 py-2">{t.title}</td>
          <td className="border px-4 py-2">{t.decision}</td>
          <td className="border px-4 py-2">{t.timestamp}</td>
        </tr>
      ))}
    </tbody>
  </table>
);
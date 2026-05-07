import { FC } from "react";
import { DecisionTicket } from "../../lib/types";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "../ui/card";
import { Badge } from "../ui/badge";

interface Props {
  ticket: DecisionTicket;
}

export const TicketCard: FC<Props> = ({ ticket }) => {
  return (
    <Card className="mb-4 hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle>{ticket.title}</CardTitle>
        <CardDescription className="text-gray-500">
          {ticket.timestamp}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-2">
        <div className="flex flex-wrap gap-2">
          <Badge variant="default">Decision: {ticket.decision}</Badge>
        </div>
      </CardContent>
    </Card>
  );
};

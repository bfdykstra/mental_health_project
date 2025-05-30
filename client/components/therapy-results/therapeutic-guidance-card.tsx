import type React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain } from "lucide-react";

interface TherapeuticGuidanceCardProps {
  response: string;
}

export function TherapeuticGuidanceCard({
  response,
}: TherapeuticGuidanceCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Brain className="h-5 w-5 mr-2 text-legacy-green" />
          Therapeutic Guidance
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="prose prose-sm max-w-none">
          <div className="whitespace-pre-wrap text-gray-700">{response}</div>
        </div>
      </CardContent>
    </Card>
  );
}

import type React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Brain, Loader2 } from "lucide-react";

interface TherapeuticGuidanceCardProps {
  response: string;
  isStreaming?: boolean;
  isLoading?: boolean;
}

export function TherapeuticGuidanceCard({
  response,
  isStreaming = false,
  isLoading = false,
}: TherapeuticGuidanceCardProps) {
  if (!response && !isLoading) return null;

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center">
          <Brain className="h-5 w-5 mr-2 text-legacy-green" />
          Possible Therapeutic Response
          {isLoading && isStreaming && response && (
            <Badge variant="outline" className="ml-2">
              <Loader2 className="h-3 w-3 animate-spin mr-1" />
              Generating...
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        <div className="prose prose-sm max-w-none flex-1">
          <div className="whitespace-pre-wrap text-gray-700">
            {response}
            {isLoading && isStreaming && response && (
              <span className="inline-block w-2 h-5 bg-blue-500 animate-pulse ml-1" />
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

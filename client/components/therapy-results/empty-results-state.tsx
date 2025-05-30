import type React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Brain } from "lucide-react";

export function EmptyResultsState() {
  return (
    <Card className="border-dashed">
      <CardContent className="flex flex-col items-center justify-center py-12 text-center">
        <Brain className="h-12 w-12 text-gray-400 mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Ready to provide guidance
        </h3>
        <p className="text-gray-600">
          Enter patient information and your question to receive personalized
          therapeutic recommendations.
        </p>
      </CardContent>
    </Card>
  );
}

import type React from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, CheckCircle } from "lucide-react";

interface ProgressCardProps {
  isLoading: boolean;
  progress: string;
  stage: string;
}

export function ProgressCard({
  isLoading,
  progress,
  stage,
}: ProgressCardProps) {
  const getStageIcon = (currentStage: string) => {
    switch (currentStage) {
      case "initialization":
      case "search":
      case "processing":
      case "synthesis":
        return <Loader2 className="h-4 w-4 animate-spin text-blue-500" />;
      default:
        return <CheckCircle className="h-4 w-4 text-green-500" />;
    }
  };

  const getStageText = (currentStage: string) => {
    switch (currentStage) {
      case "initialization":
        return "Initializing";
      case "search":
        return "Searching";
      case "processing":
        return "Processing";
      case "synthesis":
        return "Generating";
      default:
        return "Complete";
    }
  };

  if (!isLoading) return null;

  return (
    <Card className="border-blue-200 bg-blue-50">
      <CardHeader>
        <CardTitle className="flex items-center text-blue-800">
          {getStageIcon(stage)}
          <span className="ml-2">
            {getStageText(stage)} - {progress}
          </span>
        </CardTitle>
      </CardHeader>
    </Card>
  );
}

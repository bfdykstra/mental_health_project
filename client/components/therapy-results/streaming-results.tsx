import type React from "react";
import type { TherapyResponse, SimilarExample } from "@/types/therapy";
import { ProgressCard } from "./progress-card";
import { TherapeuticGuidanceCard } from "./therapeutic-guidance-card";
import { AppliedKeywordsCard } from "./applied-keywords-card";
import { EmptyResultsState } from "./empty-results-state";

interface StreamingResultsProps {
  isLoading: boolean;
  progress: string;
  stage: string;
  similarExamples: SimilarExample[];
  streamingResponse: string;
  finalResponse: TherapyResponse | null;
}

export function StreamingResults({
  isLoading,
  progress,
  stage,
  similarExamples,
  streamingResponse,
  finalResponse,
}: StreamingResultsProps) {
  // Determine what to show based on current state
  const hasContent = streamingResponse || finalResponse;
  const showEmptyState = !isLoading && !hasContent;

  return (
    <div className="space-y-6">
      {/* Progress indicator for streaming */}
      <ProgressCard isLoading={isLoading} progress={progress} stage={stage} />

      {/* Therapeutic guidance - streaming or final */}
      <TherapeuticGuidanceCard
        response={finalResponse?.synthesized_response || streamingResponse}
        isStreaming={!finalResponse}
        isLoading={isLoading}
      />

      {/* Applied keywords - only show when final response is available */}
      {finalResponse && (
        <AppliedKeywordsCard keywords={finalResponse.keywords} />
      )}

      {/* Empty state */}
      {showEmptyState && <EmptyResultsState />}
    </div>
  );
}

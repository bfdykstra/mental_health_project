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
    <div className="flex flex-col h-full">
      {/* Empty state - positioned at top when no content */}
      {showEmptyState && <EmptyResultsState />}

      {/* Progress indicator for streaming - positioned at top when loading */}
      {isLoading && (
        <div className="mb-4">
          <ProgressCard
            isLoading={isLoading}
            progress={progress}
            stage={stage}
          />
        </div>
      )}

      {/* Main content area - only show when there's content or loading */}
      {!showEmptyState && (
        <div className="flex flex-col flex-1 gap-4">
          {/* Therapeutic guidance - expands to fill available space */}
          <div className="flex-1">
            <TherapeuticGuidanceCard
              response={
                finalResponse?.synthesized_response || streamingResponse
              }
              isStreaming={!finalResponse}
              isLoading={isLoading}
            />
          </div>

          {/* Applied keywords - fixed size at bottom when available */}
          {finalResponse && (
            <div className="flex-shrink-0">
              <AppliedKeywordsCard keywords={finalResponse.keywords} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

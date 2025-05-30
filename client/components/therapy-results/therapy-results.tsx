import type React from "react";
import type { TherapyResponse } from "@/types/therapy";
import { TherapeuticGuidanceCard } from "./therapeutic-guidance-card";
import { AppliedKeywordsCard } from "./applied-keywords-card";
import { SimilarCasesCard } from "./similar-cases-card";
import { EmptyResultsState } from "./empty-results-state";

interface TherapyResultsProps {
  response: TherapyResponse | null;
  isLoading: boolean;
}

export function TherapyResults({ response, isLoading }: TherapyResultsProps) {
  if (!response && !isLoading) {
    return <EmptyResultsState />;
  }

  if (!response) {
    return null;
  }

  return (
    <div className="space-y-6">
      <TherapeuticGuidanceCard response={response.synthesized_response} />
      <AppliedKeywordsCard keywords={response.keywords} />
      <SimilarCasesCard examples={response.similar_examples} />
    </div>
  );
}

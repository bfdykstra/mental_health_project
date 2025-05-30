"use client";

import type React from "react";
import { useState } from "react";
import type { TherapyRequest, TherapyResponse } from "@/types/therapy";
import { fetchApi } from "@/lib/api";
import { Header } from "@/components/header";
import { HeroSection } from "@/components/hero-section";
import { PatientInputForm } from "@/components/patient-input-form";
import { TherapyResults } from "@/components/therapy-results/therapy-results";

export default function TherapyCopilot() {
  const [query, setQuery] = useState("");
  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([]);
  const [topK, setTopK] = useState(5);
  const [response, setResponse] = useState<TherapyResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    try {
      const requestData: TherapyRequest = {
        user_query: query,
        keywords: selectedKeywords.length > 0 ? selectedKeywords : undefined,
        top_k: topK,
      };

      const res = await fetchApi("/synthesize-therapy-response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });
      console.log("Response:", res);
      const data: TherapyResponse = res;
      setResponse(data);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <HeroSection />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <PatientInputForm
            query={query}
            setQuery={setQuery}
            selectedKeywords={selectedKeywords}
            setSelectedKeywords={setSelectedKeywords}
            topK={topK}
            setTopK={setTopK}
            isLoading={isLoading}
            onSubmit={handleSubmit}
          />

          <TherapyResults response={response} isLoading={isLoading} />
        </div>
      </div>
    </div>
  );
}

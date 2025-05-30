"use client";

import type React from "react";
import { useState } from "react";
import type { TherapyRequest, TherapyResponse } from "@/types/therapy";
import { fetchApi, streamApi } from "@/lib/api";
import { Header } from "@/components/header";
import { HeroSection } from "@/components/hero-section";
import { PatientInputForm } from "@/components/patient-input-form";
import { TherapyResults } from "@/components/therapy-results/therapy-results";
import { StreamingResults } from "@/components/therapy-results/streaming-results";
import { SimilarCasesCard } from "@/components/therapy-results/similar-cases-card";

export default function TherapyCopilot() {
  const [query, setQuery] = useState("");
  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([]);
  const [topK, setTopK] = useState(5);
  const [response, setResponse] = useState<TherapyResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(true); // Default to streaming

  // Streaming state
  const [streamingProgress, setStreamingProgress] = useState<string>("");
  const [streamingSimilarExamples, setStreamingSimilarExamples] = useState<
    any[]
  >([]);
  const [streamingResponse, setStreamingResponse] = useState<string>("");
  const [streamingStage, setStreamingStage] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);

    // Reset streaming state
    setStreamingProgress("");
    setStreamingSimilarExamples([]);
    setStreamingResponse("");
    setStreamingStage("");
    setResponse(null);

    const requestData: TherapyRequest = {
      user_query: query,
      keywords: selectedKeywords.length > 0 ? selectedKeywords : undefined,
      top_k: topK,
    };

    if (isStreaming) {
      streamApi(
        "/synthesize-therapy-response/stream",
        requestData,
        (eventData) => {
          switch (eventData.type) {
            case "progress":
              setStreamingProgress(eventData.message);
              setStreamingStage(eventData.stage);
              break;
            case "similar_examples":
              setStreamingSimilarExamples(eventData.data);
              break;
            case "response_chunk":
              setStreamingResponse(eventData.accumulated_response);
              break;
            case "complete":
              const finalResponse: TherapyResponse = eventData.data;
              setResponse(finalResponse);
              setIsLoading(false);
              break;
            case "error":
              console.error("Stream error:", eventData.message);
              setStreamingProgress(`Error: ${eventData.message}`);
              setIsLoading(false);
              break;
          }
        },
        (error) => {
          console.error("Streaming error:", error);
          setStreamingProgress(`Connection error: ${error.message}`);
          setIsLoading(false);
        },
        () => {
          setIsLoading(false);
        }
      );
    } else {
      // Use regular REST API
      try {
        const res = await fetchApi("/synthesize-therapy-response", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });
        const data: TherapyResponse = res;
        setResponse(data);
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setIsLoading(false);
      }
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
            isStreaming={isStreaming}
            onSubmit={handleSubmit}
          />

          {isStreaming ? (
            <StreamingResults
              isLoading={isLoading}
              progress={streamingProgress}
              stage={streamingStage}
              similarExamples={streamingSimilarExamples}
              streamingResponse={streamingResponse}
              finalResponse={response}
            />
          ) : (
            <TherapyResults response={response} isLoading={isLoading} />
          )}
        </div>

        {/* Similar Cases Section - Full width below the main grid */}
        {((isStreaming &&
          (streamingSimilarExamples.length > 0 ||
            response?.similar_examples)) ||
          (!isStreaming && response?.similar_examples)) && (
          <div className="mt-4">
            <SimilarCasesCard
              examples={response?.similar_examples || streamingSimilarExamples}
            />
          </div>
        )}
      </div>
    </div>
  );
}

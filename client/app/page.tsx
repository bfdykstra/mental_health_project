"use client";

import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Loader2, Brain, Users, MessageSquare } from "lucide-react";
import {
  type TherapyRequest,
  type TherapyResponse,
  THERAPY_KEYWORDS,
} from "@/types/therapy";
import { MultiSelect } from "@/components/multi-select";
import { fetchApi } from "@/lib/api";

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

  const keywordOptions = THERAPY_KEYWORDS.map((keyword) => ({
    label: keyword,
    value: keyword,
  }));

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-legacy-green rounded flex items-center justify-center">
                <span className="text-white font-bold text-lg">L</span>
              </div>
              <span className="text-xl font-semibold text-gray-900">
                Legacy Mental Health Copilot
              </span>
            </div>
            {/* <div className="text-sm text-gray-600">Mental Health Copilot</div> */}
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Brain className="h-8 w-8 text-legacy-green mr-2" />
            <span className="text-sm font-medium text-legacy-green uppercase tracking-wide">
              AI-Powered Guidance
            </span>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Get personalized therapy guidance
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Enter patient information and receive evidence-based therapeutic
            recommendations tailored to your specific situation.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <Card className="h-fit">
            <CardHeader>
              <CardTitle className="flex items-center">
                <MessageSquare className="h-5 w-5 mr-2 text-legacy-green" />
                Patient Information & Query
              </CardTitle>
              <CardDescription>
                Provide patient transcript excerpts and your specific question
                about therapeutic approach.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <Label htmlFor="query" className="text-sm font-medium">
                    Patient Transcript & Question
                  </Label>
                  <Textarea
                    id="query"
                    placeholder="Example:&#10;&#10;Patient: 'I've been feeling really overwhelmed lately with work and family responsibilities. I can't seem to find time for myself and I'm starting to feel burned out. Sometimes I just want to run away from everything. How do I deal with these feelings?'&#10;&#10;Question: How should a therapist respond to this patient who is expressing feelings of overwhelm and burnout?"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="min-h-[200px] resize-none"
                    required
                  />
                </div>

                <div>
                  <Label className="text-sm font-medium mb-2 block">
                    Related Keywords (Optional)
                  </Label>
                  <MultiSelect
                    options={keywordOptions}
                    onValueChange={setSelectedKeywords}
                    defaultValue={selectedKeywords}
                    placeholder="Select relevant keywords..."
                    variant="inverted"
                    maxCount={5}
                  />
                </div>

                <Button
                  type="submit"
                  disabled={isLoading || !query.trim()}
                  className="w-full bg-legacy-green hover:bg-legacy-green-dark"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    "Get Therapeutic Guidance"
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Results */}
          <div className="space-y-6">
            {response && (
              <>
                {/* Synthesized Response */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Brain className="h-5 w-5 mr-2 text-legacy-green" />
                      Therapeutic Guidance
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="prose prose-sm max-w-none">
                      <div className="whitespace-pre-wrap text-gray-700">
                        {response.synthesized_response}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Keywords */}
                {response.keywords.length > 0 && (
                  <Card>
                    <CardHeader>
                      <CardTitle className="text-lg">
                        Applied Keywords
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="flex flex-wrap gap-2">
                        {response.keywords.map((keyword) => (
                          <Badge key={keyword} variant="secondary">
                            {keyword}
                          </Badge>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Similar Examples */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Users className="h-5 w-5 mr-2 text-legacy-green" />
                      Similar Cases ({response.similar_examples.length})
                    </CardTitle>
                    <CardDescription>
                      Related therapeutic scenarios from our knowledge base
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {response.similar_examples.map((example, index) => (
                        <div
                          key={index}
                          className="border-l-4 border-legacy-green pl-4 py-2"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-gray-900">
                              Example {index + 1}
                            </span>
                            {example.similarity_score && (
                              <Badge variant="outline">
                                {Math.round(example.similarity_score * 100)}%
                                match
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-gray-700 mb-3">
                            {example.prompt}
                          </p>
                          {/* Display search keywords if available */}
                          {example.metadata?.search_keywords &&
                            example.metadata.search_keywords.length > 0 && (
                              <div className="mt-2">
                                <span className="text-xs font-medium text-gray-600 mb-1 block">
                                  Search Keywords:
                                </span>
                                <div className="flex flex-wrap gap-1">
                                  {example.metadata.search_keywords.map(
                                    (keyword: string, keywordIndex: number) => (
                                      <Badge
                                        key={keywordIndex}
                                        variant="secondary"
                                        className="text-xs"
                                      >
                                        {keyword}
                                      </Badge>
                                    )
                                  )}
                                </div>
                              </div>
                            )}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}

            {!response && !isLoading && (
              <Card className="border-dashed">
                <CardContent className="flex flex-col items-center justify-center py-12 text-center">
                  <Brain className="h-12 w-12 text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    Ready to provide guidance
                  </h3>
                  <p className="text-gray-600">
                    Enter patient information and your question to receive
                    personalized therapeutic recommendations.
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

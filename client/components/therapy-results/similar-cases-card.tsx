import type React from "react";
import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Users, ChevronDown, ChevronUp, MessageSquare } from "lucide-react";
import type { SimilarExample } from "@/types/therapy";

interface SimilarCasesCardProps {
  examples: SimilarExample[];
}

export function SimilarCasesCard({ examples }: SimilarCasesCardProps) {
  const [expandedExamples, setExpandedExamples] = useState<Set<number>>(
    new Set()
  );

  const toggleExpanded = (index: number) => {
    const newExpanded = new Set(expandedExamples);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedExamples(newExpanded);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Users className="h-5 w-5 mr-2 text-legacy-green" />
          Similar Cases ({examples.length})
        </CardTitle>
        <CardDescription>
          Related therapeutic scenarios from our knowledge base
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {examples.map((example, index) => {
            const isExpanded = expandedExamples.has(index);
            const highQualityResponses =
              example.metadata?.quality_buckets?.high_quality;
            const hasResponses =
              highQualityResponses &&
              Array.isArray(highQualityResponses) &&
              highQualityResponses.length > 0;

            return (
              <div
                key={index}
                className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                {/* <div className="border-l-4 border-legacy-green pl-4"> */}
                <div className="pl-4">
                  <div className="flex items-center justify-between mb-2">
                    {/* <span className="text-sm font-medium text-gray-900">
                      Example {index + 1}
                    </span> */}
                    {example.similarity_score && (
                      <Badge variant="outline">
                        {Math.round(example.similarity_score * 100)}% match
                      </Badge>
                    )}
                  </div>
                  <p className="text-sm text-gray-700 mb-3">{example.prompt}</p>

                  {hasResponses && (
                    <div className="mt-3">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => toggleExpanded(index)}
                        className="flex items-center text-legacy-green hover:text-legacy-green/80 p-0 h-auto"
                      >
                        <MessageSquare className="h-4 w-4 mr-1" />
                        {isExpanded ? "Hide" : "Show"} Possible Responses (
                        {highQualityResponses.length})
                        {isExpanded ? (
                          <ChevronUp className="h-4 w-4 ml-1" />
                        ) : (
                          <ChevronDown className="h-4 w-4 ml-1" />
                        )}
                      </Button>

                      {isExpanded && (
                        <div className="mt-3 space-y-3 border-t pt-3">
                          {/* <span className="text-xs font-medium text-gray-600 block">
                            Some possible responses:
                          </span> */}
                          {highQualityResponses.map(
                            (response: string, responseIndex: number) => (
                              <div
                                key={responseIndex}
                                className="bg-gray-50 p-3 rounded-md border-l-2 border-legacy-green/30"
                              >
                                <div className="flex items-center mb-2">
                                  <Badge variant="outline" className="text-xs">
                                    Response {responseIndex + 1}
                                  </Badge>
                                </div>
                                <p className="text-sm text-gray-700 leading-relaxed">
                                  {response}
                                </p>
                              </div>
                            )
                          )}
                        </div>
                      )}
                    </div>
                  )}

                  {example.metadata?.search_keywords &&
                    example.metadata.search_keywords.length > 0 && (
                      <div className="mt-2 mb-3">
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
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

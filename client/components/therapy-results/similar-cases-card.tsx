import type React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Users } from "lucide-react";
import type { SimilarExample } from "@/types/therapy";

interface SimilarCasesCardProps {
  examples: SimilarExample[];
}

export function SimilarCasesCard({ examples }: SimilarCasesCardProps) {
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
        <div className="space-y-4">
          {examples.map((example, index) => (
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
                    {Math.round(example.similarity_score * 100)}% match
                  </Badge>
                )}
              </div>
              <p className="text-sm text-gray-700 mb-3">{example.prompt}</p>
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
  );
}

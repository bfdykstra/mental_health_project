import type React from "react";
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
import { Switch } from "@/components/ui/switch";
import { Loader2, MessageSquare, Zap, Clock } from "lucide-react";
import { THERAPY_KEYWORDS } from "@/types/therapy";
import { MultiSelect } from "@/components/multi-select";

interface PatientInputFormProps {
  query: string;
  setQuery: (query: string) => void;
  selectedKeywords: string[];
  setSelectedKeywords: (keywords: string[]) => void;
  topK: number;
  setTopK: (topK: number) => void;
  isLoading: boolean;
  isStreaming: boolean;
  setIsStreaming: (streaming: boolean) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export function PatientInputForm({
  query,
  setQuery,
  selectedKeywords,
  setSelectedKeywords,
  isLoading,
  isStreaming,
  setIsStreaming,
  onSubmit,
}: PatientInputFormProps) {
  const keywordOptions = THERAPY_KEYWORDS.map((keyword) => ({
    label: keyword,
    value: keyword,
  }));

  return (
    <Card className="h-fit">
      <CardHeader>
        <CardTitle className="flex items-center">
          <MessageSquare className="h-5 w-5 mr-2 text-legacy-green" />
          Patient Information & Query
        </CardTitle>
        <CardDescription>
          Provide patient transcript excerpts and your specific question about
          therapeutic approach.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-6">
          <div>
            <Label htmlFor="query" className="text-sm font-medium">
              Patient Transcript & Question
            </Label>
            <Textarea
              id="query"
              placeholder="Example:&#10;&#10;Patient: 'I've been feeling really overwhelmed lately with work and family responsibilities. I can't seem to find time for myself and I'm starting to feel burned out. Sometimes I just want to run away from everything. How do I deal with these feelings?'&#10;&#10;Question: How should I respond to this patient who is expressing feelings of overwhelm and burnout?"
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

          {/* Streaming Mode Toggle */}
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-3">
              {isStreaming ? (
                <Zap className="h-5 w-5 text-blue-500" />
              ) : (
                <Clock className="h-5 w-5 text-gray-500" />
              )}
              <div>
                <Label
                  htmlFor="streaming-mode"
                  className="text-sm font-medium cursor-pointer"
                >
                  {isStreaming ? "Real-time Streaming" : "Standard Mode"}
                </Label>
                <p className="text-xs text-gray-600">
                  {isStreaming
                    ? "See results as they generate for faster feedback"
                    : "Wait for complete response before displaying results"}
                </p>
              </div>
            </div>
            <Switch
              id="streaming-mode"
              checked={isStreaming}
              onCheckedChange={setIsStreaming}
              disabled={isLoading}
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
                {isStreaming ? "Streaming..." : "Analyzing..."}
              </>
            ) : (
              <>
                {isStreaming ? (
                  <Zap className="mr-2 h-4 w-4" />
                ) : (
                  <Clock className="mr-2 h-4 w-4" />
                )}
                Get Therapeutic Guidance
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

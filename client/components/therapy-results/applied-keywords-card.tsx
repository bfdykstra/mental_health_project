import type React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface AppliedKeywordsCardProps {
  keywords: string[];
}

export function AppliedKeywordsCard({ keywords }: AppliedKeywordsCardProps) {
  if (keywords.length === 0) return null;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg">Applied Keywords</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2">
          {keywords.map((keyword) => (
            <Badge key={keyword} variant="secondary">
              {keyword}
            </Badge>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

import type React from "react";
import { Brain } from "lucide-react";

export function HeroSection() {
  return (
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
  );
}

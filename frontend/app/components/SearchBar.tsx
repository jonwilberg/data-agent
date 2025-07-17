import { useState } from "react";
import { askQuestion, CensusApiError } from "../services/api";
import type { AgentResponse } from "../types/api";

interface SearchBarProps {
  compact?: boolean;
  onResponse?: (question: string, response: AgentResponse) => void;
  onQuestion?: (question: string) => void;
}

export function SearchBar({ compact = false, onResponse, onQuestion }: SearchBarProps) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const questionText = question.trim();
    setLoading(true);
    setError(null);
    setQuestion(""); // Clear input immediately

    // Add question to chat history immediately
    onQuestion?.(questionText);

    try {
      const result = await askQuestion(questionText);
      onResponse?.(questionText, result);
    } catch (err) {
      if (err instanceof CensusApiError) {
        setError(err.detail);
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={compact ? "w-full" : "w-full max-w-2xl mx-auto px-4 sm:px-0"}>
      <form onSubmit={handleSubmit}>
        <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
          <svg
            className="h-5 w-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={compact ? "Ask another question..." : "Ask about census data"}
          className={`w-full pl-12 pr-20 text-gray-900 bg-white border border-gray-200 rounded-2xl shadow-lg focus:outline-none focus:border-blue-200 focus:ring-0 placeholder-gray-400 ${
            compact ? "py-2 text-base" : "py-3 sm:py-4 text-base sm:text-lg"
          }`}
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className={`absolute right-2 top-1/2 transform -translate-y-1/2 aspect-square bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:cursor-not-allowed rounded-2xl flex items-center justify-center transition-colors duration-200 cursor-pointer ${
            compact ? "h-8 w-8" : "h-10 sm:h-12"
          }`}
        >
          {loading ? (
            <div className="animate-spin h-4 w-4 border-2 border-gray-600 border-t-transparent rounded-full"></div>
          ) : (
            <svg
              className="h-4 w-4 text-gray-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M9 5l7 7-7 7"
              />
            </svg>
          )}
        </button>
        </div>
      </form>
      
      {/* Error Display */}
      {error && (
        <div className="mt-3 bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">
          <p className="font-medium">Error:</p>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}
interface SuggestedPromptsProps {
  onPromptSelect: (prompt: string) => void;
}

export function SuggestedPrompts({ onPromptSelect }: SuggestedPromptsProps) {
  const prompts = [
    "Show me population by county",
    "Where are the richest areas in New York?",
    "Does income correlate with education?",
    "Where should I by a home in New York?",
    "Where should I open a grocery store in New York?"
  ];

  return (
    <div className="w-full max-w-4xl mx-auto px-4 mb-8">
      <div className="flex flex-wrap justify-center gap-4">
        {prompts.map((prompt, index) => (
          <button
            key={index}
            onClick={() => onPromptSelect(prompt)}
            className="flex items-center px-4 py-2 bg-white rounded-lg shadow-sm border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all duration-200 text-left group"
          >
            <span className="text-gray-700 group-hover:text-gray-900 font-medium">
              {prompt}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
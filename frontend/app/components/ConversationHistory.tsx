import { motion } from "framer-motion";
import type { AgentResponse } from "../types/api";

interface ConversationHistoryProps {
  conversations: Array<{
    question: string;
    response: AgentResponse;
    timestamp: Date;
  }>;
  onSelectChart?: (data: AgentResponse["data"]) => void;
}

export function ConversationHistory({ conversations, onSelectChart }: ConversationHistoryProps) {
  return (
    <div className="space-y-6">
      {conversations.map((conversation, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: index * 0.1 }}
          className="border-b border-gray-200 pb-6 last:border-b-0"
        >
          {/* Question */}
          <div className="mb-3">
            <div className="text-sm text-gray-500 mb-1">
              {conversation.timestamp.toLocaleTimeString()}
            </div>
            <div className="bg-blue-50 rounded-lg p-3">
              <p className="text-gray-800 font-medium">{conversation.question}</p>
            </div>
          </div>

          {/* Answer */}
          <div className="mb-3">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-700 leading-relaxed">
                {conversation.response.text_answer}
              </p>
            </div>
          </div>

          {/* Chart Data Preview */}
          {conversation.response.data && (
            <div className="ml-4">
              <button
                onClick={() => onSelectChart?.(conversation.response.data)}
                className="text-sm text-blue-600 hover:text-blue-800 bg-blue-50 hover:bg-blue-100 px-3 py-1 rounded-full transition-colors duration-200"
              >
                📊 View Chart: {conversation.response.data.chart_title}
              </button>
            </div>
          )}
        </motion.div>
      ))}
      
      {conversations.length === 0 && (
        <div className="text-center text-gray-500 py-8">
          <p>Ask your first question about census data to get started!</p>
        </div>
      )}
    </div>
  );
}
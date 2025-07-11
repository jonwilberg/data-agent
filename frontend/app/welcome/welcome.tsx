import { useState, useEffect } from "react";
import { SearchBar } from "../components/SearchBar";
import { ChartDisplay } from "../components/ChartDisplay";
import type { AgentResponse, ChartData } from "../types/api";

interface Conversation {
  question: string;
  response: AgentResponse | null;
  timestamp: Date;
}

type AnimationStage = 'welcome' | 'complete';

export function Welcome() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentChart, setCurrentChart] = useState<ChartData | null>(null);
  const [hasResults, setHasResults] = useState(false);
  const [animationStage, setAnimationStage] = useState<AnimationStage>('welcome');

  const handleNewQuestion = (question: string) => {
    const newConversation: Conversation = {
      question,
      response: null,
      timestamp: new Date(),
    };
    
    setConversations(prev => [...prev, newConversation]);
    setHasResults(true);
  };

  const handleNewResponse = (question: string, response: AgentResponse) => {
    setConversations(prev => {
      const updated = [...prev];
      const lastConversation = updated[updated.length - 1];
      if (lastConversation && lastConversation.question === question) {
        lastConversation.response = response;
      }
      return updated;
    });
    setCurrentChart(response.data);
  };

  // Handle animation sequence - just right panel slide-in
  useEffect(() => {
    if (hasResults && animationStage === 'welcome') {
      // Jump directly to split layout, then slide in right panel
      setTimeout(() => setAnimationStage('complete'), 100);
    }
  }, [hasResults, animationStage]);

  return (
    <main className="min-h-screen bg-gray-100">
      {!hasResults ? (
        <div className="flex items-center justify-center min-h-screen">
          <div className="w-full max-w-4xl px-4">
            <div className="mb-12 text-center">
              <h1 className="text-6xl font-bold text-gray-800 mb-4">
                Census Data Explorer
              </h1>
              <p className="text-xl text-gray-600">
                Ask natural language questions about US census data
              </p>
            </div>
            <SearchBar onResponse={handleNewResponse} onQuestion={handleNewQuestion} />
          </div>
        </div>
      ) : (
        <div className="flex min-h-screen">
          {/* Left Panel - Conversation History */}
          <div className="w-1/2 flex flex-col">
            <div className="flex-1 p-6 overflow-y-auto flex flex-col justify-end">
              <div className="space-y-6">
                {conversations.map((conversation, index) => (
                  <div key={index} className="pb-6">
                    <div className="mb-3 flex justify-end">
                      <div className="bg-blue-50 rounded-lg p-3 max-w-xs">
                        <p className="text-gray-800 font-medium">{conversation.question}</p>
                      </div>
                    </div>
                    <div className="mb-3">
                      {conversation.response ? (
                        <p className="text-gray-700 leading-relaxed">
                          {conversation.response.text_answer}
                        </p>
                      ) : (
                        <div className="flex items-center space-x-2 text-gray-500">
                          <div className="animate-spin h-4 w-4 border-2 border-gray-400 border-t-transparent rounded-full"></div>
                          <span>Thinking...</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Search Bar at Bottom of Left Panel */}
            <div className="px-4 py-2 pb-6">
              <SearchBar compact={true} onResponse={handleNewResponse} onQuestion={handleNewQuestion} />
            </div>
          </div>
          
          {/* Right Panel - Chart Display with Slide Animation */}
          <div className={`w-1/2 bg-white border-l border-gray-200 p-6 transform transition-all duration-500 ease-out flex flex-col justify-end ${
            animationStage === 'complete' ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'
          }`}>
            {currentChart ? (
              <div className="pb-12">
                <ChartDisplay data={currentChart} />
              </div>
            ) : null}
          </div>
        </div>
      )}
    </main>
  );
}
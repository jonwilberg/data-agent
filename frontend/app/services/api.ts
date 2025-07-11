/**
 * API service for Census Data Explorer
 */

import type { QuestionRequest, AgentResponse, ApiError } from "../types/api";

const API_BASE_URL = "http://localhost:8000";
const IS_MOCK_MODE = import.meta.env.VITE_MOCK_API === 'true';

export class CensusApiError extends Error {
  constructor(public detail: string, public status?: number) {
    super(detail);
    this.name = "CensusApiError";
  }
}

// Mock responses for development
const MOCK_RESPONSES: AgentResponse[] = [
  {
    text_answer: "Suffolk County has the highest median household income in New York at $89,283, followed by Nassau County at $87,658. These counties on Long Island consistently rank among the highest income areas in the state.",
    data: {
      values: [89283, 87658, 78456, 72341, 68922],
      labels: ["Suffolk", "Nassau", "Westchester", "Rockland", "Putnam"],
      x_axis_title: "County",
      y_axis_title: "Median Income ($)",
      chart_title: "Top 5 NY Counties by Median Household Income"
    },
    question: "",
    status: "success"
  },
  {
    text_answer: "New York County (Manhattan) has the highest population with 1,629,054 residents, followed by Kings County (Brooklyn) with 1,596,273 residents. These urban counties represent the most densely populated areas in the state.",
    data: {
      values: [1629054, 1596273, 1472654, 1385108, 953671],
      labels: ["New York", "Kings", "Queens", "Bronx", "Nassau"],
      x_axis_title: "County",
      y_axis_title: "Population",
      chart_title: "Top 5 Most Populous NY Counties"
    },
    question: "",
    status: "success"
  },
  {
    text_answer: "Hamilton County has the smallest population in New York with just 4,416 residents, making it the most rural county in the state. It's located in the Adirondack Mountains region.",
    data: {
      values: [4416, 4836, 6489, 12187, 13570],
      labels: ["Hamilton", "Essex", "Schuyler", "Yates", "Greene"],
      x_axis_title: "County",
      y_axis_title: "Population",
      chart_title: "5 Least Populous NY Counties"
    },
    question: "",
    status: "success"
  }
];

export async function askQuestion(question: string): Promise<AgentResponse> {
  // Mock mode for development
  if (IS_MOCK_MODE) {
    console.log("🎭 MOCK MODE: Simulating API call for:", question);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
    
    // Return random mock response
    const mockResponse = MOCK_RESPONSES[Math.floor(Math.random() * MOCK_RESPONSES.length)];
    const result = { ...mockResponse, question };
    
    console.log("✅ MOCK Response:", result);
    return result;
  }

  // Real API mode
  const request: QuestionRequest = { question };

  console.log("🚀 API Request:", {
    url: `${API_BASE_URL}/ask`,
    method: "POST",
    body: request,
  });

  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    console.log("📡 API Response Status:", {
      status: response.status,
      statusText: response.statusText,
      ok: response.ok,
    });

    if (!response.ok) {
      const errorData: ApiError = await response.json();
      console.error("❌ API Error Response:", errorData);
      throw new CensusApiError(errorData.detail, response.status);
    }

    const data: AgentResponse = await response.json();
    console.log("✅ API Success Response:", data);
    return data;
  } catch (error) {
    console.error("💥 API Call Failed:", error);
    
    if (error instanceof CensusApiError) {
      throw error;
    }
    
    // Network or other errors
    throw new CensusApiError(
      "Unable to connect to the census data service. Please try again later.",
      0
    );
  }
}
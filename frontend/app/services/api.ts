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
  // Bar Chart Response 1
  {
    text_answer: "Suffolk County has the highest median household income in New York at $89,283, followed by Nassau County at $87,658. These counties on Long Island consistently rank among the highest income areas in the state.",
    data: {
      chart_type: "bar",
      values: [89283, 87658, 78456, 72341, 68922],
      labels: ["Suffolk", "Nassau", "Westchester", "Rockland", "Putnam"],
      x_axis_title: "County",
      y_axis_title: "Median Income ($)",
      chart_title: "Top 5 NY Counties by Median Household Income"
    },
    question: "",
    status: "success"
  },
  // Bar Chart Response 2
  {
    text_answer: "New York County (Manhattan) has the highest population with 1,629,054 residents, followed by Kings County (Brooklyn) with 1,596,273 residents. These urban counties represent the most densely populated areas in the state.",
    data: {
      chart_type: "bar",
      values: [1629054, 1596273, 1472654, 1385108, 953671],
      labels: ["New York", "Kings", "Queens", "Bronx", "Nassau"],
      x_axis_title: "County",
      y_axis_title: "Population",
      chart_title: "Top 5 Most Populous NY Counties"
    },
    question: "",
    status: "success"
  },
  // Scatter Chart Response 1
  {
    text_answer: "There's a strong positive correlation between median household income and education level across NY counties. Counties with higher percentages of college graduates tend to have significantly higher median incomes, with correlation coefficients showing r > 0.75.",
    data: {
      chart_type: "scatter",
      x_values: [45.2, 52.8, 38.9, 41.7, 49.3, 35.6, 44.1, 39.8],
      y_values: [89283, 87658, 78456, 72341, 68922, 54320, 65780, 58940],
      labels: ["Suffolk", "Nassau", "Westchester", "Rockland", "Putnam", "Erie", "Monroe", "Onondaga"],
      x_axis_title: "College Graduates (%)",
      y_axis_title: "Median Income ($)",
      chart_title: "Income vs Education Level by County"
    },
    question: "",
    status: "success"
  },
  // Scatter Chart Response 2
  {
    text_answer: "Population density and housing costs show a clear relationship in NY counties. More densely populated areas like NYC boroughs command higher housing prices, while rural counties with lower density have more affordable housing markets.",
    data: {
      chart_type: "scatter",
      x_values: [72033, 37137, 21460, 34653, 4832, 1390, 2256, 8847],
      y_values: [2850, 1890, 1650, 2100, 980, 750, 820, 1250],
      labels: ["New York", "Kings", "Queens", "Bronx", "Nassau", "Hamilton", "Essex", "Oneida"],
      x_axis_title: "Population Density (per sq mile)",
      y_axis_title: "Median Home Value ($1000s)",
      chart_title: "Housing Costs vs Population Density"
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
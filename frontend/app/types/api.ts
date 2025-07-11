/**
 * TypeScript types for Census Data Explorer API
 */

export interface ChartData {
  values: number[];
  labels: string[];
  x_axis_title: string;
  y_axis_title: string;
  chart_title: string;
}

export interface QuestionRequest {
  question: string;
}

export interface AgentResponse {
  text_answer: string;
  data: ChartData | null;
  question: string;
  status: "success" | "error";
  error?: string;
}

export interface ApiError {
  detail: string;
}
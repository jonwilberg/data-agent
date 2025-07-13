/**
 * TypeScript types for Census Data Explorer API
 */

export type ChartType = "bar" | "scatter";

export interface BarChartData {
  chart_type: "bar";
  values: number[];
  labels: string[];
  x_axis_title: string;
  y_axis_title: string;
  chart_title: string;
}

export interface ScatterChartData {
  chart_type: "scatter";
  x_values: number[];
  y_values: number[];
  labels: string[];
  x_axis_title: string;
  y_axis_title: string;
  chart_title: string;
}

export type ChartData = BarChartData | ScatterChartData;

// Type guards
export const isBarChart = (data: ChartData): data is BarChartData => 
  data.chart_type === "bar";

export const isScatterChart = (data: ChartData): data is ScatterChartData => 
  data.chart_type === "scatter";

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
"""API models for data-agent."""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChartData(BaseModel):
    """Pydantic model for structured chart data."""
    
    values: List[float] = Field(description="Numeric values for the chart")
    labels: List[str] = Field(description="Labels for each value")
    x_axis_title: str = Field(description="Title for x-axis")
    y_axis_title: str = Field(description="Title for y-axis") 
    chart_title: str = Field(description="Main chart title")


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    
    question: str = Field(description="Natural language question about census data", min_length=1)


class AgentResponse(BaseModel):
    """Response model from the census data agent."""
    
    text_answer: str = Field(description="Natural language answer")
    data: Optional[ChartData] = Field(description="Chart data if available", default=None)
    question: str = Field(description="Original question")
    status: str = Field(description="Response status", default="success")
    error: Optional[str] = Field(description="Error message if status is error", default=None)
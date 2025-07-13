"""API models for data-agent."""

from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Union
from enum import StrEnum, auto


class ChartType(StrEnum):
    """Enumeration of supported chart types."""
    bar = auto()
    scatter = auto()


class BarChartData(BaseModel):
    """Pydantic model for bar chart data."""
    
    values: List[float] = Field(description="Numeric values for the bars")
    labels: List[str] = Field(description="Labels for each bar")
    x_axis_title: str = Field(description="Title for x-axis")
    y_axis_title: str = Field(description="Title for y-axis") 
    chart_title: str = Field(description="Main chart title")

    @computed_field
    def chart_type(self) -> ChartType:
        return ChartType.bar

class ScatterChartData(BaseModel):
    """Pydantic model for scatter chart data."""
    
    x_values: List[float] = Field(description="X-axis numeric values")
    y_values: List[float] = Field(description="Y-axis numeric values")
    labels: List[str] = Field(description="Labels for each data point")
    x_axis_title: str = Field(description="Title for x-axis")
    y_axis_title: str = Field(description="Title for y-axis")
    chart_title: str = Field(description="Main chart title")

    @computed_field
    def chart_type(self) -> ChartType:
        return ChartType.scatter


ChartData = Union[BarChartData, ScatterChartData]


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
"""API models for data-agent."""

from pydantic import BaseModel, Field
from typing import List


class ChartData(BaseModel):
    """Pydantic model for structured chart data."""
    
    values: List[float] = Field(description="Numeric values for the chart")
    labels: List[str] = Field(description="Labels for each value")
    x_axis_title: str = Field(description="Title for x-axis")
    y_axis_title: str = Field(description="Title for y-axis") 
    chart_title: str = Field(description="Main chart title")
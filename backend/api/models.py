"""API models for data-agent."""

from pydantic import BaseModel, Field, computed_field
from typing import List, Optional, Union
from enum import StrEnum, auto


class ChartType(StrEnum):
    """Enumeration of supported chart types."""
    bar = auto()
    scatter = auto()
    radar = auto()


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
    
    @classmethod
    def get_output_example(cls) -> str:
        return """
        {
            "values": [1000000, 850000, 750000, 600000, 500000],
            "labels": ["Kings County", "Queens County", "New York County", "Suffolk County", "Bronx County"],
            "x_axis_title": "County",
            "y_axis_title": "Population",
            "chart_title": "Top 5 Counties by Population"
        }
        """

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
    
    @classmethod
    def get_output_example(cls) -> str:
        return """
        {
            "x_values": [45000, 55000, 65000, 75000, 85000],
            "y_values": [25, 30, 35, 40, 45],
            "labels": ["Kings County", "Queens County", "New York County", "Suffolk County", "Bronx County"],
            "x_axis_title": "Median Income ($)",
            "y_axis_title": "Education Level (%)",
            "chart_title": "Income vs Education Correlation"
        }
        """


class RadarDataset(BaseModel):
    """Individual dataset for radar chart."""
    label: str = Field(description="Label for this dataset")
    data: List[float] = Field(description="Data values for this dataset")

class RadarChartData(BaseModel):
    """Pydantic model for radar chart data."""
    
    datasets: List[RadarDataset] = Field(description="Radar chart datasets with labels and data")
    axis_titles: List[str] = Field(description="Names of the radar chart axes/dimensions")
    chart_title: str = Field(description="Main chart title")

    @computed_field
    def chart_type(self) -> ChartType:
        return ChartType.radar
    
    @classmethod
    def get_output_example(cls) -> str:
        return """
        {
            "datasets": [
                {"label": "Kings County", "data": [1000000, 100000, 10000, 1000, 100]},
                {"label": "Queens County", "data": [500000, 50000, 5000, 500, 50]}
            ],
            "axis_titles": ["Population", "Median Income", "Education", "Housing", "Employment"],
            "chart_title": "Population stats for Kings and Queens counties"
        }
        """


ChartData = Union[BarChartData, ScatterChartData, RadarChartData]


class ChartTypeDecision(BaseModel):
    """Model for structured chart type selection."""
    
    chart_type: ChartType = Field(description="The recommended chart type for the data")
    reasoning: str = Field(description="Brief explanation for why this chart type was chosen")


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
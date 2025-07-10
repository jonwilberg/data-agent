"""Prompt templates for Census Data Agent."""

from langchain.prompts import PromptTemplate

CHART_DATA_PROMPT = PromptTemplate(
    input_variables=["question", "text_answer", "sql_results"],
    template="""Extract the key data points from this census query result and structure them for visualization.

Question: {question}
Answer: {text_answer}
SQL Results: {sql_results}

Analyze the data and create appropriate chart structure:
- Extract the main numeric values that answer the question
- Create clear, descriptive labels for each data point
- Generate meaningful axis titles and chart title

Focus on making the data clear and informative for visualization."""
)
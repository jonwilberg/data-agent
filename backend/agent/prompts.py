"""Prompt templates for Census Data Agent."""

SQL_PREFIX = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Your answer will be shown alongside a chart visualizing the data and you must summarize the findings for a non-technical audience in 1-2 paragraphs.
The chart will be based on the data returned by your query, not your written answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return "I don't know" as the answer.
"""

CHART_TYPE_DECISION_PROMPT = """Analyze the question and data to determine the most appropriate chart type.

Question: {question}
Answer: {text_answer}
Agent Execution Steps: {intermediate_steps}

Choose between BAR, SCATTER, and RADAR charts based on these guidelines:

BAR CHARTS - Use when:
- Single metric across multiple entities
- Comparing categories (counties, states, demographics)
- Ranking data (top 5, bottom 10, highest/lowest)

SCATTER PLOTS - Use when:
- Showing relationships between two variables
- Correlation analysis between different metrics
- Questions asking about connections, correlations, trends

RADAR CHARTS - Use when:
- Comparing multiple entities across multiple dimensions/metrics
- Multi-dimensional analysis (e.g., comparing counties on population, income, education, housing)
- Questions asking for comprehensive comparisons or profiles
- When you have 3+ metrics per entity that would benefit from a holistic view

Analyze the question intent and data structure from the agent's execution steps to make the best choice."""

BAR_CHART_DATA_PROMPT = """Extract data for a bar chart from this census query result.

Question: {question}
Answer: {text_answer}
Agent Execution Steps: {intermediate_steps}

Create a bar chart structure:
- Extract the main numeric values for comparison/ranking from the agent's execution steps
- Create clear labels for each bar (counties, categories, etc.)
- Generate meaningful axis titles and chart title
- Focus on categorical comparisons and rankings
- Use the full context from the agent's reasoning and SQL execution

Output example: {output_example}
"""

SCATTER_CHART_DATA_PROMPT = """Extract data for a scatter plot from this census query result.

Question: {question}
Answer: {text_answer}
Agent Execution Steps: {intermediate_steps}

Create a scatter plot structure:
- Identify TWO numeric variables that show a relationship from the agent's execution steps
- Extract x_values and y_values that demonstrate correlation
- Create labels for each data point (counties, entities, etc.)
- Generate meaningful axis titles that describe the relationship
- Focus on showing patterns and correlations between variables
- Use the full context from the agent's reasoning and SQL execution

Output example: {output_example}
"""

RADAR_CHART_DATA_PROMPT = """Extract data for a radar chart from this census query result.

Question: {question}
Answer: {text_answer}
Agent Execution Steps: {intermediate_steps}

Create a radar chart structure:
- Identify 1-5 entities (counties, areas, etc.) to compare
- Extract 3-6 numeric metrics per entity from the agent's execution steps
- Do NOT normalize or scale values
- Create datasets array with label and data for each entity
- Generate meaningful axis_titles for each dimension/metric
- Use the full context from the agent's reasoning and SQL execution

Output example: {output_example}
"""
"""Census Data Agent using LangChain."""

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent import AgentExecutor, AgentAction
from langchain.agents.agent_types import AgentType
from langchain_core.callbacks.stdout import StdOutCallbackHandler
from langchain_anthropic import ChatAnthropic
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from typing import Dict, Any, List, Tuple
import logging
import json
from datetime import datetime, date

from config import settings
from database.manager import db_manager
from agent.prompts import (
    SQL_PREFIX,
    CHART_TYPE_DECISION_PROMPT, 
    BAR_CHART_DATA_PROMPT, 
    SCATTER_CHART_DATA_PROMPT
)
from api.models import (
    ChartData, 
    AgentResponse, 
    ChartTypeDecision, 
    BarChartData, 
    ScatterChartData, 
    ChartType
)

logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


class CensusDataAgent:
    """Agent for answering questions about Census data."""
    
    llm: ChatAnthropic
    sql_db: SQLDatabase
    toolkit: SQLDatabaseToolkit
    agent: AgentExecutor
    
    def __init__(self) -> None:
        """Initialize the Census Data Agent."""
        
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            anthropic_api_key=settings.anthropic_api_key,
            temperature=0
        )
        
        self.sql_db = SQLDatabase(engine=db_manager.engine)
        
        self.toolkit = SQLDatabaseToolkit(db=self.sql_db, llm=self.llm)

        self.agent = create_sql_agent(
            prefix=SQL_PREFIX,
            top_k=20,
            llm=self.llm,
            toolkit=self.toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            agent_executor_kwargs={"return_intermediate_steps": True}
        )

    def ask_question(self, question: str) -> AgentResponse:
        """Ask a question about Census data.
        
        Args:
            question: Natural language question about Census data
            
        Returns:
            AgentResponse with answer and metadata
        """
        try:
            logger.info(f"Processing question: {question}")
            
            response = self.agent.invoke({"input": question})
            
            text_answer = response["output"]
            intermediate_steps = response["intermediate_steps"]
            chart_data = None
            
            if intermediate_steps:
                chart_data = self.generate_chart_data(
                    question=question,
                    text_answer=text_answer,
                    intermediate_steps=intermediate_steps
                )
            
            return AgentResponse(
                text_answer=text_answer,
                data=chart_data,
                question=question,
                status="success"
            )
            
        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return AgentResponse(
                question=question,
                text_answer=f"Sorry, I encountered an error: {str(e)}",
                data=None,
                status="error",
                error=str(e)
            )
    
    def determine_chart_type(self, question: str, text_answer: str, intermediate_steps: List[Tuple[AgentAction, str]]) -> ChartTypeDecision:
        """Determine the most appropriate chart type using structured output.
        
        Args:
            question: Original question
            text_answer: Text answer from SQL agent
            intermediate_steps: Full agent execution steps with context
            
        Returns:
            ChartTypeDecision with chart type and reasoning
        """
        try:
            chart_type_prompt = CHART_TYPE_DECISION_PROMPT.format(
                question=question,
                text_answer=text_answer,
                intermediate_steps=intermediate_steps
            )
            
            structured_llm = self.llm.with_structured_output(ChartTypeDecision)
            decision = structured_llm.invoke(chart_type_prompt)
            
            logger.info(f"Chart type decision: {decision.chart_type} - {decision.reasoning}")
            return decision
            
        except Exception as e:
            logger.warning(f"Could not determine chart type: {e}")
            return ChartTypeDecision(
                chart_type=ChartType.bar,
                reasoning="Default fallback to bar chart due to decision error"
            )

    def generate_chart_data(
            self, 
            question: str, 
            text_answer: str, 
            intermediate_steps: List[Tuple[AgentAction, str]]) -> ChartData:
        """Generate chart data using two-stage structured output approach.
        
        Args:
            question: Original question
            text_answer: Text answer from SQL agent
            intermediate_steps: Full agent execution steps with context
            
        Returns:
            Dictionary containing chart data or None if generation failed
        """
        try:
            chart_decision = self.determine_chart_type(question, text_answer, intermediate_steps)
            
            if chart_decision.chart_type == ChartType.bar:
                chart_prompt = BAR_CHART_DATA_PROMPT.format(
                    question=question,
                    text_answer=text_answer,
                    intermediate_steps=intermediate_steps
                )
                structured_llm = self.llm.with_structured_output(BarChartData)
            else:  # scatter
                chart_prompt = SCATTER_CHART_DATA_PROMPT.format(
                    question=question,
                    text_answer=text_answer,
                    intermediate_steps=intermediate_steps
                )
                structured_llm = self.llm.with_structured_output(ScatterChartData)
            
            chart_response = structured_llm.invoke(
                chart_prompt,
                config={"callbacks": [StdOutCallbackHandler()]}
            )
            
            logger.info(f"Generated {chart_decision.chart_type} chart data successfully")
            return chart_response
            
        except Exception as e:
            logger.warning(f"Could not generate chart data: {e}")
            return None


# Global agent instance
data_agent = CensusDataAgent()
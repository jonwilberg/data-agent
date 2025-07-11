"""Census Data Agent using LangChain."""

from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks.stdout import StdOutCallbackHandler
from langchain_anthropic import ChatAnthropic
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from typing import Dict, Any, List
import logging
import json
from datetime import datetime, date

from config import settings
from database.manager import db_manager
from agent.prompts import CHART_DATA_PROMPT
from api.models import ChartData, AgentResponse

logger = logging.getLogger(__name__)


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime objects."""
    
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)



class SQLResultsCapture(BaseCallbackHandler):
    """Callback handler to capture SQL query results during agent execution."""
    
    def __init__(self):
        self.sql_results: List[str] = []
        self.sql_queries: List[str] = []
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Capture tool outputs, specifically SQL query results."""
        tool_name = kwargs.get('name', '')
        if tool_name == 'sql_db_query':
            self.sql_results.append(output)
        elif tool_name == 'sql_db_query_checker':
            self.sql_queries.append(output)


class CensusDataAgent:
    """Agent for answering questions about Census data."""
    
    llm: ChatAnthropic
    sql_db: SQLDatabase
    toolkit: SQLDatabaseToolkit
    agent: Any
    
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
            llm=self.llm,
            toolkit=self.toolkit,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
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
            
            sql_capture = SQLResultsCapture()
            
            response = self.agent.invoke(
                {"input": question},
                config={"callbacks": [sql_capture]}
            )
            
            text_answer = response["output"]
            chart_data = None
            
            if sql_capture.sql_results:
                chart_data = self.generate_chart_data(
                    question=question,
                    text_answer=text_answer,
                    sql_results=sql_capture.sql_results[-1]
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
    
    def generate_chart_data(self, question: str, text_answer: str, sql_results: str) -> Dict[str, Any]:
        """Generate chart data from SQL results.
        
        Args:
            question: Original question
            text_answer: Text answer from SQL agent
            sql_results: Raw SQL query results
            
        Returns:
            Dictionary containing chart data or None if generation failed
        """
        try:
            chart_prompt = CHART_DATA_PROMPT.format(
                question=question,
                text_answer=text_answer,
                sql_results=sql_results
            )
            
            structured_llm = self.llm.with_structured_output(ChartData)
            chart_response = structured_llm.invoke(
                chart_prompt,
                config={"callbacks": [StdOutCallbackHandler()]}
            )
            
            return chart_response.dict()
        except Exception as e:
            logger.warning(f"Could not generate chart data: {e}")
            return None


# Global agent instance
data_agent = CensusDataAgent()
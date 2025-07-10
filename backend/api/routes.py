"""API routes for Census Data Agent."""

from fastapi import APIRouter, HTTPException
import logging

from api.models import QuestionRequest, AgentResponse
from agent.agent import data_agent

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/ask", response_model=AgentResponse, tags=["Census Data"])
async def ask_question(request: QuestionRequest) -> AgentResponse:
    """
    Ask a natural language question about census data.
    
    Returns both a text answer and structured chart data when applicable.
    """
    try:
        logger.info(f"Received question: {request.question}")
        
        # Call the census data agent
        response = data_agent.ask_question(request.question)
        
        logger.info(f"Successfully processed question with status: {response.status}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
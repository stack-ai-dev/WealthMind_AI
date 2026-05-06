"""
api/investment.py
-----------------
FastAPI Route Handlers

This file defines all the HTTP endpoints for WealthMind.
FastAPI automatically generates interactive docs at /docs

Endpoints:
  POST /analyze          - Full investment analysis (main pipeline)
  POST /chat             - Follow-up chat with memory
  GET  /simulate         - Quick growth simulation
  GET  /compare          - Compare two strategies
  GET  /market           - Live market data
  DELETE /session/{id}   - Clear memory
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.ai_module.app.schemas import UserProfile, ChatMessage, FullAdvice
from app.ai_module.app.graph import run_graph
from app.ai_module.app.engines.market_engine import get_market_summary
from app.ai_module.app.engines.simulation_engine import compare_strategies
from app.ai_module.app.agents.advisor_agent import chat_with_advisor
from app.ai_module.app.memory.memory_store import (
    add_message,
    get_chat_history,
    get_strategy_context,
    clear_session,
)

router = APIRouter()


# Request models for extra fields not in UserProfile 

class AnalyzeRequest(BaseModel):
    profile: UserProfile
    session_id: str = "default"
    monthly_contribution: float = 0.0
    explain_mode: str = "beginner"    # "beginner" or "investor"


class SimulateRequest(BaseModel):
    savings: float
    annual_income: float
    time_horizon: int
    expected_return: float
    monthly_contribution: float = 0.0
    goal: str = "retirement"


# Endpoints 

@router.post("/analyze", response_model=FullAdvice)
async def analyze_investment(request: AnalyzeRequest):
    """
    Main endpoint: runs the full LangGraph pipeline.
    
    Accepts user profile and returns:
    - Investment strategy with asset allocation
    - Risk score (ML model)
    - Growth simulation
    - Personalized explanation
    - Market context
    
    This is the core WealthMind API call.
    """
    try:
        advice = run_graph(
            profile=request.profile,
            session_id=request.session_id,
            monthly_contribution=request.monthly_contribution,
            explain_mode=request.explain_mode,
        )

        if advice is None:
            raise HTTPException(status_code=500, detail="Analysis failed to produce results")

        return advice

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@router.post("/chat")
async def chat(message: ChatMessage):
    """
    Chat endpoint with memory.
    
    The user can ask follow-up questions about their strategy.
    The AI remembers the strategy context from previous /analyze call.
    
    Example questions:
      "What if I increase crypto to 20%?"
      "Explain bonds to me like I'm 10"
      "Is my risk score too high?"
    """
    # Save user message to memory
    add_message(message.session_id, "human", message.user_message)

    # Get context and history
    chat_history = get_chat_history(message.session_id)
    strategy_context = get_strategy_context(message.session_id)

    # Get AI response (all history except the last message we just added)
    try:
        ai_response = chat_with_advisor(
            user_message=message.user_message,
            chat_history=chat_history[:-1],  # exclude the message we just added
            strategy_context=strategy_context,
        )
    except Exception as e:
        ai_response = f"I apologize, I encountered an error: {str(e)}"

    # Save AI response to memory
    add_message(message.session_id, "ai", ai_response)

    return {
        "response": ai_response,
        "session_id": message.session_id,
        "message_count": len(chat_history) + 1,
    }


@router.post("/simulate")
async def simulate(request: SimulateRequest):
    """
    Quick simulation endpoint — no LLM needed.
    
    Computes compound growth projection and returns
    year-by-year portfolio values.
    
    Used for the "What if I invest $X monthly?" feature.
    """
    # Build a minimal UserProfile just for simulation
    from app.ai_module.app.schemas import UserProfile
    mock_profile = UserProfile(
        name="User",
        age=30,
        income=request.annual_income,
        savings=request.savings,
        risk_tolerance="medium",
        goal=request.goal,
        time_horizon=request.time_horizon,
    )

    from app.ai_module.app.engines.simulation_engine import simulate_growth
    result = simulate_growth(
        profile=mock_profile,
        expected_annual_return=request.expected_return,
        monthly_contribution=request.monthly_contribution,
    )

    return result


@router.post("/compare")
async def compare(request: SimulateRequest):
    """
    Strategy comparison endpoint.
    Returns side-by-side comparison of aggressive vs conservative plans.
    """
    from app.ai_module.app.schemas import UserProfile
    mock_profile = UserProfile(
        name="User",
        age=30,
        income=request.annual_income,
        savings=request.savings,
        risk_tolerance="medium",
        goal=request.goal,
        time_horizon=request.time_horizon,
    )

    comparison = compare_strategies(
        profile=mock_profile,
        aggressive_return=request.expected_return,
        conservative_return=5.0,
    )

    return comparison


@router.get("/market")
async def market_data():
    """
    Live market data endpoint.
    Returns current prices for S&P 500, Nasdaq, Gold, Bonds, BTC, ETH.
    """
    summary = get_market_summary()
    return {"market_summary": summary}


@router.delete("/session/{session_id}")
async def clear_memory(session_id: str):
    """
    Clears all memory for a session.
    Use this to start fresh / reset the conversation.
    """
    clear_session(session_id)
    return {"message": f"Session {session_id} cleared successfully"}


@router.get("/health")
async def health_check():
    """Simple health check — confirms the API is running."""
    return {"status": "ok", "service": "WealthMind AI"}

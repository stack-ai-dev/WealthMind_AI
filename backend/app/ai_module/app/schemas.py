"""
schemas.py
----------
All Pydantic models (data shapes) used across the project.
Think of these as the "contracts" between different parts of the system.
"""

from pydantic import BaseModel
from typing import Optional, List


# What the user sends us 

class UserProfile(BaseModel):
    """The investor's personal details."""
    name: str
    age: int
    income: float          # annual income in USD
    savings: float         # amount available to invest
    risk_tolerance: str    # "low" | "medium" | "high"
    goal: str              # e.g. "retirement", "house", "college fund"
    time_horizon: int      # years until they need the money


class ChatMessage(BaseModel):
    """A single message in the conversation."""
    session_id: str
    user_message: str


# What we return 

class AllocationBreakdown(BaseModel):
    """How money is split across asset classes (percentages)."""
    stocks: float
    etfs: float
    bonds: float
    crypto: float
    cash: float


class InvestmentStrategy(BaseModel):
    """The full AI-generated investment plan."""
    profile_type: str            # e.g. "Moderate Growth Investor"
    risk_score: float            # 0-100 (from ML model)
    risk_label: str              # "Low" | "Medium" | "High"
    allocation: AllocationBreakdown
    expected_annual_return: float  # percentage
    confidence_score: float        # 0-100 how confident the AI is
    recommendations: List[str]
    risks: List[str]
    explanation: str             # plain-English summary from LLM


class SimulationResult(BaseModel):
    """Growth projection over time."""
    years: List[int]
    portfolio_values: List[float]
    final_value: float
    total_invested: float
    total_gain: float
    goal_progress_percent: float  # how close to their stated goal


class FullAdvice(BaseModel):
    """Everything bundled together for the API response."""
    strategy: InvestmentStrategy
    simulation: SimulationResult
    rag_insight: str             # extra wisdom pulled from our knowledge base
    market_summary: str          # live market data summary

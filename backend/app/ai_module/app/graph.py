"""
graph.py
--------
LangGraph Agent Workflow — The Brain of WealthMind

This file wires all the agents and engines together into a pipeline.
Each "node" is a function. Data flows from one node to the next.

Pipeline order:
  profile → strategy → risk → market → retrieve → simulate → advisor → memory

Think of it like an assembly line:
  Raw user input → ... → Final polished advice
"""

from typing import TypedDict, Optional, Any
from langgraph.graph import StateGraph, END

from app.ai_module.app.schemas import UserProfile, AllocationBreakdown, InvestmentStrategy, FullAdvice
from app.ai_module.app.agents.profile_agent import analyze_profile
from app.ai_module.app.agents.strategy_agent import generate_strategy
from app.ai_module.app.agents.advisor_agent import explain_strategy
from app.ai_module.app.engines.risk_engine import get_risk_score
from app.ai_module.app.engines.market_engine import get_market_summary
from app.ai_module.app.engines.simulation_engine import simulate_growth
from app.ai_module.app.rag.rag_store import retrieve_relevant_knowledge
from app.ai_module.app.memory.memory_store import save_strategy_context


# State Schema 


# This dict is passed between every node.
# Each node reads from it and adds its output to it.

class GraphState(TypedDict):
    # Input
    profile: UserProfile
    session_id: str
    monthly_contribution: float
    explain_mode: str            # "beginner" or "investor"

    # Intermediate outputs (filled in as we go)
    profile_type: str
    profile_summary: str
    rag_context: str
    market_summary: str
    risk_score: float
    risk_label: str
    strategy_data: dict          # raw dict from strategy_agent
    allocation: Optional[AllocationBreakdown]
    simulation: Optional[Any]

    # Final outputs
    full_advice: Optional[FullAdvice]
    error: Optional[str]


# Node Functions 
# Each node receives the full state and returns a partial update dict.

def node_profile(state: GraphState) -> dict:
    """
    Node 1: Analyze the user's financial profile.
    Calls the profile agent LLM to classify the investor type.
    """
    print("[Graph] Running: Profile Analyzer")
    try:
        result = analyze_profile(state["profile"])
        return {
            "profile_type": result["profile_type"],
            "profile_summary": result["summary"],
        }
    except Exception as e:
        # Graceful fallback — don't crash the whole pipeline
        print(f"[Graph] Profile agent error: {e}")
        return {
            "profile_type": "Moderate Growth Investor",
            "profile_summary": "Profile analyzed with default settings.",
        }


def node_rag_retrieve(state: GraphState) -> dict:
    """
    Node 2: Retrieve relevant investment knowledge from vector DB.
    Query is built from the user's goal and profile type.
    """
    print("[Graph] Running: RAG Retrieval")
    try:
        query = f"{state['profile_type']} {state['profile'].goal} investment strategy"
        context = retrieve_relevant_knowledge(query, k=3)
        return {"rag_context": context}
    except Exception as e:
        print(f"[Graph] RAG error: {e}")
        return {"rag_context": "Diversification and long-term investing are key principles."}


def node_market(state: GraphState) -> dict:
    """
    Node 3: Fetch live market data for context.
    """
    print("[Graph] Running: Market Data Fetch")
    try:
        summary = get_market_summary()
        return {"market_summary": summary}
    except Exception as e:
        print(f"[Graph] Market data error: {e}")
        return {"market_summary": "Market data temporarily unavailable."}


def node_strategy(state: GraphState) -> dict:
    """
    Node 4: Generate asset allocation strategy via LLM.
    Uses profile type, RAG context, and market data.
    """
    print("[Graph] Running: Strategy Generator")
    try:
        # First get a preliminary allocation with neutral risk score
        # We'll refine it after the ML model runs
        data = generate_strategy(
            profile=state["profile"],
            profile_type=state["profile_type"],
            risk_score=50.0,          # placeholder, ML refines below
            rag_context=state["rag_context"],
        )
        return {
            "strategy_data": data,
            "allocation": data["allocation"],
        }
    except Exception as e:
        print(f"[Graph] Strategy error: {e}")
        # Safe fallback allocation
        fallback_allocation = AllocationBreakdown(
            stocks=40, etfs=25, bonds=20, crypto=5, cash=10
        )
        return {
            "strategy_data": {
                "allocation": fallback_allocation,
                "expected_annual_return": 7.0,
                "confidence_score": 70,
                "recommendations": ["Diversify your portfolio"],
                "risks": ["Market volatility"],
                "explanation": "A balanced investment strategy.",
            },
            "allocation": fallback_allocation,
        }


def node_risk(state: GraphState) -> dict:
    """
    Node 5: Calculate risk score using rule-based + ML model blend.
    """
    print("[Graph] Running: Risk Engine (Rules + ML)")
    try:
        risk_score, risk_label = get_risk_score(
            profile=state["profile"],
            allocation=state["allocation"],
        )
        return {
            "risk_score": risk_score,
            "risk_label": risk_label,
        }
    except Exception as e:
        print(f"[Graph] Risk engine error: {e}")
        return {"risk_score": 50.0, "risk_label": "Medium"}


def node_simulate(state: GraphState) -> dict:
    """
    Node 6: Run compound growth simulation.
    """
    print("[Graph] Running: Simulation Engine")

    strategy_data = state["strategy_data"]
    profile = state["profile"]

    simulation = simulate_growth(
        profile=profile,
        expected_annual_return=strategy_data.get("expected_annual_return", 7.0),
        monthly_contribution=state.get("monthly_contribution", 0.0),
    )

    return {"simulation": simulation}


def node_advisor(state: GraphState) -> dict:
    """
    Node 7: Generate final human-readable advice + assemble FullAdvice object.
    """
    print("[Graph] Running: Advisor Agent")

    strategy_data = state["strategy_data"]
    allocation = state["allocation"]
    profile = state["profile"]

    # Get plain-English explanation from advisor agent
    try:
        explanation = explain_strategy(
            profile_type=state["profile_type"],
            risk_score=state["risk_score"],
            allocation=allocation.model_dump(),
            expected_return=strategy_data.get("expected_annual_return", 7.0),
            recommendations=strategy_data.get("recommendations", []),
            explain_mode=state.get("explain_mode", "beginner"),
        )
    except Exception as e:
        print(f"[Graph] Advisor agent error: {e}")
        explanation = strategy_data.get("explanation", "Strategy generated successfully.")

    # Build the final InvestmentStrategy object
    investment_strategy = InvestmentStrategy(
        profile_type=state["profile_type"],
        risk_score=state["risk_score"],
        risk_label=state["risk_label"],
        allocation=allocation,
        expected_annual_return=strategy_data.get("expected_annual_return", 7.0),
        confidence_score=strategy_data.get("confidence_score", 75),
        recommendations=strategy_data.get("recommendations", []),
        risks=strategy_data.get("risks", []),
        explanation=explanation,
    )

    # Bundle everything
    full_advice = FullAdvice(
        strategy=investment_strategy,
        simulation=state["simulation"],
        rag_insight=state["rag_context"][:300] + "...",   # first 300 chars
        market_summary=state["market_summary"],
    )

    return {"full_advice": full_advice}


def node_memory(state: GraphState) -> dict:
    """
    Node 8: Save strategy to memory for future chat turns.
    """
    print("[Graph] Running: Memory Store")

    advice = state.get("full_advice")
    if advice:
        # Create a compact text summary of the strategy
        strategy = advice.strategy
        context = (
            f"Profile: {strategy.profile_type} | "
            f"Risk: {strategy.risk_score}/100 ({strategy.risk_label}) | "
            f"Allocation: Stocks {strategy.allocation.stocks}%, "
            f"ETFs {strategy.allocation.etfs}%, "
            f"Bonds {strategy.allocation.bonds}%, "
            f"Crypto {strategy.allocation.crypto}%, "
            f"Cash {strategy.allocation.cash}% | "
            f"Expected Return: {strategy.expected_annual_return}%"
        )
        save_strategy_context(state["session_id"], context)

    return {}   # no state changes needed


# Build the Graph

def build_graph():
    """
    Assembles all nodes into a LangGraph StateGraph.
    Returns a compiled, runnable graph.
    """
    workflow = StateGraph(GraphState)

    # Add each node
    workflow.add_node("profile", node_profile)
    workflow.add_node("rag_retrieve", node_rag_retrieve)
    workflow.add_node("market", node_market)
    workflow.add_node("strategy", node_strategy)
    workflow.add_node("risk", node_risk)
    workflow.add_node("simulate", node_simulate)
    workflow.add_node("advisor", node_advisor)
    workflow.add_node("memory", node_memory)

    # Define the flow: profile → rag → market → strategy → risk → simulate → advisor → memory → END
    workflow.set_entry_point("profile")
    workflow.add_edge("profile", "rag_retrieve")
    workflow.add_edge("rag_retrieve", "market")
    workflow.add_edge("market", "strategy")
    workflow.add_edge("strategy", "risk")
    workflow.add_edge("risk", "simulate")
    workflow.add_edge("simulate", "advisor")
    workflow.add_edge("advisor", "memory")
    workflow.add_edge("memory", END)

    return workflow.compile()


# Compile once at import time (so FastAPI doesn't recompile on every request)
wealthmind_graph = build_graph()


def run_graph(
    profile: UserProfile,
    session_id: str,
    monthly_contribution: float = 0.0,
    explain_mode: str = "beginner",
) -> FullAdvice:
    """
    Main entry point: runs the full WealthMind pipeline.

    Args:
        profile: user's financial profile
        session_id: unique ID for memory/chat continuity
        monthly_contribution: extra monthly investment amount
        explain_mode: "beginner" or "investor"

    Returns:
        FullAdvice with complete strategy, simulation, and explanation
    """
    initial_state = {
        "profile": profile,
        "session_id": session_id,
        "monthly_contribution": monthly_contribution,
        "explain_mode": explain_mode,
        # All other fields start as None/empty and get filled in
        "profile_type": "",
        "profile_summary": "",
        "rag_context": "",
        "market_summary": "",
        "risk_score": 50.0,
        "risk_label": "Medium",
        "strategy_data": {},
        "allocation": None,
        "simulation": None,
        "full_advice": None,
        "error": None,
    }

    result = wealthmind_graph.invoke(initial_state)
    return result["full_advice"]

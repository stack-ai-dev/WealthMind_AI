import json
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.ai_module.app.schemas import UserProfile, AllocationBreakdown


STRATEGY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert investment strategist.
            Generate a personalized investment strategy based on the user's profile.

            You MUST respond with valid JSON only — no explanation, no markdown, just raw JSON.

            JSON format:
            {{
                "stocks": <number 0-100>,
                "etfs": <number 0-100>,
                "bonds": <number 0-100>,
                "crypto": <number 0-100>,
                "cash": <number 0-100>,
                "expected_annual_return": <number like 8.5>,
                "confidence_score": <number 0-100>,
                "recommendations": ["rec1", "rec2", "rec3"],
                "risks": ["risk1", "risk2"],
                "explanation": "plain English summary of the strategy"
            }}

            Rules:
            - All allocation numbers must add up to exactly 100
            - Conservative profiles: more bonds and cash, less crypto
            - Aggressive profiles: more stocks and crypto, fewer bonds
            - Higher risk_score = more aggressive allocation
            """,
    ),
    (
        "human",
        """
        Investor Profile:
        - Profile Type: {profile_type}
        - Age: {age}
        - Goal: {goal}
        - Time Horizon: {time_horizon} years
        - Risk Tolerance: {risk_tolerance}
        - Risk Score (ML model output, 0-100): {risk_score}
        - RAG Context (investment wisdom): {rag_context}
        """,
    ),
])


def generate_strategy(
    profile: UserProfile,
    profile_type: str,
    risk_score: float,
    rag_context: str,
) -> dict:
    """
    Calls the LLM to generate an investment strategy.
    
    Returns a dict that matches our InvestmentStrategy schema.
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",  
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),  
        base_url="https://openrouter.ai/api/v1"
    )

    chain = STRATEGY_PROMPT | llm

    response = chain.invoke({
        "profile_type": profile_type,
        "age": profile.age,
        "goal": profile.goal,
        "time_horizon": profile.time_horizon,
        "risk_tolerance": profile.risk_tolerance,
        "risk_score": risk_score,
        "rag_context": rag_context,
    })

    # Parse JSON from LLM response
    strategy_data = _parse_json_response(response.content)

    # Build AllocationBreakdown object
    allocation = AllocationBreakdown(
        stocks=strategy_data.get("stocks", 40),
        etfs=strategy_data.get("etfs", 25),
        bonds=strategy_data.get("bonds", 20),
        crypto=strategy_data.get("crypto", 5),
        cash=strategy_data.get("cash", 10),
    )

    return {
        "allocation": allocation,
        "expected_annual_return": strategy_data.get("expected_annual_return", 7.0),
        "confidence_score": strategy_data.get("confidence_score", 75),
        "recommendations": strategy_data.get("recommendations", []),
        "risks": strategy_data.get("risks", []),
        "explanation": strategy_data.get("explanation", ""),
    }


def _parse_json_response(text: str) -> dict:
    """
    Safely parse JSON from LLM response.
    If parsing fails, return safe default values.
    """
    try:
        # Strip any accidental markdown code fences
        clean = text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except json.JSONDecodeError:
        # Fallback defaults if LLM returns bad JSON
        print("[WARN] Could not parse LLM JSON response, using defaults")
        return {
            "stocks": 40, "etfs": 25, "bonds": 20, "crypto": 5, "cash": 10,
            "expected_annual_return": 7.0,
            "confidence_score": 70,
            "recommendations": ["Diversify your portfolio", "Review annually"],
            "risks": ["Market volatility", "Inflation risk"],
            "explanation": "A balanced investment strategy tailored to your profile.",
        }

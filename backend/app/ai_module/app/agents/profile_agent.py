from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.ai_module.app.schemas import UserProfile
import os


# The prompt template we send to the LLM
PROFILE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a financial profile analyzer.
           Given a user's details, produce a short investor profile.

           Respond in this exact format (no extra text):
           PROFILE_TYPE: <type>
           SUMMARY: <one sentence about their situation>
           KEY_FACTORS: <comma-separated list of 3 key factors>

           Profile types to choose from:
            - Conservative Saver
            - Balanced Investor  
            - Moderate Growth Investor
            - Aggressive Growth Investor
            - Speculative Investor
    """,
    ),
    (
        "human",
        """
            Name: {name}
            Age: {age}
            Annual Income: ${income}
            Available Savings: ${savings}
            Risk Tolerance: {risk_tolerance}
            Investment Goal: {goal}
            Time Horizon: {time_horizon} years
        """,
    ),
])


def analyze_profile(profile: UserProfile) -> dict:
    """
    Sends user profile to LLM and gets back a structured profile type.
    
    Returns a dict with:
      - profile_type: e.g. "Moderate Growth Investor"
      - summary: one-sentence description
      - key_factors: list of important factors
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",  
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),  
        base_url="https://openrouter.ai/api/v1"
    )

    chain = PROFILE_PROMPT | llm   # LangChain "pipe" 

    response = chain.invoke({
        "name": profile.name,
        "age": profile.age,
        "income": profile.income,
        "savings": profile.savings,
        "risk_tolerance": profile.risk_tolerance,
        "goal": profile.goal,
        "time_horizon": profile.time_horizon,
    })

    # Parse the structured text response
    result = _parse_profile_response(response.content)
    return result


def _parse_profile_response(text: str) -> dict:
    """
    Parses the LLM's text output into a Python dict.
    Example input:
      PROFILE_TYPE: Moderate Growth Investor
      SUMMARY: Young professional with medium risk appetite
      KEY_FACTORS: age, income stability, long time horizon
    """
    lines = text.strip().split("\n")
    result = {
        "profile_type": "Moderate Growth Investor",  # safe default
        "summary": "",
        "key_factors": [],
    }

    for line in lines:
        if line.startswith("PROFILE_TYPE:"):
            result["profile_type"] = line.split(":", 1)[1].strip()
        elif line.startswith("SUMMARY:"):
            result["summary"] = line.split(":", 1)[1].strip()
        elif line.startswith("KEY_FACTORS:"):
            factors_str = line.split(":", 1)[1].strip()
            result["key_factors"] = [f.strip() for f in factors_str.split(",")]

    return result

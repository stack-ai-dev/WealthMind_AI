import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage


# Explanation prompt 

EXPLAIN_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are WealthMind, a friendly AI financial advisor.
            Explain the investment strategy to the user.

            Mode: {explain_mode}
            - If mode is "beginner": use simple words, avoid jargon, use analogies
            - If mode is "investor": use professional financial terminology

            Keep it under 150 words. Be encouraging and clear.
        """,
    ),
    (
        "human",
        """Here is the investment strategy to explain:

            Profile Type: {profile_type}
            Risk Score: {risk_score}/100
            Allocation: Stocks {stocks}%, ETFs {etfs}%, Bonds {bonds}%, Crypto {crypto}%, Cash {cash}%
            Expected Return: {expected_return}% annually
            Key Recommendations: {recommendations}
        """,
    ),
])


# Chat prompt (uses memory) 

CHAT_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are WealthMind, a helpful AI financial advisor.
            You remember the user's investment strategy and answer their questions.
            Be concise, friendly, and accurate. Do not give illegal financial advice.

            User's Strategy Context:
            {strategy_context}
        """,
    ),
    MessagesPlaceholder(variable_name="chat_history"),  # injects past messages
    ("human", "{user_message}"),
])


def explain_strategy(
    profile_type: str,
    risk_score: float,
    allocation: dict,
    expected_return: float,
    recommendations: list,
    explain_mode: str = "beginner",
) -> str:
    """
    Generates a plain-English explanation of the strategy.
    explain_mode: "beginner" or "investor"
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",  
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),  
        base_url="https://openrouter.ai/api/v1"
   )

    chain = EXPLAIN_PROMPT | llm

    response = chain.invoke({
        "explain_mode": explain_mode,
        "profile_type": profile_type,
        "risk_score": risk_score,
        "stocks": allocation.get("stocks", 0),
        "etfs": allocation.get("etfs", 0),
        "bonds": allocation.get("bonds", 0),
        "crypto": allocation.get("crypto", 0),
        "cash": allocation.get("cash", 0),
        "expected_return": expected_return,
        "recommendations": ", ".join(recommendations),
    })

    return response.content


def chat_with_advisor(
    user_message: str,
    chat_history: list,    # list of HumanMessage / AIMessage objects
    strategy_context: str, # summary of current strategy
) -> str:
    """
    Handles follow-up questions with memory of past conversation.
    
    chat_history: previous messages stored in memory_store
    Returns: the AI's reply as a string
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",  
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),  
        base_url="https://openrouter.ai/api/v1"
    )

    chain = CHAT_PROMPT | llm

    response = chain.invoke({
        "strategy_context": strategy_context,
        "chat_history": chat_history,
        "user_message": user_message,
    })

    return response.content

"""
Memory System - Chat History Storage

Stores conversation history per session so the AI remembers context.
Uses a simple in-memory dict for now (can swap to Redis or a database).

Each session has:
  - chat_history: list of HumanMessage/AIMessage objects
    strategy_context: the last generated strategy (as text)
  - user_profile: the user's profile data
"""

from typing import Dict, List, Optional
from langchain_core.messages import HumanMessage, AIMessage
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessionMemory:
    """All memory for one user session."""
    session_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    chat_history: List = field(default_factory=list)   # HumanMessage / AIMessage
    strategy_context: str = ""
    user_name: str = ""
    last_risk_score: Optional[float] = None


# Global storage: session_id -> SessionMemory
# In production, replace with Redis or a database
_sessions: Dict[str, SessionMemory] = {}


def get_or_create_session(session_id: str) -> SessionMemory:
    """Gets existing session or creates a new one."""
    if session_id not in _sessions:
        _sessions[session_id] = SessionMemory(session_id=session_id)
        print(f"[Memory] Created new session: {session_id}")
    return _sessions[session_id]


def add_message(session_id: str, role: str, content: str) -> None:
    """
    Adds a message to the session's chat history.

    role: "human" or "ai"
    content: the message text
    """
    session = get_or_create_session(session_id)

    if role == "human":
        session.chat_history.append(HumanMessage(content=content))
    else:
        session.chat_history.append(AIMessage(content=content))


def get_chat_history(session_id: str) -> List:
    """Returns the full chat history for a session."""
    session = get_or_create_session(session_id)
    return session.chat_history


def save_strategy_context(session_id: str, strategy_summary: str) -> None:
    """
    Saves the current strategy as context for future chat turns.
    The advisor agent uses this to answer follow-up questions.
    """
    session = get_or_create_session(session_id)
    session.strategy_context = strategy_summary


def get_strategy_context(session_id: str) -> str:
    """Gets the saved strategy context for a session."""
    session = get_or_create_session(session_id)
    return session.strategy_context or "No strategy generated yet."


def clear_session(session_id: str) -> None:
    """Clears all memory for a session (fresh start)."""
    if session_id in _sessions:
        del _sessions[session_id]
        print(f"[Memory] Cleared session: {session_id}")


def get_session_count() -> int:
    """Returns how many active sessions exist (for monitoring)."""
    return len(_sessions)

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.api.users import get_current_user
from pydantic import BaseModel

from app.ai_module.app.schemas import UserProfile, ChatMessage, FullAdvice
from app.ai_module.app.graph import run_graph

router = APIRouter(prefix="/ai", tags=["AI"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  


# Request model
class AnalyzeRequest(BaseModel):
    profile: UserProfile
    session_id: str = "default"
    monthly_contribution: float = 0.0
    explain_mode: str = "beginner"  # beginner/investor


# Protected AI endpoint
@router.post("/analyze", response_model=FullAdvice)
def analyze_investment(request: AnalyzeRequest, current_user: dict = Depends(get_current_user)):
    """
    Protected AI endpoint.
    Only accessible if user is logged in and has valid JWT.
    """
    try:
        advice = run_graph(
            profile=request.profile,
            session_id=request.session_id,
            monthly_contribution=request.monthly_contribution,
            explain_mode=request.explain_mode,
        )
        if advice is None:
            raise HTTPException(status_code=500, detail="AI analysis failed")
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")
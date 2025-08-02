from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import ai.chat as ai

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get('/chat/{content}')
async def chat(content):
    session_id = "alice5"
    try:
        return StreamingResponse(
            ai.chat(content, session_id),
            media_type="text/plain")
    except Exception as e:
        return {"error": str(e)}
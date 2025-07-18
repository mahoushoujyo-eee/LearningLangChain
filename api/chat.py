from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import ai.chat as ai

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get('/chat/{content}')
async def chat(content):
    return StreamingResponse(
        ai.chat(content),
        media_type="text/plain")
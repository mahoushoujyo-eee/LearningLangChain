from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import ai.chat as ai

router = APIRouter(prefix="/ai", tags=["ai"])

async def async_generator_wrapper(async_gen):
    """将异步生成器包装为同步生成器供 StreamingResponse 使用"""
    async for item in async_gen:
        yield item

@router.get('/chat/{content}')
async def chat(content):
    try:
        return StreamingResponse(
            async_generator_wrapper(ai.chat(content)),
            media_type="text/plain")
    except Exception as e:
        return {"error": str(e)}
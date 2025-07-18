from config.logger import logger as log
from ai.model import get_chain

async def chat(content: str, session_id: str):
    chain = get_chain()
    async for chunk in chain.astream({"input": content},
        config={"configurable": {"session_id": session_id}}):
        # Agent 返回的是字典格式，需要处理不同的数据结构
        if isinstance(chunk, dict):
            # Agent 的输出在 'output' 键中
            if 'output' in chunk:
                content_text = chunk['output']
                log.info(content_text)
                yield content_text
            # 处理中间步骤的输出
            elif 'actions' in chunk or 'steps' in chunk:
                log.info(f"Agent 中间步骤: {chunk}")
                # 中间步骤不向用户输出
                continue
            else:
                # 其他字典内容
                log.info(f"Agent 输出: {chunk}")
                yield str(chunk)
        else:
            # 兼容原来的消息格式
            if hasattr(chunk, 'content'):
                log.info(chunk.content)
                yield chunk.content
            else:
                log.info(str(chunk))
                yield str(chunk)

import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain_community.chat_message_histories import SQLChatMessageHistory


# 异步包装器类
class AsyncSQLChatMessageHistory:
    def __init__(self, session_id: str, connection: str):
        self.session_id = session_id
        self.connection = connection
        self._history = None
        self._executor = ThreadPoolExecutor(max_workers=1)
    
    def _get_history(self):
        if self._history is None:
            self._history = SQLChatMessageHistory(
                session_id=self.session_id,
                connection_string=self.connection
            )
        return self._history
    
    async def aget_messages(self):
        loop = asyncio.get_event_loop()
        def get_messages():
            history = self._get_history()
            return list(history.messages)  # 确保返回消息列表的副本
        return await loop.run_in_executor(self._executor, get_messages)
    
    async def aadd_message(self, message):
        loop = asyncio.get_event_loop()
        def add_message():
            history = self._get_history()
            history.add_message(message)
            return None
        return await loop.run_in_executor(self._executor, add_message)
    
    async def aadd_messages(self, messages):
        loop = asyncio.get_event_loop()
        def add_messages():
            history = self._get_history()
            for message in messages:
                history.add_message(message)
            return None
        return await loop.run_in_executor(self._executor, add_messages)
    
    async def aclear(self):
        loop = asyncio.get_event_loop()
        def clear_history():
            history = self._get_history()
            history.clear()
            return None
        return await loop.run_in_executor(self._executor, clear_history)
    
    def add_message(self, message):
        return self._get_history().add_message(message)
    
    def add_messages(self, messages):
        history = self._get_history()
        for message in messages:
            history.add_message(message)
        return None
    
    def add_ai_message(self, message):
        return self._get_history().add_ai_message(message)
    
    def add_user_message(self, message):
        return self._get_history().add_user_message(message)
    
    def clear(self):
        return self._get_history().clear()
    
    @property
    def messages(self):
        return self._get_history().messages
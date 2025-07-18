from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool
from operator import itemgetter
from ai.mcp import get_all_tools
import asyncio
import os
import anyio


# ------------- 工具示例 -------------
@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    try:
        result = eval(expression)
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

# 创建消息修剪器 - 使用消息数量限制更安全
trimmer = trim_messages(
    max_tokens=10,  # 保留最近10条消息
    strategy="last",  # 保留最后的消息
    token_counter=len,  # 使用消息数量作为计数器
    include_system=True,  # 保留系统消息
    start_on="human",  # 确保以人类消息开始
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    google_api_key="AIzaSyCpTrnTei0clJ92vH4V6wJm03xaL_BBGs0",
)

# ------------- 提示模板 -------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的 AI 助手，记住用户说过的话，必要时可调用工具。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# 添加调试函数来打印消息
def debug_messages(x):
    print(f"Debug - 输入数据: {x}")
    if 'chat_history' in x:
        print(f"Debug - 历史消息数量: {len(x['chat_history'])}")
        for i, msg in enumerate(x['chat_history']):
            print(f"Debug - 历史消息 {i}: {msg}")
    if 'input' in x:
        print(f"Debug - 用户输入: {x['input']}")
    return x

global chain_with_history


def create_chat_message_history(session_id: str) -> SQLChatMessageHistory:
    """创建 SQL 聊天消息历史实例"""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="mysql+pymysql://langchain:langchain123@127.0.0.1:3306/langchain"
    )

# async def get_async_history(session_id: str):
#     return await anyio.to_thread(create_chat_message_history, session_id)


async def init_agent():
    global chain_with_history
    
    tools = [calculator]

    mcp_tools = await get_all_tools()
    tools.extend(mcp_tools)

    # 使用全局的llm变量并绑定工具
    llm_with_tools = llm.bind_tools(tools)
    # ------------- 创建 Agent -------------
    agent = create_tool_calling_agent(llm_with_tools, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,               # 控制台打印 ReAct 过程
        max_iterations=5,
        handle_parsing_errors=True
    )

    # 创建带有消息修剪和调试的agent链
    enhanced_agent = (
        RunnablePassthrough.assign(chat_history=itemgetter("chat_history") | trimmer)
        | debug_messages
        | agent_executor
    )

    # ------------- 绑定 MySQL 记忆 -------------
    chain_with_history = RunnableWithMessageHistory(
        enhanced_agent,
        create_chat_message_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

def get_agent():
    return chain_with_history

# mcp_tools = asyncio.run(get_all_tools())
# tools.extend(mcp_tools)


#-lite-preview-06-17"
# llm = ChatOpenAI(
#     temperature=0.1,
#     model_name="deepseek-r1-0528", 
#     openai_api_base="https://api.qnaigc.com/v1", # 例如，您可以指定base_url
#     openai_api_key="sk-d1485a93f87c3c0add520ca9a97d507cb810537de27ac5d9a72f2b6ba4651a0d", # 直接在此处设置API密钥，或者通过环境变量设置
# )







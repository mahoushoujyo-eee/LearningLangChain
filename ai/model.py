from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import Prompt, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    google_api_key="AIzaSyCpTrnTei0clJ92vH4V6wJm03xaL_BBGs0.",  # 字符串形式
    # stream=True
)

# 创建消息修剪器
trimmer = trim_messages(
    max_tokens=20,  # 或者使用 max_messages=10 来限制消息数量
    strategy="last",  # 保留最后的消息
    token_counter=len,  # 使用您的模型来计算token
    include_system=True,  # 保留系统消息
    start_on="human",  # 确保以人类消息开始
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是助手，记住用户说过的话。"),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

# 修正chain结构：只对history应用trimmer
chain = (
    RunnablePassthrough.assign(history=itemgetter("history") | trimmer)
    | prompt 
    | llm
)

# 添加调试函数来打印消息
def debug_messages(x):
    print(f"Debug - 输入数据: {x}")
    if 'history' in x:
        print(f"Debug - 历史消息数量: {len(x['history'])}")
        for i, msg in enumerate(x['history']):
            print(f"Debug - 历史消息 {i}: {msg}")
    if 'input' in x:
        print(f"Debug - 用户输入: {x['input']}")
    return x

# 在chain中添加调试
chain = (
    RunnablePassthrough.assign(history=itemgetter("history") | trimmer)
    | debug_messages
    | prompt 
    | llm
)

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id,
        connection="mysql+pymysql://langchain:langchain123@127.0.0.1:3306/langchain"
    ),
    input_messages_key="input",
    history_messages_key="history"
)
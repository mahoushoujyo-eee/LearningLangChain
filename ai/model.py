from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.prompts import Prompt, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    google_api_key="AIzaSyCpTrnTei0clJ92vH4V6wJm03xaL_BBGs0.",  # 字符串形式
    # stream=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是助手，记住用户说过的话。"),
    ("placeholder", "{history}"),
    ("human", "{input}")
])
chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id,
        connection="mysql+pymysql://langchain:langchain123@127.0.0.1:3306/langchain"
    ),
    input_messages_key="input",
    history_messages_key="history"
)
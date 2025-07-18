from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI

embeddings = OpenAIEmbeddings(
    api_key="sk-a4d9b8b15f6a494b92491f3b6f2129f2",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # 按需选择模型
    model="text-embedding-v4",
    check_embedding_ctx_length=False,   # 关键参数
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite-preview-06-17",
    google_api_key="AIzaSyCpTrnTei0clJ92vH4V6wJm03xaL_BBGs0",
)

# 示例：构建检索器
vectorstore = Chroma.from_texts(["八嘎鸭肉是一种很好吃的鸭肉，不过吃的太多对身体有害"], embeddings)
retriever = vectorstore.as_retriever()

# 构建 RAG chain
prompt = ChatPromptTemplate.from_template(
    "根据以下上下文回答问题：{context}\n问题：{question}"
) 

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
rag_tool = rag_chain.as_tool(
    name="rag_tool",
    description="基于知识库回答八嘎鸭肉相关问题"
)
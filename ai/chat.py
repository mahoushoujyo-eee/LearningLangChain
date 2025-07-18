from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import Prompt, ChatPromptTemplate, HumanMessagePromptTemplate
from config.logger import logger as log
from ai.model import chain_with_history

def chat(content:str):
    session_id = "alice2"
    for chunk in chain_with_history.stream({"input": content},
        config={"configurable": {"session_id": session_id}}):
        log.info(chunk.content)
        yield chunk.content

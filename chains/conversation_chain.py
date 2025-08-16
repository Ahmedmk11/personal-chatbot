from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory

from prompts.conversation_prompt import conversation_prompt
from utils.llm_fallback import with_fallback

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
FALLBACK_MODEL_NAME = os.getenv("FALLBACK_MODEL_NAME")

# ===============================
# Memory
# ===============================

class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: list[BaseMessage]) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

# ===============================
# LLM
# ===============================

primary_llm = ChatGroq(
    model_name=MODEL_NAME,
    temperature=0.3,
    api_key=GROQ_API_KEY
)

fallback_llm = ChatGroq(
    model_name=FALLBACK_MODEL_NAME,
    temperature=0.3,
    api_key=GROQ_API_KEY
)

# ===============================
# Conversation Chain
# ===============================

conversation_chain = RunnableWithMessageHistory(
    with_fallback(primary_llm, fallback_llm, conversation_prompt),
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
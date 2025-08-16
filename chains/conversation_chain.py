from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain

from prompts import conversation_prompt

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===============================
# Memory
# ===============================

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=False
)

# ===============================
# LLM
# ===============================

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

# ===============================
# Conversation Chain
# ===============================

llm_chain = LLMChain(
    llm=llm,
    prompt=conversation_prompt,
    output_key="response",
)

conversation_chain = ConversationChain(
    llm=llm_chain,
    memory=memory,
    verbose=True
)
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# import json
from langchain.chains import SequentialChain
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import ConversationChain

from langchain.memory import ConversationBufferMemory

# ==================================
# Environment Variables
# ==================================

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("GROQ_API_KEY:", GROQ_API_KEY)

# ==================================
# Memory Initialization
# ==================================

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=False)

# ==================================
# LLM Initialization
# ==================================

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

conversation = LLMChain(
    llm=llm, 
    memory=memory,
    verbose=True
)

# ==================================
# Prompt Templates
# ==================================

# first_prompt = ChatPromptTemplate.from_template()

# ==================================
# Chain Definitions
# ==================================

# general_chain = LLMChain(llm=llm, prompt=first_prompt, output_key="")

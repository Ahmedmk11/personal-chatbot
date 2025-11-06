from langchain_groq import ChatGroq
from prompts.redirect_prompt import redirect_prompt
import os
from dotenv import load_dotenv
from utils.llm_fallback import with_fallback

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
FALLBACK_MODEL_NAME = os.getenv("FALLBACK_MODEL_NAME")

# ===============================
# LLMs
# ===============================

primary_llm = ChatGroq(
    model_name=MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
    streaming=True
)

fallback_llm = ChatGroq(
    model_name=FALLBACK_MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
    streaming=True
)

# ===============================
# Redirect chain with fallback
# ===============================

redirect_chain = with_fallback(
    primary_llm,
    fallback_llm,
    redirect_prompt
)

from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableBranch

from prompts.router_prompt import router_prompt
from chains.conversation_chain import conversation_chain
from chains.retrieval_chain import retrieval_chain
from chains.redirect_chain import redirect_chain
from utils.llm_fallback import with_fallback

import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
FALLBACK_MODEL_NAME = os.getenv("FALLBACK_MODEL_NAME")

# ===============================
# Router LLM
# ===============================

primary_router_llm = ChatGroq(
    model_name=MODEL_NAME,
    temperature=0.0,
    api_key=GROQ_API_KEY
)

fallback_router_llm = ChatGroq(
    model_name=FALLBACK_MODEL_NAME,
    temperature=0.0,
    api_key=GROQ_API_KEY
)

# ===============================
# Router LLM
# ===============================

router_llm_chain = with_fallback(primary_router_llm, fallback_router_llm, router_prompt, False)

# ===============================
# Router chain
# ===============================

def get_route(input_data):
    route = router_llm_chain.invoke(input_data).content.strip().lower()
    return route

router_chain = RunnableBranch(
    (lambda x: get_route(x) == "retrieval", retrieval_chain),
    (lambda x: get_route(x) == "redirect", redirect_chain),
    conversation_chain
)
from langchain_groq import ChatGroq
from prompts.router_prompt import router_prompt
from chains.retrieval_chain import retrieval_chain
from chains.redirect_chain import redirect_chain
from utils.llm_fallback import with_fallback
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
FALLBACK_MODEL_NAME = os.getenv("FALLBACK_MODEL_NAME")

# ===============================
# Router LLMs
# ===============================

primary_router_llm = ChatGroq(
    model_name=MODEL_NAME,
    temperature=0.0,
    api_key=GROQ_API_KEY,
    streaming=True
)

fallback_router_llm = ChatGroq(
    model_name=FALLBACK_MODEL_NAME,
    temperature=0.0,
    api_key=GROQ_API_KEY,
    streaming=True
)

# ===============================
# Router LLM Chain (Async)
# ===============================

router_llm_chain = with_fallback(primary_router_llm, fallback_router_llm, router_prompt, parser=False)

# ===============================
# Router function (Async)
# ===============================

async def get_route(input_data):
    """Run router LLM asynchronously and return route name."""
    result = await router_llm_chain.ainvoke(input_data)
    route = result.content.strip().lower() if hasattr(result, "content") else str(result).strip().lower()
    return route

# ===============================
# Router chain (Async)
# ===============================

async def route_input(input_data, config=None):
    route = await get_route(input_data)
    route = route.lower()
    
    if route == "retrieval":
        async for chunk in retrieval_chain.astream(input_data, config=config or {}):
            yield chunk
    elif route == "redirect":
        async for chunk in redirect_chain.astream(input_data, config=config or {}):
            yield chunk

router_chain = RunnableLambda(route_input)

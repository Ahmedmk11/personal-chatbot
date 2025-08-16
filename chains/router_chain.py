from langchain_groq import ChatGroq
from langchain.chains.router import RouterChain
from langchain.chains import LLMChain
from prompts.router_prompt import router_prompt

from chains.conversation_chain import conversation_chain
from chains.retrieval_chain import retrieval_chain
from chains.redirect_chain import redirect_chain

import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===============================
# Router LLM
# ===============================

router_llm = ChatGroq(
    model_name="llama-3.3-7b-versatile",
    temperature=0.0,
    api_key=GROQ_API_KEY
)

# ===============================
# LLMChain for routing
# ===============================

router_llm_chain = LLMChain(llm=router_llm, prompt=router_prompt)

# ===============================
# RouterChain
# ===============================

router_chain = RouterChain.from_llm(
    router_llm_chain,
    default_chain_key="conversation",
    return_all_outputs=False
)

router_chain.chains = {
    "redirect": redirect_chain,
    "retrieval": retrieval_chain,
    "conversation": conversation_chain
}

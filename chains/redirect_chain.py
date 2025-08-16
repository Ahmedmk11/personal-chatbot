from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from prompts.redirect_prompt import redirect_prompt
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===============================
# LLM for redirect chain
# ===============================

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0,
    api_key=GROQ_API_KEY
)

# ===============================
# Redirect chain
# ===============================

redirect_chain = LLMChain(
    llm=llm,
    prompt=redirect_prompt,
    output_key="redirect_response",
    verbose=True
)

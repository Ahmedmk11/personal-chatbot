from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from prompts.retrieval_prompt import retrieval_prompt
from utils.llm_fallback import with_fallback
import os
from dotenv import load_dotenv

from langchain_core.runnables import RunnableLambda

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
# FAISS
# ===============================

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

retriever = FAISS.load_local(
    "data/vectorstore",
    embeddings_model,
    allow_dangerous_deserialization=True
).as_retriever(search_kwargs={"k": 10})

# ===============================
# Retrieval pipeline (async safe)
# ===============================

async def get_context(x):
    docs = await retriever.ainvoke(x["input"])
    return "\n".join(doc.page_content for doc in docs)

get_context_runnable = RunnableLambda(get_context)

retrieval_chain = {
    "input": lambda x: x["input"],
    "retrieved_context": get_context_runnable
} | with_fallback(primary_llm, fallback_llm, retrieval_prompt)

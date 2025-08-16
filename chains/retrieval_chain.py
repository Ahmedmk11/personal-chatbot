from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from prompts.retrieval_prompt import retrieval_prompt
from utils.llm_fallback import with_fallback

from langchain_core.runnables import RunnableMap
from utils.llm_fallback import with_fallback

import os
from dotenv import load_dotenv

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
    api_key=GROQ_API_KEY
)

fallback_llm = ChatGroq(
    model_name=FALLBACK_MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY
)

# ===============================
# FAISS
# ===============================

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
retriever = FAISS.load_local(
    "data/vectorstore",
    embeddings_model,
    allow_dangerous_deserialization=True
).as_retriever()

# ===============================
# Retrieval pipeline with fallback
# ===============================

retrieval_chain = RunnableMap({
    "input": lambda x: x["input"],
    "retrieved_context": lambda x: "\n".join(
        [doc.page_content for doc in retriever.get_relevant_documents(x["input"], k=10)]
    )
}) | with_fallback(primary_llm, fallback_llm, retrieval_prompt)

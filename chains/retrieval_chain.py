from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate

import os
from dotenv import load_dotenv

from prompts import retrieval_prompt

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ===============================
# LLM
# ===============================

llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=GROQ_API_KEY
)

# ===============================
# LLMChain with retrieval prompt
# ===============================

retrieval_llm_chain = LLMChain(
    llm=llm,
    prompt=retrieval_prompt,
    output_key="response"
)

# ===============================
# FAISS
# ===============================

retriever = FAISS.load_local("data").as_retriever()

# ===============================
# Retrieval Chain
# ===============================

retrieval_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": retrieval_prompt}
)

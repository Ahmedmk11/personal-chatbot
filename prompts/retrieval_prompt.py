from langchain.prompts import PromptTemplate

retrieval_prompt = PromptTemplate(
    input_variables=["input", "retrieved_context"],
    template="""
You are representing Ahmed, a software engineer. Use the context below to answer the user's question naturally and concisely.
Do not copy text verbatim. Only include the most relevant information. Make it conversational and human-like.

Context:
{retrieved_context}

User Question:
{input}

Answer naturally and concisely:
"""
)

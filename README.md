# Personal Chatbot

A FastAPI-based AI chatbot representing Ahmed, a software engineer. Uses LangChain, Groq LLM, and FAISS for retrieval, conversation, and redirection.

## Features

- **Conversational AI**: Chat naturally with context from Ahmed’s portfolio and CV
- **Context Retrieval**: Pulls relevant documents for accurate answers
- **Chain Routing**: Routes queries to conversation, retrieval, or redirect chains
- **Memory Support**: Remembers previous messages per session

## Tech Stack

- Python 3.11+
- FastAPI
- LangChain, LangChain-Groq
- Groq API (LLM)
- FAISS & HuggingFace embeddings

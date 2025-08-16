from langchain.prompts import PromptTemplate

conversation_prompt = PromptTemplate(
    input_variables=["chat_history", "input"],
    template="""
You are Ahmed’s friendly and professional chatbot. 
Keep the conversation casual, natural, and engaging. 
Answer in a way that feels like talking to a human.

Conversation so far:
{chat_history}

User: {input}
Chatbot:"""
)

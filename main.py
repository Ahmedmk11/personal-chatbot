from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chains.router_chain import router_chain
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

session_histories = {}

class UserQuery(BaseModel):
    query: str
    session_id: str = None

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.post("/chat", response_model=ChatResponse)
async def chat(query: UserQuery):
    try:
        logger.info(f"Received query: {query.query}")
        
        session_id = query.session_id or str(uuid.uuid4())
        
        previous_messages = session_histories.get(session_id, [])
        
        input_with_memory = {
            "input": query.query,
            "history": previous_messages
        }
        
        config = {
            "configurable": {
                "session_id": session_id
            }
        }
        
        response = await router_chain.ainvoke(input_with_memory, config=config)
        
        if hasattr(response, 'content'):
            response_text = response.content
        elif isinstance(response, str):
            response_text = response
        elif isinstance(response, dict) and 'output' in response:
            response_text = response['output']
        elif isinstance(response, dict) and 'answer' in response:
            response_text = response['answer']
        else:
            response_text = str(response)
        
        previous_messages.append({"user": query.query, "bot": response_text})
        session_histories[session_id] = previous_messages
        
        logger.info(f"Generated response: {response_text}")
        
        return ChatResponse(response=response_text, status="success")
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Personal Chatbot API is running!"}

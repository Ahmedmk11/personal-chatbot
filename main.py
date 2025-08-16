from fastapi import FastAPI
from pydantic import BaseModel
from chains.router_chain import router_chain

app = FastAPI()

class UserQuery(BaseModel):
    query: str

@app.post("/chat")
def chat(query: UserQuery):
    response = router_chain.run(query.query)
    return {"response": response}

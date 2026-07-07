from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from agent import get_agent
from langchain_core.messages import HumanMessage, SystemMessage

app = FastAPI(title="LangGraph AI Agent API")

class ChatRequest(BaseModel):
    messages: List[str] 
    system_prompt: str
    model_name: str
    allow_search: bool

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        agent = get_agent(
            model_name=request.model_name,
            system_prompt=request.system_prompt,
            allow_search=request.allow_search
        )
        
        user_message = request.messages[-1]
        
        # Version-proof fix: We manually inject the system prompt right here
        messages_to_send = [
            SystemMessage(content=request.system_prompt),
            HumanMessage(content=user_message)
        ]
        
        result = agent.invoke({"messages": messages_to_send})
        ai_response = result["messages"][-1].content
        
        return ChatResponse(response=ai_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
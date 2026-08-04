from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_client import generate_response

router = APIRouter()

# Definimos cómo debe ser la petición que nos envíen
class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_llm(request: PromptRequest):
    # Aquí es donde más adelante pondremos los cronómetros y guardrails
    ai_response = await generate_response(request.prompt)
    
    return {
        "status": "success",
        "original_prompt": request.prompt,
        "response": ai_response
    }
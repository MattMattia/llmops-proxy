from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.llm_client import generate_response
from app.guardrails.prompt_check import is_safe_prompt
import logging

router = APIRouter()
logger = logging.getLogger("LLMOps")

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_llm(request: PromptRequest):
    # 1. Pasamos el prompt por la barrera de seguridad
    is_safe, reason = is_safe_prompt(request.prompt)
    
    # 2. Si detecta peligro, cortamos la conexión inmediatamente
    if not is_safe:
        logger.warning(f"🚨 [ALERTA DE SEGURIDAD] Intento de inyección bloqueado. Razón: {reason}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El mensaje contiene instrucciones no permitidas por las políticas de seguridad."
        )

    # 3. Si el mensaje es limpio, le permitimos llegar a la IA local
    ai_response = await generate_response(request.prompt)
    
    return {
        "status": "success",
        "original_prompt": request.prompt,
        "response": ai_response
    }
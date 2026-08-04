from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.llm_client import generate_response
from app.guardrails.prompt_check import is_safe_prompt
from app.guardrails.pii_filter import mask_sensitive_data  # <-- Nueva importación
import logging

router = APIRouter()
logger = logging.getLogger("LLMOps")

class PromptRequest(BaseModel):
    prompt: str

@router.post("/chat")
async def chat_with_llm(request: PromptRequest):
    # 1. Verificamos que no sea un ataque de inyección
    is_safe, reason = is_safe_prompt(request.prompt)
    if not is_safe:
        logger.warning(f"🚨 [ALERTA] Intento de inyección bloqueado: {reason}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mensaje bloqueado por políticas de seguridad."
        )

    # 2. Censuramos datos sensibles (PII)
    cleaned_prompt = mask_sensitive_data(request.prompt)
    
    # Opcional: logueamos si el prompt fue modificado
    if cleaned_prompt != request.prompt:
        logger.info("🛡️ [DLP] Datos sensibles detectados y censurados.")

    # 3. Enviamos el prompt LIMPIO a la IA
    ai_response = await generate_response(cleaned_prompt)
    
    return {
        "status": "success",
        "original_prompt": request.prompt,      # Lo que mandó el usuario
        "clean_prompt": cleaned_prompt,         # Lo que realmente vio la IA
        "response": ai_response
    }
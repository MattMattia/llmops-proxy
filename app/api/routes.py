from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.services.llm_client import generate_response
from app.guardrails.prompt_check import is_safe_prompt
from app.guardrails.pii_filter import mask_sensitive_data
from app.core.metrics import SECURITY_BLOCKED_COUNTER, DLP_MASKED_COUNTER
import logging

router = APIRouter()
logger = logging.getLogger("LLMOps")

class PromptRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="El texto de entrada para el LLM")

class PromptResponse(BaseModel):
    status: str
    original_prompt: str
    clean_prompt: str
    response: str

@router.post("/chat", response_model=PromptResponse, status_code=status.HTTP_200_OK)
async def chat_with_llm(request: PromptRequest):
    """
    Endpoint principal del proxy LLMOps:
    1. Valida guardrails de seguridad (inyecciones).
    2. Aplica filtro DLP para enmascarar PII.
    3. Envía el prompt limpio al LLM de forma asincrónica.
    4. Registra métricas en Prometheus.
    """
    user_prompt = request.prompt

    # 1. Verificación de seguridad (Guardrails)
    is_safe, reason = is_safe_prompt(user_prompt)
    if not is_safe:
        logger.warning(f"🚨 [ALERTA] Intento de inyección bloqueado: {reason}")
        SECURITY_BLOCKED_COUNTER.inc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mensaje bloqueado por políticas de seguridad."
        )

    # 2. Filtrado y enmascaramiento de datos sensibles (DLP)
    cleaned_prompt = mask_sensitive_data(user_prompt)
    if cleaned_prompt != user_prompt:
        logger.info("🛡️ [DLP] Datos sensibles detectados y censurados.")
        DLP_MASKED_COUNTER.inc()

    # 3. Invocación asincrónica al cliente del LLM
    ai_response = await generate_response(cleaned_prompt)
    
    return PromptResponse(
        status="success",
        original_prompt=user_prompt,
        clean_prompt=cleaned_prompt,
        response=ai_response
    )
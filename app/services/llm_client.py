import httpx
import logging
import asyncio
from fastapi import HTTPException, status

logger = logging.getLogger("LLMOps")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"
MAX_RETRIES = 2        # Reducimos a 2 intentos para no demorar si hay fallos
TIMEOUT_SECONDS = 10.0 # Bajamos el timeout a 10 segundos para respuestas locales ágiles

async def generate_response(prompt: str) -> str:
    """
    Envía el prompt al LLM de forma asincrónica con reintentos rápidos y timeout ajustado.
    """
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(OLLAMA_URL, json=payload, timeout=TIMEOUT_SECONDS)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
                
                logger.warning(f"⚠️ [LLM] Ollama respondió con código inesperado: {response.status_code}")

        except (httpx.TimeoutException, httpx.ConnectError) as e:
            logger.warning(f"⚠️ [LLM] Error de conexión en el intento {attempt}: {str(e)}")
            if attempt == MAX_RETRIES:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="El servicio de IA no está disponible temporalmente."
                )
            # Pausa muy breve (0.5s) para reintentar rápido sin bloquear
            await asyncio.sleep(0.5 * attempt)
            
        except Exception as e:
            logger.error(f"❌ [LLM] Error crítico inesperado: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno procesando la respuesta de la IA."
            )
            
    return "Error conectando con la IA."
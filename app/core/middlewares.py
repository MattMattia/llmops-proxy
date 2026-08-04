import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Configuramos el sistema de logs para que imprima bonito en la consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("LLMOps")

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f} sec"
        
        # Reemplazamos el print() por logger.info()
        logger.info(f"Ruta: {request.url.path} | Latencia: {process_time:.4f} segundos")
        
        return response
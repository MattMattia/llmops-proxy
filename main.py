from fastapi import FastAPI
from app.api.routes import router
from app.core.middlewares import TimingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator # <-- 1. Importación

app = FastAPI(title="LLMOps Proxy", version="1.0.0")

app.add_middleware(TimingMiddleware)
app.include_router(router, prefix="/api/v1")

# <-- 2. Activamos el instrumentador de métricas
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Proxy interceptor funcionando"}
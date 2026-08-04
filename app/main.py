from fastapi import FastAPI
from app.api.routes import router
from app.core.middlewares import TimingMiddleware  # <-- Nueva importación

app = FastAPI(title="LLMOps Proxy", version="1.0.0")

# Activamos el middleware (se ejecuta en TODAS las peticiones)
app.add_middleware(TimingMiddleware)  # <-- Activación

# Conectamos las rutas
app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Proxy interceptor funcionando"}
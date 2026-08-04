from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="LLMOps Proxy", version="1.0.0")

# Conectamos las rutas
app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Proxy interceptor funcionando"}
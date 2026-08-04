from fastapi import FastAPI

app = FastAPI(title="LLMOps Proxy", version="1.0.0")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Proxy interceptor funcionando"}
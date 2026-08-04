import httpx

# Ollama se ejecuta por defecto en este puerto local
OLLAMA_URL = "http://localhost:11434/api/generate"

async def generate_response(prompt: str) -> str:
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    # Usamos httpx para hacer la consulta de forma asíncrona
    async with httpx.AsyncClient() as client:
        response = await client.post(OLLAMA_URL, json=payload, timeout=60.0)
        
    if response.status_code == 200:
        return response.json().get("response", "")
    return "Error conectando con la IA."
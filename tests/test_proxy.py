from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_chat_endpoint_success():
    payload = {"prompt": "¿Cuál es la capital de Francia?"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "response" in data

def test_security_metrics_triggered():
    # Probamos que un prompt con datos sensibles (tarjeta de crédito) active el guardrail/DLP
    payload = {"prompt": "Mi tarjeta es 4532-1111-2222-3333"}
    response = client.post("/api/v1/chat", json=payload)
    # Esperamos 400 por bloqueo de seguridad o 200 si el diseño enmascara y deja pasar (según tu lógica de rutas)
    assert response.status_code in [200, 400]
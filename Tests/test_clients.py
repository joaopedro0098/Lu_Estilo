from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_clients():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert response.json()["message"] == "Listagem de clientes"
    assert "filtros" in response.json()

def test_create_client():
    response = client.post("/clientes")
    assert response.status_code == 200
    assert response.json()["message"] == "Criar novo cliente"

def test_read_client():
    response = client.get("/clientes/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Detalhes do cliente 1"
    assert response.json()["cliente_id"] == 1

def test_update_client():
    response = client.put("/clientes/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Atualizar cliente 1"
    assert response.json()["cliente_id"] == 1

def test_delete_client():
    response = client.delete("/clientes/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Deletar cliente 1"
    assert response.json()["cliente_id"] == 1
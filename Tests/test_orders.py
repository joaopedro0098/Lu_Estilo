from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_orders():
    response = client.get("/pedidos")
    assert response.status_code == 200
    assert response.json()["message"] == "Listagem de pedidos"
    assert "filtros" in response.json()

def test_create_order():
    response = client.post("/pedidos")
    assert response.status_code == 200
    assert response.json()["message"] == "Criar novo pedido"

def test_read_order():
    response = client.get("/pedidos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Detalhes do pedido 1"
    assert response.json()["pedido_id"] == 1

def test_update_order():
    response = client.put("/pedidos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Atualizar pedido 1"
    assert response.json()["pedido_id"] == 1

def test_delete_order():
    response = client.delete("/pedidos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Deletar pedido 1"
    assert response.json()["pedido_id"] == 1
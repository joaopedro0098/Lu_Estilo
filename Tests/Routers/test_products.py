from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_products():
    response = client.get("/produtos")
    assert response.status_code == 200
    assert response.json()["message"] == "Listagem de produtos"
    assert "filtros" in response.json()

def test_create_product():
    response = client.post("/produtos")
    assert response.status_code == 200
    assert response.json()["message"] == "Criar novo produto"

def test_read_product():
    response = client.get("/produtos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Detalhes do produto 1"
    assert response.json()["produto_id"] == 1

def test_update_product():
    response = client.put("/produtos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Atualizar produto 1"
    assert response.json()["produto_id"] == 1

def test_delete_product():
    response = client.delete("/produtos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Deletar produto 1"
    assert response.json()["produto_id"] == 1
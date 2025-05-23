from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_categories():
    response = client.get("/categorias")
    assert response.status_code == 200
    assert response.json()["message"] == "Lista de categorias"
    assert "categorias" in response.json()

def test_read_products_by_category():
    response = client.get("/categorias/tenis") 
    assert response.status_code == 200
    assert response.json()["message"] == "Produtos da categoria tenis"
    assert response.json()["categoria"] == "tenis"

def test_read_products_by_category_and_section():
    response = client.get("/categorias/tenis/masculino") 
    assert response.status_code == 200
    assert response.json()["message"] == "Produtos da categoria tenis na seção masculino"
    assert response.json()["categoria"] == "tenis"
    assert response.json()["secao"] == "masculino"

def test_create_category():
    response = client.post("/categorias")
    assert response.status_code == 200
    assert response.json()["message"] == "Criar nova categoria"

def test_update_category():
    response = client.put("/categorias/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Atualizar categoria 1"

def test_delete_category():
    response = client.delete("/categorias/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Deletar categoria 1"
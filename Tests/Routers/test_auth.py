from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post("/auth/register")  
    assert response.status_code == 200
    assert response.json()["message"] == "Registro de novo usuário"  

def test_login():
    response = client.post("/auth/login") 
    assert response.status_code == 200
    assert response.json()["message"] == "Autenticação de usuário" 

def test_refresh_token():
    response = client.post("/auth/refresh-token")  
    assert response.status_code == 200
    assert response.json()["message"] == "Refresh de token JWT"  
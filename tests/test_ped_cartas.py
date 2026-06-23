import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_criar_pedido(client):
    response = client.post("/pedidos",
        json={
            "user": "Jose",
            "produto": "Black Lotus",
            "quantidade": 1
        }
    )
    assert response.status_code in [200, 201]

def test_listar_pedidos(client):
    response = client.get("/pedidos")
    assert response.status_code == 200

def test_atualizar_pedido(client):
    setup_response = client.post("/pedidos",
        json={
            "user": "Liliana",
            "produto": "Counterspell",
            "quantidade": 2
        }
    )
    assert setup_response.status_code in [200, 201]
    pedido_id = setup_response.json().get("id") or 1
    response = client.put(f"/pedidos/{pedido_id}",
        json={
            "user": "Liliana",
            "produto": "Counterspell",
            "quantidade": 5
        }
    )
    assert response.status_code in [200, 201]

def test_deletar_pedido(client):
    setup_response = client.post("/pedidos",
        json={
            "user": "Lucas",
            "produto": "Lightning Bolt",
            "quantidade": 4
        }
    )
    assert setup_response.status_code in [200, 201]
    pedido_id = setup_response.json().get("id") or 1
    response = client.delete(f"/pedidos/{pedido_id}")
    assert response.status_code in [200, 204]

def test_deletar_pedido_inexistente(client):
    response = client.delete("/pedidos/99999")
    assert response.status_code == 404

def test_atualizar_pedido_inexistente(client):
    response = client.put(
        "/pedidos/99999",
        json={
            "user": "Inexistente",
            "produto": "Fogo",
            "quantidade": 1
        }
    )
    assert response.status_code == 404
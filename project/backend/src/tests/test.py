from fastapi.testclient import TestClient
from src import main

client: TestClient = TestClient(main.app)

def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI is running"}


def test_create_and_get_items() -> None:
    response = client.post("/items", json={"name": "Test", "description": "Example"})
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "Test"

    response = client.get("/items")
    assert response.status_code == 200
    assert any(i["name"] == "Test" for i in response.json())


def test_delete_item() -> None:
    client.post("/items", json={"name": "DeleteMe", "description": "Temp"})
    client.post("/items", json={"name": "KeepMe", "description": "Leave me"})
    response = client.delete("/items/3")
    assert response.status_code == 200
    assert response.json()["name"] == "KeepMe"


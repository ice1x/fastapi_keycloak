from fastapi.testclient import TestClient
import pytest
from src import main
from src.auth import get_current_user

client: TestClient = TestClient(main.app)


@pytest.fixture
def mock_basic_user() -> dict:
    return {"username": "testuser", "roles": ["user"]}


@pytest.fixture(autouse=True)
def override_user_dependency(mock_basic_user: dict) -> None:
    main.app.dependency_overrides[get_current_user] = lambda: mock_basic_user
    yield
    main.app.dependency_overrides = {}


def test_create_item_forbidden() -> None:
    response = client.post("/items", json={"name": "Nope", "description": "Should fail"})
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


def test_delete_item_forbidden() -> None:
    response = client.delete("/items/1")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden"


@pytest.mark.usefixtures("override_user_dependency")
def test_get_items_allowed_for_basic_user(override_user_dependency) -> None:
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

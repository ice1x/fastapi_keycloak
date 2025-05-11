import pytest
from src.api import items_db
from src.auth import get_current_user


@pytest.fixture(autouse=True)
def clear_items_db() -> None:
    items_db.clear()


@pytest.fixture
def mock_admin_user() -> dict:
    return {"username": "admin", "roles": ["admin"]}


@pytest.fixture(autouse=True)
def override_user_dependency(mock_admin_user: dict) -> None:
    from src import main
    main.app.dependency_overrides[get_current_user] = lambda: mock_admin_user
    yield
    main.app.dependency_overrides = {}

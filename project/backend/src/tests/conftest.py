import pytest
from src.api import items_db
from src.auth import get_current_user


@pytest.fixture(autouse=True)
def clear_items_db() -> None:
    items_db.clear()


@pytest.fixture
def mock_admin_user() -> dict:
    return {"username": "admin", "roles": ["admin"]}


@pytest.fixture
def mock_user_no_roles() -> dict:
    return {"username": "test", "roles": []}


@pytest.fixture
def override_user_dependency():
    from src import main

    def _override(user: dict):
        main.app.dependency_overrides[get_current_user] = lambda: user

    yield _override
    main.app.dependency_overrides = {}

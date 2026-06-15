from fastapi.testclient import TestClient

from core.auth import require_auth
from main import app


def test_get_me_returns_authenticated_user_claims():
    app.dependency_overrides[require_auth] = lambda: {
        "sub": "auth0|test-user",
        "email": "runner@example.com",
        "permissions": ["read:profile"],
    }

    try:
        with TestClient(app) as client:
            response = client.get("/me")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "sub": "auth0|test-user",
        "email": "runner@example.com",
        "permissions": ["read:profile"],
    }


def test_get_me_requires_authorization_token():
    with TestClient(app) as client:
        response = client.get("/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing authorization token"}

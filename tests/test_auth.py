import pytest
from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/customers/",
        json={
            "name": "New User",
            "email": "new@example.com",
            "password": "newpassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New User"
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_create_customer_duplicate_email(client, test_customer):
    response = client.post(
        "/customers/",
        json={
            "name": "Another User",
            "email": "test@example.com",  # Same email as test_customer
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_success(client, test_customer):
    response = client.post(
        "/token", data={"username": "test@example.com", "password": "testpassword123"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client, test_customer):
    response = client.post(
        "/token", data={"username": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_wrong_email(client, test_customer):
    response = client.post(
        "/token", data={"username": "wrong@example.com", "password": "testpassword123"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_current_user(client, token):
    response = client.get("/customers/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"


def test_update_customer(client, token):
    response = client.put(
        "/customers/me",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Updated Name"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "test@example.com"


def test_delete_customer(client, token):
    response = client.delete(
        "/customers/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Try to get the deleted user
    response = client.get("/customers/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

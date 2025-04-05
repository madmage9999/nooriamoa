import pytest
from httpx import AsyncClient
from fastapi import status
from .conftest import hash_password
from app.models import User
from sqlalchemy import delete
from sqlalchemy.sql import text
from uuid import uuid4

@pytest.mark.asyncio
async def test_user_login_success(client: AsyncClient, session):
    db = session
    # Clean slate
    await db.execute(delete(User))
    await db.commit()

    # Create test user
    test_user = User(
        email=f"test_{uuid4()}@example.com",
        password=hash_password("secret123")
    )
    print("adding test user")
    db.add(test_user)
    await db.commit()

    # Print all database entries for debugging
    users = await db.execute(text('SELECT * FROM users'))
    print(users.fetchall())

    response = await client.post("/login", json={
        "email": test_user.email,
        "password": "secret123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_login_fail(client):
    response = await client.post("/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

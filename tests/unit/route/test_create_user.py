import pytest


@pytest.mark.asyncio
async def test_create_user(async_client):

    payload = {"name": "Diego", "email": "diego@test.com"}

    response = await async_client.post("/users/", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "diego@test.com"

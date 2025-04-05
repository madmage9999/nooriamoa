import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_read_main(client):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Hello": "World"}

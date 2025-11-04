import pytest

from src.main import app
from httpx import AsyncClient, ASGITransport
import json


@pytest.mark.asyncio
async def test_create_game():

    game = json.dumps({
        "title": "string",
        "description": "string",
        "rating": 0,
        "image_path": "string"
        })

    print(game)

    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        response = await client.post('/games', json=game)
        assert response.status_code == 201
        data = response.json()

        assert data == {'message': 'Success'}
        
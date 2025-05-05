import json

import pytest


@pytest.mark.anyio
async def test_create_summary(test_app_with_db):
    response = await test_app_with_db.post(
        "/summaries/", json={"url": "http://testdriven.io"}
    )
    assert response.status_code == 201
    assert response.json()["url"] == "http://testdriven.io"

import json

import pytest


@pytest.mark.anyio
async def test_create_summary(test_app_with_db):
    response = await test_app_with_db.post(
        "/summaries/", json={"url": "http://testdriven.io"}
    )
    assert response.status_code == 201
    assert response.json()["url"] == "http://testdriven.io"


@pytest.mark.anyio
async def test_create_summaries_invalid_json(test_app_with_db):
    response = await test_app_with_db.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": {},
                "loc": ["body", "url"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }

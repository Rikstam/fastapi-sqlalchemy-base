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
@pytest.mark.anyio

async def test_read_summary(test_app_with_db):
    response = await test_app_with_db.post("/summaries/", data=json.dumps({"url": "https://foo.bar"}))
    summary_id = response.json()["id"]

    response = await test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


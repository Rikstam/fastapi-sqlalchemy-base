import json
from datetime import datetime

import pytest
from app.api import crud, summaries


@pytest.fixture(autouse=True)
def mock_generate_summary_fixture(monkeypatch):
    def mock_generate_summary(summary_id, url):
        return None
    monkeypatch.setattr(summaries, "generate_summary", mock_generate_summary)


@pytest.mark.anyio
async def test_create_summary(test_app_with_db, monkeypatch):
    test_request_payload = {"url": "https://foo.bar"}
    test_response_payload = {"id": 1, "url": "https://foo.bar/"}

    async def mock_post(payload, db):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = await test_app_with_db.post(
        "/summaries/",
        data=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.anyio
async def test_create_summaries_invalid_json(test_app_with_db):
    response = await test_app_with_db.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "url"],
                "msg": "Field required",
                "input": {},
            }
        ]
    }

    response = await test_app_with_db.post(
        "/summaries/", data=json.dumps({"url": "invalid://url"})
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"] == "URL scheme should be 'http' or 'https'"
    )


@pytest.mark.anyio
async def test_read_summary(test_app_with_db, monkeypatch):
    test_data = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_get(id, db):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = await test_app_with_db.get("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.anyio
async def test_read_summary_incorrect_id(test_app_with_db, monkeypatch):
    async def mock_get(id, db):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = await test_app_with_db.get("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


async def test_read_all_summaries(test_app_with_db, monkeypatch):
    test_data = [
        {
            "id": 1,
            "url": "https://foo.bar",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
        {
            "id": 2,
            "url": "https://testdrivenn.io",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = await test_app_with_db.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.anyio
async def test_remove_summary(test_app_with_db, monkeypatch):
    async def mock_get(id, db):
        return {
            "id": 1,
            "url": "https://foo.bar",
            "summary": "summary",
            "created_at": datetime.utcnow().isoformat(),
        }

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id, db):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = await test_app_with_db.delete("/summaries/1/")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "url": "https://foo.bar/"}


@pytest.mark.anyio
async def test_remove_summary_incorrect_id(test_app_with_db, monkeypatch):
    async def mock_get(id, db):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = await test_app_with_db.delete("/summaries/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


@pytest.mark.anyio
async def test_update_summary(test_app_with_db, monkeypatch):
    test_request_payload = {"url": "https://foo.bar", "summary": "updated"}
    test_response_payload = {
        "id": 1,
        "url": "https://foo.bar",
        "summary": "summary",
        "created_at": datetime.utcnow().isoformat(),
    }

    async def mock_put(id, payload, db):
        return test_response_payload

    monkeypatch.setattr(crud, "put", mock_put)

    response = await test_app_with_db.put(
        "/summaries/1/", data=json.dumps(test_request_payload)
    )
    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "summary_id, payload, status_code, detail",
    [
        [
            999,
            {"url": "https://foo.bar", "summary": "updated!"},
            404,
            "Summary not found",
        ],
        [
            0,
            {"url": "https://foo.bar", "summary": "updated!"},
            422,
            [
                {
                    "type": "greater_than",
                    "loc": ["path", "id"],
                    "msg": "Input should be greater than 0",
                    "input": "0",
                    "ctx": {"gt": 0},
                }
            ],
        ],
        [
            1,
            {},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "url"],
                    "msg": "Field required",
                    "input": {},
                },
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {},
                },
            ],
        ],
        [
            1,
            {"url": "https://foo.bar"},
            422,
            [
                {
                    "type": "missing",
                    "loc": ["body", "summary"],
                    "msg": "Field required",
                    "input": {"url": "https://foo.bar"},
                }
            ],
        ],
    ],
)
@pytest.mark.anyio
async def test_update_summary_invalid(
    test_app_with_db, monkeypatch, summary_id, payload, status_code, detail
):
    async def mock_put(id, payload, db):
        return None

    monkeypatch.setattr(crud, "put", mock_put)

    response = await test_app_with_db.put(
        f"/summaries/{summary_id}/", data=json.dumps(payload)
    )
    assert response.status_code == status_code
    assert response.json()["detail"] == detail

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BASE_URL = "http://test"
transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_predict_stub_ok_single():
    payload = {"texts": ["hello world"], "top_k": 1}
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        r = await ac.post("/v1/predict", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "results" in body and "processing_ms" in body
    assert isinstance(body["processing_ms"], int)
    assert len(body["results"]) == 1
    assert len(body["results"][0]) >= 1
    assert set(body["results"][0][0].keys()) == {"label", "score"}

@pytest.mark.asyncio
async def test_predict_stub_ok_batch():
    payload = {"texts": ["good", "bad", "neutral"], "top_k": 1}
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        r = await ac.post("/v1/predict", json=payload, headers={"X-Request-ID": "test-123"})
    assert r.status_code == 200
    body = r.json()
    assert len(body["results"]) == 3
    assert r.headers["X-Request-ID"] #Test middleware

@pytest.mark.asyncio
async def test_predict_validation_errors():
    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        r1 = await ac.post("/v1/predict", json={"texts": [], "top_k": 1})
        r2 = await ac.post("/v1/predict", json={"texts": ["x"], "top_k": 0})
    assert r1.status_code == 422
    assert r2.status_code == 422
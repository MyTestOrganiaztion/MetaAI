import pytest
from httpx import AsyncClient
import json


testEndPoint = "http://127.0.0.1:8000"
testEvent = json.load(open("./test/events/prompt.json", "r", encoding="utf-8"))

@pytest.mark.asyncio
async def test_post_prompt_text_only():
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["textOnly"]
        response = await client.post("/chat", json=payload, timeout=120)
    responseData = response.json()
    assert response.status_code == 200
    assert responseData.get("code") == "OK000"
    assert responseData.get("detail") == ""

@pytest.mark.asyncio
async def test_post_prompt_web_only():
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["webOnly"]
        response = await client.post("/chat", json=payload, timeout=120)
    responseData = response.json()
    assert response.status_code == 200
    assert responseData.get("code") == "OK000"
    assert responseData.get("detail") == ""

@pytest.mark.asyncio
async def test_post_prompt_text_web():
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["textAndWeb"]
        response = await client.post("/chat", json=payload, timeout=120)
    responseData = response.json()
    assert response.status_code == 200
    assert responseData.get("code") == "OK000"
    assert responseData.get("detail") == ""

@pytest.mark.asyncio
async def test_reach_rate_limit():
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["reachRateLimit"]
        response = await client.post("/chat", json=payload, timeout=120)
    responseData = response.json()
    assert response.status_code == 429
    assert responseData.get("code") == "ER000"

@pytest.mark.asyncio
async def test_missong_require_para():
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["missingRequirePara"]
        response = await client.post("/chat", json=payload, timeout=120)
    responseData = response.json()
    assert response.status_code == 400
    assert responseData.get("code") == "ER005"

@pytest.mark.asyncio
async def test_unknown_route():
    async with AsyncClient(base_url=testEndPoint) as client:
        response = await client.get("/unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

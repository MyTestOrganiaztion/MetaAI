import pytest
from httpx import AsyncClient, Client
import json
import logging


logger = logging.getLogger(__name__)

testEndPoint = "http://localhost:8000"
testEvent = json.load(open("./test/events/prompt.json", "r", encoding="utf-8"))

@pytest.mark.asyncio
async def test_post_prompt_text_only():
    with Client(base_url=testEndPoint) as client:
        response = client.get("/session/create", timeout=120)
        responseData:dict = response.json()
    sessionID = responseData.get("result").get("sessionID")
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["textOnly"]
        response = await client.post(f"/chat/{sessionID}", json=payload, timeout=120)
    responseData = response.json()
    logger.info(f"Test {test_post_prompt_text_only.__name__}")
    logger.info(responseData)
    assert response.status_code == 200
    assert responseData.get("code") == "OK000"
    assert responseData.get("detail") == ""

@pytest.mark.asyncio
async def test_post_prompt_web_only():
    with Client(base_url=testEndPoint) as client:
        response = client.get("/session/create", timeout=120)
        responseData:dict = response.json()
    sessionID = responseData.get("result").get("sessionID")
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["webOnly"]
        response = await client.post(f"/chat/{sessionID}", json=payload, timeout=120)
    responseData = response.json()
    logger.info(f"Test {test_post_prompt_web_only.__name__}")
    logger.info(responseData)
    assert response.status_code == 200
    assert responseData.get("code") == "OK000"
    assert responseData.get("detail") == ""

@pytest.mark.asyncio
async def test_post_prompt_text_web():
    with Client(base_url=testEndPoint) as client:
        response = client.get("/session/create", timeout=120)
        responseData:dict = response.json()
    sessionID = responseData.get("result").get("sessionID")
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["textAndWeb"]
        response = await client.post(f"/chat/{sessionID}", json=payload, timeout=120)
    responseData = response.json()
    logger.info(f"Test {test_post_prompt_text_web.__name__}")
    logger.info(responseData)
    assert response.status_code == 200
    assert responseData.get("code") == "OK000"
    assert responseData.get("detail") == ""

@pytest.mark.asyncio
async def test_reach_rate_limit():
    with Client(base_url=testEndPoint) as client:
        response = client.get("/session/create", timeout=120)
        responseData:dict = response.json()
    sessionID = responseData.get("result").get("sessionID")
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["reachRateLimit"]
        response = await client.post(f"/chat/{sessionID}", json=payload, timeout=120)
    responseData = response.json()
    logger.info(f"Test {test_reach_rate_limit.__name__}")
    logger.info(responseData)
    assert response.status_code == 429
    assert responseData.get("code") == "ER000"

@pytest.mark.asyncio
async def test_missing_require_para():
    with Client(base_url=testEndPoint) as client:
        response = client.get("/session/create", timeout=120)
        responseData:dict = response.json()
    sessionID = responseData.get("result").get("sessionID")
    async with AsyncClient(base_url=testEndPoint) as client:
        payload = testEvent["missingRequirePara"]
        response = await client.post(f"/chat/{sessionID}", json=payload, timeout=120)
    responseData = response.json()
    logger.info(f"Test {test_missing_require_para.__name__}")
    logger.info(responseData)
    assert response.status_code == 400
    assert responseData.get("code") == "ER005"

@pytest.mark.asyncio
async def test_unknown_route():
    async with AsyncClient(base_url=testEndPoint) as client:
        response = await client.get("/unknown")
    responseData = response.json()
    logger.info(f"Test {test_unknown_route.__name__}")
    logger.info(responseData)
    assert response.status_code == 404
    assert responseData == {"detail": "Not Found"}

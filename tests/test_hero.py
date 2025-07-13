import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_add_hero_success(client: AsyncClient):
    response = await client.post("/hero/", json={"name": "TestHero"})
    assert response.status_code == 201, "Expected status 201 Created"
    data = response.json()
    assert data["name"] == "TestHero", "Hero name should match the request"
    assert isinstance(data.get("id"), int), "Response should include an integer id"

@pytest.mark.anyio
async def test_add_hero_duplicate(client: AsyncClient):
    await client.post("/hero/", json={"name": "TestHero"})
    response = await client.post("/hero/", json={"name": "TestHero"})
    assert response.status_code == 400, "Expected status 400 for duplicate hero"
    assert "already exists" in response.json()["detail"], "Error detail should mention duplicate"

@pytest.mark.anyio
async def test_list_heroes_no_filter(client: AsyncClient):
    response = await client.get("/heroes/")
    assert response.status_code == 200, "Expected status 200 OK"
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) >= 1, "At least one hero should exist"

@pytest.mark.anyio
@pytest.mark.parametrize(
    "param,value,expected_in",
    [
        ("strength_ge", 50, "TestHero"),
        ("intelligence_le", 100, "TestHero"),
    ],
    ids=[
        "should filter heroes with strength >= value",
        "should filter heroes with intelligence <= value",
    ],
)
async def test_list_filter_match(client: AsyncClient, param, value, expected_in):
    url = f"/heroes/?{param}={value}"
    response = await client.get(url)
    assert response.status_code == 200, f"Expected 200 for filter {param}"
    names = [h["name"] for h in response.json()]
    assert expected_in in names, f"Expected {expected_in} in filtered results"

@pytest.mark.anyio
async def test_list_filter_no_match(client: AsyncClient):
    response = await client.get("/heroes/?strength_ge=1000")
    assert response.status_code == 404, "Expected 404 when no heroes match the filter"
    assert "No heroes found" in response.json()["detail"], "Error detail should indicate no matches"

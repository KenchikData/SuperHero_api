import os
import httpx

SUPERHERO_TOKEN = os.getenv("SUPERHERO_API_TOKEN", "")
BASE_URL = f"https://superheroapi.com/api/{SUPERHERO_TOKEN}"

class SuperHeroAPIError(Exception):
    pass

async def fetch_hero_stats(name: str) -> dict:
    url = f"{BASE_URL}/search/{name}"
    
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        resp = await client.get(url)

    if resp.status_code != 200:
        raise SuperHeroAPIError(f"SuperHero API error: status {resp.status_code}")

    try:
        data = resp.json()
    except ValueError:
        raise SuperHeroAPIError("SuperHero API returned invalid JSON response")

    if data.get("response") == "error" or "results" not in data:
        raise SuperHeroAPIError(f"No such hero: {name}")

    for item in data.get("results", []):
        if item.get("name", "").lower() == name.lower():
            stats = item.get("powerstats", {})
            return {
                "name": item.get("name"),
                "intelligence": int(stats.get("intelligence") or 0),
                "strength": int(stats.get("strength") or 0),
                "speed": int(stats.get("speed") or 0),
                "power": int(stats.get("power") or 0),
            }

    raise SuperHeroAPIError(f"No exact match for hero: {name}")

from aiohttp import ClientSession

from checker.constants import HTTPS_HEADERS


async def check_hypixel(uuid: str) -> str:
    try:
        async with ClientSession() as session:
            response = await session.get(f"https://api.slothpixel.me/api/players/{uuid}", headers=HTTPS_HEADERS)
            json = await response.json()

            return f"""Hypixel:
                    Rank: {str(json["rank"]).replace("_PLUS", "+")}
                    Level: {json["level"]}
                    No Login: {"true" if json["username"] is None else "false"}
                    Bedwars Level: {json["stats"]["BedWars"]["level"]}
                    Bedwars Coins: {json["stats"]["BedWars"]["coins"]}
                    Skywars Level: {round(json["stats"]["SkyWars"]["level"])}
                    Skywars Coins: {json["stats"]["SkyWars"]["coins"]}"""
    except Exception:
        return "Hypixel: None"

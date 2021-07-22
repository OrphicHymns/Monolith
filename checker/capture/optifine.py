from aiohttp import ClientSession

from checker.constants import HTTP_HEADERS


async def check_optifine(username: str) -> str:
    try:
        async with ClientSession() as session:
            response = await session.get(f"http://s.optifine.net/capes/{username}.png", headers=HTTP_HEADERS)

            if response.status == 200:
                return "Optifine: True"
            else:
                return "Optifine: False"
    except Exception:
        return "Optifine: False"

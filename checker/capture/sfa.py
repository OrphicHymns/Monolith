from aiohttp import ClientSession

from checker.constants import HTTPS_HEADERS


async def check_sfa(access_token: str) -> str:
    headers = HTTPS_HEADERS
    headers["Authorization"] = f"Authorization: Bearer {access_token}"
    try:
        async with ClientSession() as session:
            response = await session.get("https://api.mojang.com/user/security/challenges", headers=headers)
            text = await response.text()
            if text.__contains__("[]"):
                return "Account Type: SFA"
            else:
                return "Account Type: NFA"
    except Exception:
        return "Account Type: NFA"

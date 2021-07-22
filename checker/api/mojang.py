from typing import Optional

from aiohttp_proxy import ProxyConnector
from aiohttp import ClientSession, ClientTimeout

from checker.functions import create_mojang_payload
from checker.api.types import Account, MojangLoginResponse
from checker.constants import MOJANG_AUTH, JSON_POST_HEADERS


async def mojang_login(
        email: str, password: str, proxy: Optional[ProxyConnector] = None, timeout: Optional[ClientTimeout] = None
) -> MojangLoginResponse:
    async with ClientSession(connector=proxy, timeout=timeout) as session:
        response = await session.post(
            MOJANG_AUTH, json=create_mojang_payload(email, password), headers=JSON_POST_HEADERS
        )
        text = await response.text()

        if text.__contains__("accessToken"):
            json = await response.json()
            return MojangLoginResponse(
                success=True,
                account_type=Account.PREMIUM,
                access_token=json["accessToken"],
                uuid=json["availableProfiles"][0]["id"],
                username=json["availableProfiles"][0]["name"]
            )
        elif text.__contains__("[]"):
            return MojangLoginResponse(
                success=True,
                account_type=Account.FREE
            )
        elif text.__contains__("Invalid credentials"):
            return MojangLoginResponse(
                account_type=Account.INVALID
            )
        else:
            return MojangLoginResponse(
                status_code=response.status
            )

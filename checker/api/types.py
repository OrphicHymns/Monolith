from typing import NamedTuple, Optional, NewType


AccessToken = NewType("AccessToken", str)


class Account(object):
    PREMIUM = "premium"
    FREE = "free"
    INVALID = "invalid"


class MojangLoginResponse(NamedTuple):
    success: Optional[bool] = False
    account_type: Optional[str] = None
    access_token: Optional[str] = None
    uuid: Optional[str] = None
    username: Optional[str] = None
    status_code: Optional[int] = None

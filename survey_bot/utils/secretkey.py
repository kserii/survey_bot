import asyncio
import secrets

_secret = None

SECRET_REFRESH_TIME = 5 * 60


async def secret_update_task():
    global _secret
    while True:
        _secret = secrets.token_hex(16)
        await asyncio.sleep(SECRET_REFRESH_TIME)


def get_current_secret() -> str:
    return _secret

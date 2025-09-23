import logging
from typing import Any

from aiohttp import ClientSession

requests_logger = logging.getLogger('requests')

USERS_DATA_URL = 'https://jsonplaceholder.typicode.com/users'
POSTS_DATA_URL = 'https://jsonplaceholder.typicode.com/posts'


async def fetch_json(session: ClientSession, url: str) -> Any:
    async with session.get(url) as response:
        return await response.json()


async def fetch_users_data(session: ClientSession) -> list[dict]:
    return await fetch_json(session, USERS_DATA_URL)


async def fetch_posts_data(session: ClientSession) -> list[dict]:
    return await fetch_json(session, POSTS_DATA_URL)

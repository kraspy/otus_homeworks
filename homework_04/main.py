"""
Домашнее задание №4
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio
import logging

import aiohttp
from jsonplaceholder_requests import (
    fetch_posts_data,
    fetch_users_data,
)
from models import (
    Base,
    Post,
    Session,
    User,
    async_engine,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_users(session: AsyncSession, users_data: list[dict]):
    users = [
        User(
            id=user_data['id'],
            name=user_data['name'],
            username=user_data['username'],
            email=user_data['email'],
        )
        for user_data in users_data
    ]
    session.add_all(users)
    await session.commit()


async def add_posts(session: AsyncSession, posts_data: list[dict]):
    posts = [
        Post(
            id=post_data['id'],
            title=post_data['title'],
            body=post_data['body'],
            user_id=post_data['userId'],
        )
        for post_data in posts_data
    ]
    session.add_all(posts)
    await session.commit()


async def async_main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
    )

    await create_tables(async_engine)

    async with aiohttp.ClientSession() as http_session:
        users_data, posts_data = await asyncio.gather(
            fetch_users_data(http_session),
            fetch_posts_data(http_session),
        )

    async with Session() as session:
        await add_users(session, users_data)
        await add_posts(session, posts_data)

    await async_engine.dispose()


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()

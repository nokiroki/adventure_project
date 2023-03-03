import logging
import asyncio

from database import DBWorker

logging.basicConfig(level=logging.INFO)


def create_insert_task():
    task = asyncio.wait(DBWorker.add_new_user)


if __name__ == '__main__':
    asyncio.run(DBWorker.check_user_if_exists_and_create(12))

import logging
import asyncio

from database import DBWorker

logging.basicConfig(level=logging.INFO)


def create_insert_task():
    task = asyncio.wait(DBWorker.add_new_user)


if __name__ == '__main__':
    a = asyncio.run(DBWorker.get_tables_by_user(3))
    print(a)

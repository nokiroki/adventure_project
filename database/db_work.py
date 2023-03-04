from contextlib import closing
import sqlite3
import os
import logging
from typing import Optional, Iterable, Tuple

import aiosqlite as sql
from aiosqlite import Connection


class DBWorker:

    NAME = os.path.join('data', 'databse.db')

    async def check_table_exists_and_create(user_id: int, table_name: str) -> Optional[int]:
        async with sql.connect(DBWorker.NAME) as db:
            cur = await db.cursor()
            await cur.execute("""SELECT telegram_id, table_name FROM user_table
                INNER JOIN tables ON user_table.table_id = tables.table_id
                WHERE telegram_id = (?) and table_name LIKE (?)
            """, (user_id, table_name))
            result = await cur.fetchone()   
            if not result:
                logging.info('Table is not exist. Creating new table...')
                result = await DBWorker._create_new_table(user_id, table_name, db)
                await cur.close()
                return result
            logging.warning('User tried to create table with existing name')
            await cur.close()
            return None

    async def get_tables_by_user(user_id: int) -> Optional[Iterable[Tuple[int, str]]]:
        async with sql.connect(DBWorker.NAME) as db:
            cur = await db.cursor()
            await cur.execute("""SELECT table_id FROM user_table
                WHERE telegram_id = (?)
            """, (user_id,))
            result = await cur.fetchall()
            if not result:
                await cur.close()
                return None
            ids = tuple(map(lambda x: x[0], result))
            await cur.execute(f"""SELECT table_name FROM tables
            WHERE table_id IN ({','.join(['?' for _ in ids])})
            """, ids)
            names = await cur.fetchall()
            await cur.close()
            return list(map(lambda x: (x[0], x[1][0]), zip(ids, names)))

    async def _create_new_table(user_id: int, table_name: str, db: Connection) -> int:
        await db.execute('INSERT INTO tables(table_name) VALUES (?)', (table_name,))
        cur = await db.cursor()
        await cur.execute("""SELECT table_id FROM tables
            WHERE table_name = (?)
        """, (table_name,))
        result = await cur.fetchall()
        await cur.close()

        await db.execute('INSERT INTO user_table VALUES (?, ?)', (user_id, result[-1][0]))
        await db.commit()
        return result[-1][0]



if __name__ == '__main__':
    if not os.path.exists('data'):
        os.mkdir('data')
    with sqlite3.connect(DBWorker.NAME) as conn:
        with closing(conn.cursor()) as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS user_table(
                telegram_id INTEGER,
                table_id INTEGER,
                PRIMARY KEY(telegram_id, table_id))
            """)
            cur.execute("""CREATE TABLE IF NOT EXISTS tables(
                table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT)
            """)
            conn.commit()

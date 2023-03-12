import aiofiles
from typing import Optional

from .db_work import DBWorker
from logic import Matrix


class DebtDataBase:

    GENERAL_FOLDER  = 'data'
    DB_NAME         = 'database.db'
    USER_TABLE      = 'user_table'
    TABLES          = 'tables'
    TABLES_DIR      = 'tables'

    @staticmethod
    async def create_new_table(user_id: int, table_name: str) -> Optional[int]:
        table_id = DBWorker.check_table_exists_and_create(user_id, table_name)
        if not table_id:
            return None
        

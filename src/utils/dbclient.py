import sqlite3
from pathlib import Path

class DBClient:
    def __init__(self, file_path: str) -> None:
        self.db_file = Path("src/data") / file_path
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()
        self._insert_defaults()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        conn.text_factory = str
        return conn

    def execute(self, sql: str, params: tuple = (), fetch=False, commit=False, script=False, return_lastrowid=False) -> list[tuple] | int | None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            result = None
            if script:
                cursor.executescript(sql)
            else:
                cursor.execute(sql, params)
                if fetch:
                    result = cursor.fetchall()
                elif return_lastrowid:
                    result = cursor.lastrowid
            if commit:
                conn.commit()
            return result

    def _create_tables(self) -> None:
        create_tables_sql = self._extract_sql(file_name="create_tables.sql")
        self.execute(sql=create_tables_sql, commit=True, script=True)

    def _insert_defaults(self) -> None:
        insert_defaults_sql = self._extract_sql(file_name="insert_defaults.sql")
        self.execute(sql=insert_defaults_sql, commit=True, script=True)
    
    def _extract_sql(self, file_name: str) -> str:
        try:
            path = Path("src/sql") / file_name
            with open(path) as file:
                sql = file.read()
            return sql
        except Exception as e:
            print(f"Failed to load sql file {file_name}. Exception: {str(e)}")
            raise

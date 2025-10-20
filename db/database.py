# database.py
import psycopg2
from psycopg2.extensions import connection
from core.config import settings



class DatabaseConnection:
    """Класс для управления подключением к БД (Singleton)."""
    _instance = None
    _connection: connection = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, dbname, user, password, host, port):
        # Чтобы __init__ не пересоздавал соединение много раз
        if self._connection is None:
            self._connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )

    def get_connection(self) -> connection:
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None



db_conn = DatabaseConnection(settings.DATABASE, settings.USER, settings.PASSWORD, settings.HOST,settings.PORT)
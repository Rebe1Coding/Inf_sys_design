from psycopg2 import sql
from typing import List, Optional
from models.client import Client


class Client_rep_DB:
    """Реализация репозитория для работы с PostgreSQL."""

    def __init__(self, db_connection):

        self._db = db_connection

    def get_by_id(self, client_id: int) -> Optional[Client]:
        query = "SELECT * FROM clients WHERE client_id = %s;"
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (client_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Client(*row)
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[dict]:
        """Получить список k по счету n объектов класса short."""
        # Используем LIMIT и OFFSET для пагинации
        query = "SELECT client_id, name, contact_person FROM clients ORDER BY client_id LIMIT %s OFFSET %s;"
        offset = (n - 1) * k
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (k, offset))
        rows = cursor.fetchall()
        cursor.close()
        # Создаём краткие описания на лету
        short_list = []
        for row in rows:
            # row: (id, name, contact_person)
            short_list.append({
                "client_id": row[0],
                "name": row[1],
                "contact_person": row[2]
            })
        return short_list

    def add_client(self, client_data: dict) -> Client:
        """Добавить объект в список. ID генерируется в БД (SERIAL)."""
        # Исключаем client_id, так как он auto-increment
        query = """
            INSERT INTO clients (name, ownership_type, address, phone, contact_person)
            VALUES (%(name)s, %(ownership_type)s, %(address)s, %(phone)s, %(contact_person)s)
            RETURNING client_id;
        """
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, client_data)
        new_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        # Создаём и возвращаем объект
        return Client(client_id=new_id, **client_data)

    def update_client(self, client_id: int, new_data: dict) -> bool:
        """Заменить элемент списка по ID."""
        # Динамически формируем запрос на основе переданных полей
        set_clause = ", ".join([f"{key} = %s" for key in new_data.keys()])
        values = list(new_data.values())
        values.append(client_id)  # Добавляем client_id для условия WHERE

        query = sql.SQL("UPDATE clients SET {} WHERE client_id = %s;").format(
            sql.SQL(set_clause)
        )
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, values)
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return rows_affected > 0

    def delete_client(self, client_id: int) -> bool:
        query = "DELETE FROM clients WHERE client_id = %s;"
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (client_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return rows_affected > 0

    def get_count(self) -> int:
        query = "SELECT COUNT(*) FROM clients;"
        conn = self._db.get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        return count

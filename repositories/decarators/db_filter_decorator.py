# repositories/db_filter_decorator.py

class FilteredClientDBRepository:
    """Декоратор: добавляет фильтрацию и сортировку к Client_rep_DB."""

    def __init__(self, db_repo, filter_sql: str = "", order_by: str = "client_id"):
        """
        :param db_repo: экземпляр Client_rep_DB
        :param filter_sql: строка для условия WHERE (без слова WHERE), например: "name LIKE '%ООО%'"
        :param order_by: поле и направление сортировки, например: "name ASC"
        """
        self._db_repo = db_repo
        self._filter = filter_sql
        self._order_by = order_by if order_by else "client_id"

    def get_k_n_short_list(self, k: int, n: int) -> list[str]:
        """Возвращает k элементов, начиная с n-й страницы, с учётом фильтра и сортировки."""
        offset = (n - 1) * k
        
        query = "SELECT name, contact_person FROM clients"
        if self._filter:
            query += f" WHERE {self._filter}"
        query += f" ORDER BY {self._order_by} LIMIT {k} OFFSET {offset}"

        with self._db_repo._db.cursor() as cur:
            cur.execute(query)
            return [f"{name} ({contact})" for name, contact in cur.fetchall()]

    def get_count(self) -> int:
        """Возвращает общее количество записей с учётом фильтра."""
        query = "SELECT COUNT(*) FROM clients"
        if self._filter:
            query += f" WHERE {self._filter}"

        with self._db_repo._db.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()[0]

    # Остальные методы просто делегируем (можно не писать, если не используются в задании)
    def get_by_id(self, client_id: int):
        return self._db_repo.get_by_id(client_id)

    def add_client(self, client_data: dict):
        return self._db_repo.add_client(client_data)

    def update_client(self, client_id: int, new_data: dict):
        return self._db_repo.update_client(client_id, new_data)

    def delete_client(self, client_id: int):
        return self._db_repo.delete_client(client_id)
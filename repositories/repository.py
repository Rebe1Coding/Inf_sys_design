from abc import ABC, abstractmethod
from typing import List, Optional
from models.client import Client


class ClientRepository(ABC):
    """Абстрактный базовый класс для всех репозиториев клиентов."""

    def __init__(self):
        self._clients = []
        self._next_id = 1

    def _get_next_id(self):
        next_id = self._next_id
        self._next_id += 1
        return next_id

    @abstractmethod
    def read_all(self) -> None:
        """Абстрактный метод для загрузки всех данных из источника."""
        pass

    @abstractmethod
    def write_all(self) -> None:
        """Абстрактный метод для сохранения всех данных в источник."""
        pass

    # Реализуем общие для всех репозиториев методы
    def get_by_id(self, client_id: int) -> Optional[Client]:
        for client in self._clients:
            if client.client_id == client_id:
                return client
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[str]:
        """Получить список k по счету n объектов класса short."""
        # k - сколько элементов, n - с какого номера (начиная с 1)
        start_index = (n - 1) * k
        end_index = start_index + k
        # Возвращаем список кратких описаний
        return [client.full_info() for client in self._clients[start_index:end_index]]

    def sort_by_field(self, field: str) -> None:

        def normalize_name(name: str) -> str:

            prefixes = ["ООО", "АО", "ЗАО", "ОАО", "ПАО", "ИП", "НКО", "МУП"]

            for prefix in prefixes:
                if name.startswith(prefix):
                    # Удаляем префикс и следующий пробел если есть
                    normalized = name[len(prefix) :].lstrip()
                    return normalized if normalized else name

            return name

        if hasattr(Client, field):
            if field == "name":
                # Для поля name используем нормализованную версию
                self._clients.sort(
                    key=lambda client: normalize_name(getattr(client, field))
                )
            else:
                self._clients.sort(key=lambda client: getattr(client, field))
        else:
            raise ValueError(f"Поле {field} не существует в классе Client")

    def add_client(self, client_data: dict) -> Client:
        """Добавить объект в список (при добавлении сформировать новый ID)."""
        new_id = self._get_next_id()
        # client_data - это словарь с данными, кроме ID
        new_client = Client(client_id=new_id, **client_data)
        self._clients.append(new_client)
        return new_client

    def update_client(self, client_id: int, new_data: dict) -> bool:
        """Заменить элемент списка по ID."""
        client = self.get_by_id(client_id)
        if client:
            for key, value in new_data.items():
                if hasattr(client, key):
                    setattr(client, key, value)
            return True
        return False

    def delete_client(self, client_id: int) -> bool:
        """Удалить элемент списка по ID."""
        client = self.get_by_id(client_id)
        if client:
            self._clients.remove(client)
            return True
        return False

    def get_count(self) -> int:
        """Получить количество элементов."""
        return len(self._clients)


class ClientDBAdapter(ClientRepository):
    """Адаптер для подключения Client_rep_DB к иерархии репозиториев."""

    def __init__(self, db_repository):
        super().__init__()
        self._db_repo = db_repository
        self.read_all()

    def read_all(self):
        conn = self._db_repo._db.get_connection()
        cursor = conn.cursor()
        with cursor as cur:
            cur.execute("SELECT * FROM clients ORDER BY client_id")
            rows = cur.fetchall()
            self._clients = [Client(*row) for row in rows]

    def write_all(self):
        # В данном адаптере запись не требуется, так как операции
        # добавления, обновления и удаления сразу отражаются в БД.
        pass

    def get_by_id(self, client_id: int) -> Optional[Client]:
        return self._db_repo.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[dict]:
        return self._db_repo.get_k_n_short_list(k, n)

    def add_client(self, client_data: dict) -> Client:
        return self._db_repo.add_client(client_data)

    def update_client(self, client_id: int, new_data: dict) -> bool:
        return self._db_repo.update_client(client_id, new_data)

    def delete_client(self, client_id: int) -> bool:
        return self._db_repo.delete_client(client_id)

    def get_count(self) -> int:
        return self._db_repo.get_count()

import json
from abc import ABC, abstractmethod
from typing import List, Optional
from client import Client  
from repositories.client_rep_json import Client_rep_json
from repositories.client_rep_yaml import Client_rep_yaml    
from repositories.client_rep_db import Client_rep_DB 
from db.database import db_conn


class ClientRepository(ABC):
    """Абстрактный базовый класс для всех репозиториев клиентов."""

    def __init__(self):
        self._clients = []  # Список для хранения объектов Client в памяти
        self._next_id = 1   # Счётчик для генерации нового ID

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

            prefixes = ['ООО', 'АО', 'ЗАО', 'ОАО', 'ПАО', 'ИП', 'НКО', 'МУП']
        
            for prefix in prefixes:
                if name.startswith(prefix):
                # Удаляем префикс и следующий пробел если есть
                    normalized = name[len(prefix):].lstrip()
                    return normalized if normalized else name
        
            return name

        if hasattr(Client, field):
            if field == 'name':
            # Для поля name используем нормализованную версию
                self._clients.sort(key=lambda client: normalize_name(getattr(client, field)))
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
        # Вместо наследования используем композицию (делегация!)
        self._db_repo = db_repository


    def read_all(self) -> None:
        #??????
        pass

    def write_all(self) -> None:
        #??????
        pass

    # Далее мы делегируем все вызовы методов адаптируемому объекту (_db_repo)
    def get_by_id(self, client_id: int) -> Optional[Client]:
        return self._db_repo.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[str]:
        return self._db_repo.get_k_n_short_list(k, n)

    def add_client(self, client_data: dict) -> Client:
        return self._db_repo.add_client(client_data)

    def update_client(self, client_id: int, new_data: dict) -> bool:
        return self._db_repo.update_client(client_id, new_data)

    def delete_client(self, client_id: int) -> bool:
        return self._db_repo.delete_client(client_id)

    def get_count(self) -> int:
        return self._db_repo.get_count()




def use_client_repo_json(filename = "./data/clients.json") -> None:
    """
    Демонстрация использования Client_rep_json:
    - загрузка из файла
    - добавление, обновление, удаление
    - краткие списки и сортировка
    """
    repo = Client_rep_json(filename)

    print("\nКлиенты из репозитория (до изменений):")
    for c in repo._clients:
        print(c.full_info())

    # Добавим нового клиента через add_client (репозиторий сам сгенерирует ID)
    new_data = {
        "name": "ООО Новое",
        "ownership_type": "ООО",
        "address": "г.Тест, ул. Новая, 1",
        "phone": "+70000000001",
        "contact_person": "Новиков Н.Н."
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())

    # Сохраняем изменения
    repo.write_all()

    # Обновим только что добавленного клиента
    if repo.update_client(new_client.client_id, {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"}):
        print("\nПосле обновления:")
        print(repo.get_by_id(new_client.client_id).full_info())

    # Показ краткого списка (k=2, n=1)
    print("\nКраткий список (k=2, n=1):")
    for s in repo.get_k_n_short_list(2, 1):
        print(s)

    # Сортируем по имени и выводим
    try:
        repo.sort_by_field("name")
        print("\nПосле сортировки по name:")
        for c in repo._clients:
            print(c.full_info())
    except ValueError as e:
        print("\nОшибка при сортировке:", e)

    # Удалим добавленного клиента
    if repo.delete_client(new_client.client_id):
        print(f"\nКлиент с id={new_client.client_id} удалён")
    else:
        print(f"\nНе удалось удалить клиента id={new_client.client_id}")

    # Сохраняем финальное состояние
    repo.write_all()
    print("\nОперации с репозиторием завершены.")



def use_client_repo_yaml(filename = "./data/clients.yaml") -> None:
    """
    Демонстрация использования Client_rep_yaml:
    - загрузка из файла
    - добавление, обновление, удаление
    - краткие списки и сортировка
    """
    repo = Client_rep_yaml(filename)

    print("\nКлиенты из репозитория (до изменений):")
    for c in repo._clients:
        print(c.full_info())

    # Добавим нового клиента через add_client (репозиторий сам сгенерирует ID)
    new_data = {
        "name": "ООО Новое",
        "ownership_type": "ООО",
        "address": "г.Тест, ул. Новая, 1",
        "phone": "+70000000001",
        "contact_person": "Новиков Н.Н."
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())

    # Сохраняем изменения
    repo.write_all()

    # Обновим только что добавленного клиента
    if repo.update_client(new_client.client_id, {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"}):
        print("\nПосле обновления:")
        print(repo.get_by_id(new_client.client_id).full_info())

    # Показ краткого списка (k=2, n=1)
    print("\nКраткий список (k=2, n=1):")
    for s in repo.get_k_n_short_list(2, 1):
        print(s)

    # Сортируем по имени и выводим
    try:
        repo.sort_by_field("name")
        print("\nПосле сортировки по name:")
        for c in repo._clients:
            print(c.full_info())
    except ValueError as e:
        print("\nОшибка при сортировке:", e)

    # Удалим добавленного клиента
    if repo.delete_client(new_client.client_id):
        print(f"\nКлиент с id={new_client.client_id} удалён")
    else:
        print(f"\nНе удалось удалить клиента id={new_client.client_id}")

    # Сохраняем финальное состояние
    repo.write_all()
    print("\nОперации с репозиторием завершены.")

def use_client_repo_db(db_params = db_conn) -> None:
    """
    Демонстрация использования Client_rep_DB через адаптер ClientDBAdapter:
    - загрузка из базы данных
    - добавление, обновление, удаление
    - краткие списки и сортировка
    """
    db_repo = Client_rep_DB(db_params)
    repo = ClientDBAdapter(db_repo)

    print("\nКлиенты из репозитория (до изменений):")
    for c in repo._clients:
        print(c.full_info())

    # Добавим нового клиента через add_client 
    new_data = {
        "name": "ООО Новое",
        "ownership_type": "ООО",
        "address": "г.Тест, ул. Новая, 1",
        "phone": "+70000000001",
        "contact_person": "Новиков Н.Н."
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())


    # Обновим только что добавленного клиента
    if repo.update_client(new_client.client_id, {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"}):
        print("\nПосле обновления:")
        print(repo.get_by_id(new_client.client_id).full_info())

    # Показ краткого списка (k=2, n=1)
    print("\nКраткий список (k=2, n=1):")
    for s in repo.get_k_n_short_list(2, 1):
        print(s)

    # Сортируем по имени и выводим
    try:
        repo.sort_by_field("name")
        print("\nПосле сортировки по name:")
        for c in repo._clients:
            print(c.full_info())
    except ValueError as e:
        print("\nОшибка при сортировке:", e)

    # Удалим добавленного клиента
    if repo.delete_client(new_client.client_id):
        print(f"\nКлиент с id={new_client.client_id} удалён")
    else:
        print(f"\nНе удалось удалить клиента id={new_client.client_id}")

    # Сохраняем финальное состояние
    repo.write_all()
    print("\nОперации с репозиторием завершены.")
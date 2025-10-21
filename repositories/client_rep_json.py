import json
from repositories.repository import ClientRepository
from core.models.client import Client


class Client_rep_json(ClientRepository):
    """Реализация репозитория для JSON файла."""

    def __init__(self, filename: str):
        super().__init__()
        self._filename = filename
        self.read_all()  # Загружаем данные при создании репозитория

    def read_all(self) -> None:
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._clients = []
                for item in data:
                    # Создаём объекты Client из данных JSON
                    client = Client(**item)
                    self._clients.append(client)
                    # Обновляем счётчик ID, чтобы новый ID был больше существующих
                    if client.client_id >= self._next_id:
                        self._next_id = client.client_id + 1
        except FileNotFoundError:
            # Если файла нет, начинаем с пустого списка
            self._clients = []

    def write_all(self) -> None:
        data = []
        for client in self._clients:
            # Преобразуем каждый объект Client в словарь
            client_dict = {
                'client_id': client.client_id,
                'name': client.name,
                'ownership_type': client.ownership_type,
                'address': client.address,
                'phone': client.phone,
                'contact_person': client.contact_person
            }
            data.append(client_dict)
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
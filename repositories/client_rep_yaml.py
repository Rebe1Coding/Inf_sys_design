from repositories.repository import ClientRepository
import yaml
from models.client import Client


class Client_rep_yaml(ClientRepository):
    """Реализация репозитория для YAML файла."""

    def __init__(self, path: str):
        super().__init__()
        self._path = path
        self.read_all()

    def read_all(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = (
                    yaml.safe_load(f) or []
                )  # Если файл пустой, safe_load вернёт None
                self._clients = []
                for item in data:
                    client = Client(**item)
                    self._clients.append(client)
                    if client.client_id >= self._next_id:
                        self._next_id = client.client_id + 1
        except FileNotFoundError:
            self._clients = []

    def write_all(self) -> None:
        data = []
        for client in self._clients:
            client_dict = {
                "client_id": client.client_id,
                "name": client.name,
                "ownership_type": client.ownership_type,
                "address": client.address,
                "phone": client.phone,
                "contact_person": client.contact_person,
            }
            data.append(client_dict)
        with open(self._path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

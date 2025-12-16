from abc import ABC, abstractmethod
from typing import List, Any


class Observer(ABC):

    @abstractmethod
    def update(self, event_type: str, data: Any = None):
        
        pass


class Subject:
    """Субъект, за которым наблюдают"""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: str, data: Any = None):
    
        for observer in self._observers:
            observer.update(event_type, data)


class RepositoryObserver(Subject):
    """Обертка над репозиторием с поддержкой паттерна Наблюдатель"""

    def __init__(self, repository):
        super().__init__()
        self._repository = repository

    def get_by_id(self, client_id: int):
        return self._repository.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int):
        return self._repository.get_k_n_short_list(k, n)

    def add_client(self, client_data: dict):
        client = self._repository.add_client(client_data)
        self.notify("client_added", client)
        return client

    def update_client(self, client_id: int, new_data: dict):
        success = self._repository.update_client(client_id, new_data)
        if success:
            client = self._repository.get_by_id(client_id)
            self.notify("client_updated", client)
        return success

    def delete_client(self, client_id: int):
        success = self._repository.delete_client(client_id)
        if success:
            self.notify("client_deleted", client_id)
        return success

    def get_count(self):
        return self._repository.get_count()
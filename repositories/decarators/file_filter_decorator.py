# repositories/file_filter_decorator.py

class FilteredFileRepository:
    """Декоратор для файловых репозиториев: добавляет фильтрацию и сортировку."""

    def __init__(self, file_repo, filter_func=None, sort_key=None, reverse=False):
        """
        :param file_repo: экземпляр Client_rep_json или Client_rep_yaml
        :param filter_func: функция для фильтрации, например: lambda c: c.ownership_type == 'ООО'
        :param sort_key: функция для сортировки, например: lambda c: c.name
        :param reverse: сортировать в обратном порядке?
        """
        self._repo = file_repo
        self._filter = filter_func or (lambda x: True)  
        self._sort_key = sort_key
        self._reverse = reverse

    def get_k_n_short_list(self, k: int, n: int) -> list[str]:
     
        all_clients = self._repo._clients  
        filtered = [c for c in all_clients if self._filter(c)]
        if self._sort_key:
            filtered.sort(key=self._sort_key, reverse=self._reverse)
        start = (n - 1) * k
        page = filtered[start:start + k]
        
        return [client.full_info() for client in page]

    def get_count(self) -> int:
        all_clients = self._repo._clients
        return len([c for c in all_clients if self._filter(c)])

    def get_by_id(self, client_id: int):
        return self._repo.get_by_id(client_id)

    def add_client(self, client_data: dict):
        return self._repo.add_client(client_data)

    def update_client(self, client_id: int, new_data: dict):
        return self._repo.update_client(client_id, new_data)

    def delete_client(self, client_id: int):
        return self._repo.delete_client(client_id)
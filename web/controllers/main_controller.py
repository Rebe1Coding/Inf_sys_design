from typing import Optional
from repositories.decarators.db_filter_decorator import FilteredClientDBRepository

class MainController:
    """Контроллер главной страницы - отображение списка клиентов"""

    def __init__(self, repository):
        self._repository = repository

    def get_clients_page(self, page: int = 1, page_size: int = 10, 
                        ownership_filter: Optional[str] = None,
                        sort_field: Optional[str] = None):
        """
        Получить страницу клиентов с фильтрацией и сортировкой
        
        Args:
            page: номер страницы (начиная с 1)
            page_size: количество элементов на странице
            ownership_filter: фильтр по типу собственности
            sort_field: поле для сортировки
        
        Returns:
            dict с данными для отображения
        """
        # Применяем фильтр если нужно
        if ownership_filter:
            
            filter_sql = f"ownership_type = '{ownership_filter}'"
            order_by = sort_field if sort_field else "client_id"
            filtered_repo = FilteredClientDBRepository(
                self._repository._db_repo, 
                filter_sql=filter_sql,
                order_by=order_by
            )
            clients_list = filtered_repo.get_k_n_short_list(page_size, page)
            total_count = filtered_repo.get_count()
        else:
            # Без фильтра
            clients_list = self._repository.get_k_n_short_list(page_size, page)
            total_count = self._repository.get_count()
        
        total_pages = (total_count + page_size - 1) // page_size
        
        return {
            "clients": clients_list,
            "current_page": page,
            "total_pages": total_pages,
            "total_count": total_count,
            "page_size": page_size
        }

    def get_client_detail(self, client_id: int):
        """
        Получить полную информацию о клиенте
        
        Args:
            client_id: ID клиента
        
        Returns:
            dict с данными клиента или None
        """
        client = self._repository.get_by_id(client_id)
        if client:
            return {
                "client_id": client.client_id,
                "name": client.name,
                "ownership_type": client.ownership_type,
                "address": client.address,
                "phone": client.phone,
                "contact_person": client.contact_person
            }
        return None
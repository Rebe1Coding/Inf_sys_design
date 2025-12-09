from models.client import Client


class AddController:
    """Контроллер для добавления нового клиента"""

    def __init__(self, repository):
        self._repository = repository

    def validate_and_add(self, client_data: dict):
        """
        Валидировать данные и добавить клиента
        
        Args:
            client_data: словарь с данными клиента
        
        Returns:
            dict: {"success": bool, "message": str, "client": dict/None}
        """
        try:
            # Валидация на уровне контроллера
            errors = self._validate_client_data(client_data)
            if errors:
                return {
                    "success": False,
                    "message": "Ошибки валидации",
                    "errors": errors,
                    "client": None
                }

            # Валидация на уровне модели произойдет в репозитории
            new_client = self._repository.add_client(client_data)
            
            return {
                "success": True,
                "message": "Клиент успешно добавлен",
                "client": {
                    "client_id": new_client.client_id,
                    "name": new_client.name,
                    "ownership_type": new_client.ownership_type,
                    "address": new_client.address,
                    "phone": new_client.phone,
                    "contact_person": new_client.contact_person
                }
            }
        except ValueError as e:
            return {
                "success": False,
                "message": f"Ошибка валидации: {str(e)}",
                "client": None
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Ошибка при добавлении: {str(e)}",
                "client": None
            }

    def _validate_client_data(self, data: dict):
        """Валидация данных на уровне UI"""
        errors = []

        # Проверка обязательных полей
        required_fields = ["name", "ownership_type", "address", "phone", "contact_person"]
        for field in required_fields:
            if not data.get(field) or not data[field].strip():
                errors.append(f"Поле '{field}' обязательно для заполнения")

        # Дополнительная валидация
        if data.get("name") and len(data["name"].strip()) < 2:
            errors.append("Название должно содержать минимум 2 символа")

        if data.get("address") and len(data["address"].strip()) < 5:
            errors.append("Адрес должен содержать минимум 5 символов")

        if data.get("phone"):
            phone = data["phone"].strip()
            if len(phone) < 7:
                errors.append("Телефон должен содержать минимум 7 цифр")

        if data.get("contact_person") and len(data["contact_person"].strip()) < 2:
            errors.append("ФИО контактного лица должно содержать минимум 2 символа")

        return errors
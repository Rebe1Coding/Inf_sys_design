class EditController:
    
    def __init__(self, repository):
        self._repository = repository

    def get_client_for_edit(self, client_id: int):

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

    def validate_and_update(self, client_id: int, client_data: dict):
       
        try:
            # Проверяем существование клиента
            existing_client = self._repository.get_by_id(client_id)
            if not existing_client:
                return {
                    "success": False,
                    "message": "Клиент не найден",
                    "client": None
                }

            errors = self._validate_client_data(client_data)
            if errors:
                return {
                    "success": False,
                    "message": "Ошибки валидации",
                    "errors": errors,
                    "client": None
                }

            success = self._repository.update_client(client_id, client_data)
            
            if success:
                updated_client = self._repository.get_by_id(client_id)
                return {
                    "success": True,
                    "message": "Клиент успешно обновлен",
                    "client": {
                        "client_id": updated_client.client_id,
                        "name": updated_client.name,
                        "ownership_type": updated_client.ownership_type,
                        "address": updated_client.address,
                        "phone": updated_client.phone,
                        "contact_person": updated_client.contact_person
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "Не удалось обновить клиента",
                    "client": None
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
                "message": f"Ошибка при обновлении: {str(e)}",
                "client": None
            }

    def _validate_client_data(self, data: dict):
        """Валидация данных на уровне UI"""
        errors = []

        # Проверка обязательных полей
        required_fields = ["name", "ownership_type", "address", "phone", "contact_person"]
        for field in required_fields:
            if field in data:
                if not data[field] or not data[field].strip():
                    errors.append(f"Поле '{field}' не может быть пустым")

        # Дополнительная валидация
        if "name" in data and len(data["name"].strip()) < 2:
            errors.append("Название должно содержать минимум 2 символа")

        if "address" in data and len(data["address"].strip()) < 5:
            errors.append("Адрес должен содержать минимум 5 символов")

        if "phone" in data:
            phone = data["phone"].strip()
            if len(phone) < 7:
                errors.append("Телефон должен содержать минимум 7 цифр")

        if "contact_person" in data and len(data["contact_person"].strip()) < 2:
            errors.append("ФИО контактного лица должно содержать минимум 2 символа")

        return errors
from typing import Optional


class FormController:

    def __init__(self, repository, mode: str = "add", client_id: Optional[int] = None):
        self._repository = repository
        self._mode = mode
        self._client_id = client_id

    def get_form_data(self):
        if self._mode == "edit" and self._client_id:
            client = self._repository.get_by_id(self._client_id)
            if client:
                return {
                    "mode": "edit",
                    "title": "Редактирование клиента",
                    "data": {
                        "client_id": client.client_id,
                        "name": client.name,
                        "ownership_type": client.ownership_type,
                        "address": client.address,
                        "phone": client.phone,
                        "contact_person": client.contact_person
                    }
                }
            else:
                return {
                    "mode": "error",
                    "title": "Ошибка",
                    "message": "Клиент не найден"
                }
        else:
            return {
                "mode": "add",
                "title": "Добавление клиента",
                "data": {
                    "client_id": None,
                    "name": "",
                    "ownership_type": "",
                    "address": "",
                    "phone": "",
                    "contact_person": ""
                }
            }

    def submit_form(self, client_data: dict):

        errors = self._validate_client_data(client_data)
        if errors:
            return {
                "success": False,
                "message": "Ошибки валидации",
                "errors": errors
            }

        try:
            if self._mode == "edit" and self._client_id:
                success = self._repository.update_client(self._client_id, client_data)
                if success:
                    updated_client = self._repository.get_by_id(self._client_id)
                    return {
                        "success": True,
                        "message": "Клиент успешно обновлен",
                        "client": self._client_to_dict(updated_client)
                    }
                else:
                    return {
                        "success": False,
                        "message": "Не удалось обновить клиента"
                    }
            else:
                
                new_client = self._repository.add_client(client_data)
                return {
                    "success": True,
                    "message": "Клиент успешно добавлен",
                    "client": self._client_to_dict(new_client)
                }
                
        except ValueError as e:
            return {
                "success": False,
                "message": f"Ошибка валидации: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Ошибка при сохранении: {str(e)}"
            }

    def _validate_client_data(self, data: dict):

        errors = []

        required_fields = {
            "name": "Название",
            "ownership_type": "Тип собственности",
            "address": "Адрес",
            "phone": "Телефон",
            "contact_person": "Контактное лицо"
        }

        for field, label in required_fields.items():
            if not data.get(field) or not data[field].strip():
                errors.append(f"{label} обязательно для заполнения")

        if data.get("name") and len(data["name"].strip()) < 2:
            errors.append("Название должно содержать минимум 2 символа")

        if data.get("address") and len(data["address"].strip()) < 5:
            errors.append("Адрес должен содержать минимум 5 символов")

        if data.get("phone"):
            phone = data["phone"].strip()
            if len(phone) < 7:
                errors.append("Телефон должен содержать минимум 7 цифр")

        if data.get("contact_person") and len(data["contact_person"].strip()) < 2:
            errors.append("ФИО должно содержать минимум 2 символа")

        return errors

    def _client_to_dict(self, client):
        return {
            "client_id": client.client_id,
            "name": client.name,
            "ownership_type": client.ownership_type,
            "address": client.address,
            "phone": client.phone,
            "contact_person": client.contact_person
        }
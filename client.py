import re
import json

class Client:
    def __init__(self, client_id: int, name: str, ownership_type: str,
                 address: str, phone: str, contact_person: str):
        
        self.__client_id = self.validate_id(client_id)
        self.__name = self.validate_name(name)
        self.__ownership_type = ownership_type.strip()
        self.__address = self.validate_address(address)
        self.__phone = self.validate_phone(phone)
        self.__contact_person = self.validate_name(contact_person)
        # ========== ГЕТТЕРЫ / СЕТТЕРЫ ==========


    @property
    def client_id(self):
        return self.__client_id
    
    @client_id.setter
    def client_id(self, value):
        self.__client_id = self.validate_id(value)
    
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        self.__name = self.validate_name(value)

    @property
    def ownership_type(self):
        return self.__ownership_type
    
    @ownership_type.setter
    def ownership_type(self, value):
        self.__ownership_type = value.strip()

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = self.validate_phone(value)
    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self, value):
        self.__address = self.validate_address(value)

    @property
    def contact_person(self):
        return self.__contact_person
    
    @contact_person.setter
    def contact_person(self, value):
        self.__contact_person = self.validate_name(value)

    @property
    def credit_sum(self):
        return self.__credit_sum   
     
    @credit_sum.setter
    def credit_sum(self, value):    
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Сумма кредита должна быть неотрицательным числом")
        self.__credit_sum = float(value)
    
    # ========== ВАЛИДАЦИЯ ==========
      

    @staticmethod
    def validate_id(client_id: int) -> int:
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("ID клиента должен быть положительным числом")
        return client_id

    @staticmethod
    def validate_name(name: str) -> str:
        if not re.match(r'^[А-ЯЁ][а-яёА-ЯЁ\s\.\-]+$', name):
            raise ValueError("Название/ФИО должно начинаться с заглавной буквы и содержать только буквы, пробелы, тире или точки")
        return name.strip()

    @staticmethod
    def validate_address(address: str) -> str:
        if len(address.strip()) < 5:
            raise ValueError("Адрес слишком короткий")
        return address.strip()

    @staticmethod
    def validate_phone(phone: str) -> str:
    # Удаляем все символы, кроме цифр и знака +
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
    
    # Проверяем, что номер содержит от 7 до 15 цифр и может начинаться с +
        if not re.match(r'^\+?\d{7,15}$', cleaned_phone):
            raise ValueError("Телефон должен содержать от 7 до 15 цифр и может начинаться с +")
    
        return cleaned_phone
    
    # ========== ПЕРЕГРУЗКИ КОНСТРУКТОРА ==========

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)

    @classmethod
    def from_string(cls, data_str: str):
        # строка вида: "1;ООО Ромашка;ООО;Москва, ул. Пушкина, 10;+79995553322;Иванов Иван Иванович"
        parts = data_str.split(";")
        if len(parts) != 6:
            raise ValueError("Неверный формат строки для создания клиента")
        return cls(int(parts[0]), parts[1], parts[2], parts[3], parts[4], parts[5])
    

        # ========== ПРЕДСТАВЛЕНИЕ ОБЪЕКТА ==========

    def full_info(self):
        return (f"Клиент {self.name}, "
                f"Форма собственности: {self.ownership_type}, "
                f"Адрес: {self.address}, "
                f"Телефон: {self.phone}, "
                f"Контактное лицо: {self.contact_person}")

    def __str__(self):
        return f"{self.name} ({self.ownership_type})"

    def __eq__(self, other):
        return isinstance(other, Client) and self.client_id == other.client_id
    


class ShortClient:
    def __init__(self, client: Client):
        self._client = client  # храним ссылку на оригинальный объект
    
    @property
    def client_id(self):
        return self._client.client_id
    
    @property
    def name(self):
        return self._client.name
    
    @property
    def ownership_type(self):
        return self._client.ownership_type
    
    @property
    def phone(self):
        return self._client.phone
    
    def __str__(self):
        return f"{self.name}, тел.: {self.phone}"
    
    def full_info(self):
        return f"{self.name} ({self.ownership_type}) - {self.phone}"  
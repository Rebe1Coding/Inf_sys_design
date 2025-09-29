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
from client import Client, ShortClient
import json



# ===== Создание клиентов =====

# 1. Через обычный конструктор
c1 = Client(1, "ООО Ромашка", "ООО", "Москва, ул. Пушкина, 10", "+79995553322", "Иванов Иван Иванович")

# 2. Через JSON
json_str = '{"client_id": 2, "name": "ЗАО Василёк", "ownership_type": "ЗАО", "address": "СПб, Невский 15", "phone": "+78125557788", "contact_person": "Петров Петр Петрович"}'
c2 = Client.from_json(json_str)

# 3. Через строку
str_data = "3;ИП Сидоров;ИП;Казань, Кремль, 1;+79270001122;Сидоров Сидор Сидорович"
c3 = Client.from_string(str_data)


# ===== Вывод информации =====
print("Краткая версия (str):")
print(c1)               # ООО Ромашка (ООО)
print(c2)               # ЗАО Василёк (ЗАО)

print("\nПолная версия (full_info):")
print(c1.full_info())
print(c2.full_info())

# ===== Сравнение =====
print("\nСравнение объектов:")
print(c1 == c2)  # False
c1_copy = Client(1, "ООО Ромашка", "ООО", "Москва, ул. Ленина, 99", "+79995553322", "Иванов Иван Иванович")
print(c1 == c1_copy)  # True (id одинаковый)


# ===== Использование ShortClient =====
short_c1 = ShortClient(c1)
short_c2 = ShortClient(c2)

print("\nКраткие версии клиентов:")
print(short_c1)              # ООО Ромашка, тел.: +79995553322
print(short_c2.full_info())  # ЗАО Василёк (+78125557788)

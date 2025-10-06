from client import Client, ShortClient
import json

from rep.client_rep_json import Client_rep_json
from rep.client_rep_yaml import Client_rep_yaml
# # ===== Создание клиентов =====

# # 1. Через обычный конструктор
# c1 = Client(1, "ООО Ромашка", "ООО", "Москва, ул. Пушкина, 10", "+79995553322", "Иванов Иван Иванович")

# # 2. Через JSON
# json_str = '{"client_id": 2, "name": "ЗАО Василёк", "ownership_type": "ЗАО", "address": "СПб, Невский 15", "phone": "+78125557788", "contact_person": "Петров Петр Петрович"}'
# c2 = Client.from_json(json_str)

# # 3. Через строку
# str_data = "3;ИП Сидоров;ИП;Казань, Кремль, 1;+79270001122;Сидоров Сидор Сидорович"
# c3 = Client.from_string(str_data)


# # ===== Вывод информации =====
# print("Краткая версия (str):")
# print(c1)               # ООО Ромашка (ООО)
# print(c2)               # ЗАО Василёк (ЗАО)

# print("\nПолная версия (full_info):")
# print(c1.full_info())
# print(c2.full_info())

# # ===== Сравнение =====
# print("\nСравнение объектов:")
# print(c1 == c2)  # False
# c1_copy = Client(1, "ООО Ромашка", "ООО", "Москва, ул. Ленина, 99", "+79995553322", "Иванов Иван Иванович")
# print(c1 == c1_copy)  # True (id одинаковый)


# # ===== Использование ShortClient =====
# short_c1 = ShortClient(c1)
# short_c2 = ShortClient(c2)

# print("\nКраткие версии клиентов:")
# print(short_c1)              # ООО Ромашка, тел.: +79995553322
# print(short_c2.full_info())  # ЗАО Василёк (+78125557788)




def use_client_repo_json(filename: str) -> None:
    """
    Демонстрация использования Client_rep_json:
    - загрузка из файла
    - добавление, обновление, удаление
    - краткие списки и сортировка
    """
    repo = Client_rep_json(filename)

    print("\nКлиенты из репозитория (до изменений):")
    for c in repo._clients:
        print(c.full_info())

    # Добавим нового клиента через add_client (репозиторий сам сгенерирует ID)
    new_data = {
        "name": "ООО Новое",
        "ownership_type": "ООО",
        "address": "г.Тест, ул. Новая, 1",
        "phone": "+70000000001",
        "contact_person": "Новиков Н.Н."
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())

    # Сохраняем изменения
    repo.write_all()

    # Обновим только что добавленного клиента
    if repo.update_client(new_client.client_id, {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"}):
        print("\nПосле обновления:")
        print(repo.get_by_id(new_client.client_id).full_info())

    # Показ краткого списка (k=2, n=1)
    print("\nКраткий список (k=2, n=1):")
    for s in repo.get_k_n_short_list(2, 1):
        print(s)

    # Сортируем по имени и выводим
    try:
        repo.sort_by_field("name")
        print("\nПосле сортировки по name:")
        for c in repo._clients:
            print(c.full_info())
    except ValueError as e:
        print("\nОшибка при сортировке:", e)

    # Удалим добавленного клиента
    if repo.delete_client(new_client.client_id):
        print(f"\nКлиент с id={new_client.client_id} удалён")
    else:
        print(f"\nНе удалось удалить клиента id={new_client.client_id}")

    # Сохраняем финальное состояние
    repo.write_all()
    print("\nОперации с репозиторием завершены.")



def use_client_repo_yaml(filename: str) -> None:
    """
    Демонстрация использования Client_rep_yaml:
    - загрузка из файла
    - добавление, обновление, удаление
    - краткие списки и сортировка
    """
    repo = Client_rep_yaml(filename)

    print("\nКлиенты из репозитория (до изменений):")
    for c in repo._clients:
        print(c.full_info())

    # Добавим нового клиента через add_client (репозиторий сам сгенерирует ID)
    new_data = {
        "name": "ООО Новое",
        "ownership_type": "ООО",
        "address": "г.Тест, ул. Новая, 1",
        "phone": "+70000000001",
        "contact_person": "Новиков Н.Н."
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())

    # Сохраняем изменения
    repo.write_all()

    # Обновим только что добавленного клиента
    if repo.update_client(new_client.client_id, {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"}):
        print("\nПосле обновления:")
        print(repo.get_by_id(new_client.client_id).full_info())

    # Показ краткого списка (k=2, n=1)
    print("\nКраткий список (k=2, n=1):")
    for s in repo.get_k_n_short_list(2, 1):
        print(s)

    # Сортируем по имени и выводим
    try:
        repo.sort_by_field("name")
        print("\nПосле сортировки по name:")
        for c in repo._clients:
            print(c.full_info())
    except ValueError as e:
        print("\nОшибка при сортировке:", e)

    # Удалим добавленного клиента
    if repo.delete_client(new_client.client_id):
        print(f"\nКлиент с id={new_client.client_id} удалён")
    else:
        print(f"\nНе удалось удалить клиента id={new_client.client_id}")

    # Сохраняем финальное состояние
    repo.write_all()
    print("\nОперации с репозиторием завершены.")


if __name__ == "__main__":
    use_client_repo_json("rep/clients.json")
    use_client_repo_yaml("rep/clients.yaml")

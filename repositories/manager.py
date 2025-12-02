from repositories.client_rep_json import Client_rep_json
from repositories.client_rep_yaml import Client_rep_yaml
from repositories.client_rep_db import Client_rep_DB
from repositories.repository import ClientDBAdapter
from config.db_conn import db_conn


def use_client_repo_json(filename="./data/clients.json") -> None:
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
        "contact_person": "Новиков Н.Н.",
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())

    # Сохраняем изменения
    repo.write_all()

    # Обновим только что добавленного клиента
    if repo.update_client(
        new_client.client_id,
        {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"},
    ):
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


def use_client_repo_yaml(filename="./data/clients.yaml") -> None:
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
        "contact_person": "Новиков Н.Н.",
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())

    # Сохраняем изменения
    repo.write_all()

    # Обновим только что добавленного клиента
    if repo.update_client(
        new_client.client_id,
        {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"},
    ):
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


def use_client_repo_db(db_params=db_conn) -> None:
    """
    Демонстрация использования Client_rep_DB через адаптер ClientDBAdapter:
    - загрузка из базы данных
    - добавление, обновление, удаление
    - краткие списки и сортировка
    """
    db_repo = Client_rep_DB(db_params)
    repo = ClientDBAdapter(db_repo)

    print("\nКлиенты из репозитория (до изменений):")
    for c in repo._clients:
        print(c.full_info())

    # Добавим нового клиента через add_client
    new_data = {
        "name": "ООО Новое",
        "ownership_type": "ООО",
        "address": "г.Тест, ул. Новая, 1",
        "phone": "+70000000001",
        "contact_person": "Новиков Н.Н.",
    }
    new_client = repo.add_client(new_data)
    print("\nДобавлен клиент:")
    print(new_client.full_info())

    # Обновим только что добавленного клиента
    if repo.update_client(
        new_client.client_id,
        {"address": "г.Тест, ул. Новая, 2", "phone": "+70000000002"},
    ):
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

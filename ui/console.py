import os
from datetime import datetime
from repositories.manager import (
    use_client_repo_json,
    use_client_repo_yaml,
    use_client_repo_db,
)


class ConsoleUI:
    """Класс для управления репозиториями клиентов"""

    def __init__(self):
        self.current_repo = None
        self.repo_type = None
        self.repo_name = None
        self.history = []

    def clear_screen(self):
        """Очистка экрана консоли"""
        os.system("cls" if os.name == "nt" else "clear")

    def show_banner(self):
        """Показать баннер с информацией"""
        print("\n" + "=" * 60)
        print("🎯 СИСТЕМА УПРАВЛЕНИЯ РЕПОЗИТОРИЯМИ КЛИЕНТОВ")
        print("=" * 60)
        if self.current_repo:
            print(f"📁 Текущий репозиторий: {self.repo_type} - {self.repo_name}")
        else:
            print("📁 Репозиторий не выбран")
        print(f"🕒 Время: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)

    def show_menu(self):
        """Отображение меню выбора репозитория"""
        print("\n" + "🔧 ДОСТУПНЫЕ РЕПОЗИТОРИИ")
        print("-" * 40)
        print("1. 📄 JSON репозиторий")
        print("2. 📊 YAML репозиторий")
        print("3. 🗄️  База данных")
        print("4. 📋 История выбора")
        print("5. 🚪 Выйти")
        print("-" * 40)

    def get_repository_choice(self):
        """Получение выбора пользователя"""
        while True:
            try:
                choice = input("🎲 Выберите действие (1-5): ").strip()
                if choice in ["1", "2", "3", "4", "5"]:
                    return choice
                else:
                    print("❌ Ошибка: введите число от 1 до 5")
            except KeyboardInterrupt:
                print("\n👋 Программа прервана пользователем")
                return "5"

    def add_to_history(self, repo_type, repo_name):
        """Добавить выбор в историю"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history.append({"time": timestamp, "type": repo_type, "name": repo_name})

    def show_history(self):
        """Показать историю выбора репозиториев"""
        self.clear_screen()
        self.show_banner()

        print("\n📋 ИСТОРИЯ ВЫБОРА РЕПОЗИТОРИЕВ")
        print("-" * 50)

        if not self.history:
            print("📝 История пуста")
            return

        for i, entry in enumerate(self.history, 1):
            print(f"{i}. 🕒 {entry['time']} | 📁 {entry['type']} | 🏷️  {entry['name']}")

        print("-" * 50)
        input("\nНажмите Enter для продолжения...")

    def use_json_repository(self):
        """Работа с JSON репозиторием"""
        filename = input(
            "📝 Введите имя файла JSON (по умолчанию: clients.json): "
        ).strip()
        if not filename:
            filename = "./data/clients.json"

        # Добавляем расширение .json если его нет
        if not filename.endswith(".json"):
            filename += ".json"

        try:
            use_client_repo_json(filename)
            self.current_repo = "JSON"
            self.repo_type = "JSON"
            self.repo_name = filename
            self.add_to_history("JSON", filename)
            print(f"✅ Успешно подключен JSON репозиторий: {filename}")
        except Exception as e:
            print(f"❌ Ошибка при работе с JSON репозиторием: {e}")

    def use_yaml_repository(self):
        """Работа с YAML репозиторием"""
        filename = input(
            "📝 Введите имя файла YAML (по умолчанию: clients.yaml): "
        ).strip()
        if not filename:
            filename = "./data/clients.yaml"

        # Добавляем расширение .yaml если его нет
        if not filename.endswith((".yaml", ".yml")):
            filename += ".yaml"

        try:
            use_client_repo_yaml(filename)
            self.current_repo = "YAML"
            self.repo_type = "YAML"
            self.repo_name = filename
            self.add_to_history("YAML", filename)
            print(f"✅ Успешно подключен YAML репозиторий: {filename}")
        except Exception as e:
            print(f"❌ Ошибка при работе с YAML репозиторием: {e}")

    def use_database_repository(self):
        """Работа с репозиторием базы данных"""
        try:
            db_type = "PostgreSQL"

            use_client_repo_db()
            self.current_repo = "Database"
            self.repo_type = "Database"
            self.repo_name = db_type
            self.add_to_history("Database", db_type)
            print(f"✅ Успешно подключен репозиторий базы данных: {db_type}")
        except Exception as e:
            print(f"❌ Ошибка при работе с базой данных: {e}")

    def show_repo_info(self):
        """Показать информацию о текущем репозитории"""
        if self.current_repo:
            print("\n📊 ИНФОРМАЦИЯ О РЕПОЗИТОРИИ:")
            print(f"   Тип: {self.repo_type}")
            print(f"   Имя: {self.repo_name}")
            print(
                f"   Время подключения: {self.history[-1]['time'] if self.history else 'N/A'}"
            )
        else:
            print("\n⚠️  Репозиторий не выбран")

    def run(self):
        """Основной цикл программы"""
        self.clear_screen()

        while True:
            self.clear_screen()
            self.show_banner()
            self.show_menu()

            choice = self.get_repository_choice()

            if choice == "5":
                print("\n👋 До свидания!")
                break

            if choice == "4":
                self.show_history()
                continue

            self.clear_screen()
            self.show_banner()

            # Обработка выбора репозитория
            if choice == "1":
                self.use_json_repository()
            elif choice == "2":
                self.use_yaml_repository()
            elif choice == "3":
                self.use_database_repository()

            # Показать информацию о текущем репозитории
            self.show_repo_info()

            # Запрос на продолжение
            print("\n" + "=" * 50)
            continue_choice = (
                input(
                    "\n🔄 Нажмите Enter для выбора нового репозитория или 'q' для выхода: "
                )
                .strip()
                .lower()
            )

            if continue_choice == "q":
                print("\n👋 До свидания!")
                break

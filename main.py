from ui.console import Manager
import sys





def main():
    """Основная функция программы"""
    try:
        manager = Manager()
        manager.run()
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    




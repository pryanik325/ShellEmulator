from src.config import load_config
from src.gui import run_gui


def main() -> None:
    try:
        config = load_config()
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"Ошибка конфигурации: {exc}")
        return

    run_gui(config)

if __name__ == "__main__":
    main()
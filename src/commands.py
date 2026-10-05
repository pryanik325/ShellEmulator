"""Встроенные команды оболочки (заглушки)."""

from typing import Callable, Dict, List, Optional

# Тип: список аргументов -> строка результата
CommandHandler = Callable[[List[str]], str]


def cmd_ls(args: List[str]) -> str:
    """Заглушка ls: имя команды и аргументы."""
    return f"ls args={args}"


def cmd_cd(args: List[str]) -> str:
    """Заглушка cd: имя команды и аргументы."""
    return f"cd args={args}"


def cmd_exit(args: List[str]) -> str:
    """Завершение работы. Возвращает маркер."""
    return "__EXIT__"


# Словарь зарегистрированных команд
COMMANDS: Dict[str, CommandHandler] = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}


def execute(
    command: Optional[str],
    args: List[str],
) -> str:
    """
    Выполняет разобранную команду.

    Args:
        command: Имя команды или None.
        args: Список аргументов.

    Returns:
        Строка результата. Значение "__EXIT__"
        означает выход из приложения.
    """
    if command is None:
        return ""

    handler = COMMANDS.get(command)
    if handler is None:
        name = command
        return f"Ошибка: неизвестная команда '{name}'"

    return handler(args) 
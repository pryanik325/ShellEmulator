"""Парсер командной строки с кавычками."""

import shlex
from typing import List, Optional, Tuple


def parse_command(
    line: str,
) -> Tuple[Optional[str], List[str]]:
    """
    Разбирает строку на команду и аргументы.

    Поддерживает одинарные и двойные кавычки.
    Пустая строка возвращает (None, []).

    Args:
        line: Строка пользователя.

    Returns:
        Кортеж (имя_команды, аргументы).
        Имя равно None, если строка пустая.

    Raises:
        ValueError: Если кавычки не закрыты.
    """
    stripped = line.strip()
    if not stripped:
        return None, []

    try:
        tokens = shlex.split(stripped, posix=True)
    except ValueError as exc:
        msg = f"ошибка разбора: {exc}"
        raise ValueError(msg) from exc

    if not tokens:
        return None, []

    command = tokens[0]
    args = tokens[1:]
    return command, args
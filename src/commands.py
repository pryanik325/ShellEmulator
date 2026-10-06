from typing import Callable, Dict, List, Optional

CommandHandler = Callable[[List[str]], str]


def cmd_ls(args: List[str]) -> str:
    return f"ls args={args}"


def cmd_cd(args: List[str]) -> str:
    return f"cd args={args}"


def cmd_exit(args: List[str]) -> str:
    return "__EXIT__"


COMMANDS: Dict[str, CommandHandler] = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "exit": cmd_exit,
}


def execute(
    command: Optional[str],
    args: List[str],
) -> str:
    if command is None:
        return ""

    handler = COMMANDS.get(command)
    if handler is None:
        name = command
        return f"Неизвестная команда '{name}'"

    return handler(args)
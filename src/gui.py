"""Графический интерфейс эмулятора (tkinter)."""

import getpass
import socket
import tkinter as tk
from tkinter import scrolledtext
from typing import Optional

from pathlib import Path

from src.commands import execute
from src.config import AppConfig, format_debug
from src.parser import parse_command


def get_window_title() -> str:
    """Заголовок окна по данным реальной ОС."""
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"Эмулятор - [{username}@{hostname}]"


class ShellGUI:
    """Главное окно эмулятора оболочки."""

    def __init__(
            self,
            root: tk.Tk,
            config: AppConfig,
    ) -> None:
        """
        Создаёт окно эмулятора.

        Args:
            root: Окно tkinter.
            config: Настройки запуска.
        """
        self.root = root
        self.config = config
        self.root.title(get_window_title())
        self.root.geometry("700x450")
        self.root.minsize(400, 300)

        self._build_widgets()
        self._bind_events()
        self._print_welcome()

        # Показать, какие параметры реально загрузились
        self._append(format_debug(config) + "\n")

        # Если указан стартовый скрипт — выполнить его
        if config.script_path:
            path = config.script_path
            self.root.after(
                100,
                lambda: self._run_startup_script(path),
            )

    def _build_widgets(self) -> None:
        """Создаёт и размещает виджеты."""
        self.output = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Consolas", 11),
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
        )
        self.output.pack(
            fill=tk.BOTH, expand=True, padx=4, pady=4
        )

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=4, pady=(0, 4))

        self.prompt_label = tk.Label(
            frame,
            text="> ",
            font=("Consolas", 11),
            fg="#4ec9b0",
        )
        self.prompt_label.pack(side=tk.LEFT)

        self.entry = tk.Entry(
            frame,
            font=("Consolas", 11),
            bg="#252526",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            relief=tk.FLAT,
        )
        self.entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True
        )
        self.entry.focus_set()

    def _bind_events(self) -> None:
        """Привязывает обработчики событий."""
        self.entry.bind("<Return>", self._on_enter)
        self.root.protocol(
            "WM_DELETE_WINDOW", self._on_close
        )

    def _print_welcome(self) -> None:
        """Выводит приветствие при запуске."""
        self._append(
            "Эмулятор оболочки (Этап 1)\n"
            "Команды: ls, cd, exit\n"
            'Кавычки: ls "имя файла.txt"\n'
            "------------------------------\n"
        )

    def _append(self, text: str) -> None:
        """
        Добавляет текст в область вывода.

        Args:
            text: Текст для отображения.
        """
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def _on_enter(
        self, event: Optional[tk.Event] = None
    ) -> None:
        """
        Обрабатывает Enter: разбор и выполнение.

        Args:
            event: Событие tkinter (не используется).
        """
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self._append(f"> {line}\n")

        try:
            command, args = parse_command(line)
        except ValueError as exc:
            self._append(f"Ошибка: {exc}\n")
            return

        result = execute(command, args)
        if result == "__EXIT__":
            self.root.destroy()
            return
        if result:
            self._append(result + "\n")

    def _on_close(self) -> None:
        """Обрабатывает закрытие окна."""
        self.root.destroy()

    def _run_startup_script(self, path: str) -> None:
        """
        Выполняет файл со командами эмулятора.
        Ошибки в отдельных строках не останавливают весь скрипт.
        """
        script = Path(path)
        if not script.is_file():
            self._append(
                f"Ошибка скрипта: файл не найден ({path})\n"
            )
            return

        self._append(f"--- Стартовый скрипт: {path} ---\n")

        try:
            lines = script.read_text(
                encoding="utf-8"
            ).splitlines()
        except OSError as exc:
            self._append(f"Ошибка чтения: {exc}\n")
            return

        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            # Как будто пользователь ввёл команду
            self._append(f"> {line}\n")

            try:
                command, args = parse_command(line)
            except ValueError as exc:
                self._append(f"Ошибка: {exc}\n")
                continue

            result = execute(command, args)
            if result == "__EXIT__":
                self._append("(exit — конец скрипта)\n")
                break
            if result:
                self._append(result + "\n")

        self._append("--- Конец скрипта ---\n")

def run_gui(config: AppConfig) -> None:
    """Запускает GUI с переданными настройками."""
    root = tk.Tk()
    ShellGUI(root, config)
    root.mainloop()
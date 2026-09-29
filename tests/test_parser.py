"""Модульные тесты парсера."""

import unittest

from src.parser import parse_command


class TestParseCommand(unittest.TestCase):
    """Тесты функции parse_command."""

    def test_empty(self) -> None:
        """Пустой ввод и ввод из пробелов."""
        self.assertEqual(parse_command(""), (None, []))
        self.assertEqual(
            parse_command("   "), (None, [])
        )

    def test_simple(self) -> None:
        """Команда без аргументов."""
        self.assertEqual(parse_command("ls"), ("ls", []))
        self.assertEqual(
            parse_command("  cd  "), ("cd", [])
        )

    def test_args(self) -> None:
        """Команда с обычными аргументами."""
        cmd, args = parse_command("ls -l /tmp")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["-l", "/tmp"])

    def test_double_quotes(self) -> None:
        """Аргументы в двойных кавычках."""
        cmd, args = parse_command('ls "my file.txt"')
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["my file.txt"])

    def test_single_quotes(self) -> None:
        """Аргументы в одинарных кавычках."""
        line = "cd 'dir with spaces'"
        cmd, args = parse_command(line)
        self.assertEqual(cmd, "cd")
        self.assertEqual(args, ["dir with spaces"])

    def test_mixed(self) -> None:
        """Смешанные аргументы с кавычками."""
        line = 'ls -la "file 1" file2'
        cmd, args = parse_command(line)
        self.assertEqual(cmd, "ls")
        self.assertEqual(
            args, ["-la", "file 1", "file2"]
        )

    def test_unclosed_quote(self) -> None:
        """Незакрытая кавычка → ValueError."""
        with self.assertRaises(ValueError):
            parse_command('ls "unclosed')


if __name__ == "__main__":
    unittest.main()
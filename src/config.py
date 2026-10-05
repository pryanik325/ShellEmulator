"""Чтение параметров запуска: CLI и TOML."""

import argparse
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class AppConfig:
    """Итоговые настройки приложения."""

    vfs_path: Optional[str] = None
    script_path: Optional[str] = None
    config_path: Optional[str] = None


def parse_cli(argv: Optional[list] = None) -> AppConfig:
    """Читает только аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС",
    )
    parser.add_argument(
        "--vfs",
        dest="vfs_path",
        default=None,
        help="Путь к VFS",
    )
    parser.add_argument(
        "--script",
        dest="script_path",
        default=None,
        help="Путь к стартовому скрипту",
    )
    parser.add_argument(
        "--config",
        dest="config_path",
        default=None,
        help="Путь к TOML-конфигу",
    )
    args = parser.parse_args(argv)
    return AppConfig(
        vfs_path=args.vfs_path,
        script_path=args.script_path,
        config_path=args.config_path,
    )


def load_toml(path: str) -> AppConfig:
    """Читает настройки из TOML-файла."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Конфиг не найден: {path}"
        )

    with file_path.open("rb") as f:
        data = tomllib.load(f)

    return AppConfig(
        vfs_path=data.get("vfs_path"),
        script_path=data.get("script_path"),
        config_path=path,
    )


def merge_configs(
    cli: AppConfig,
    file_cfg: Optional[AppConfig],
) -> AppConfig:
    """
    Склеивает настройки.
    Если в CLI что-то указано — берём CLI, иначе из файла.
    """
    if file_cfg is None:
        return AppConfig(
            vfs_path=cli.vfs_path,
            script_path=cli.script_path,
            config_path=cli.config_path,
        )

    return AppConfig(
        vfs_path=(
            cli.vfs_path
            if cli.vfs_path is not None
            else file_cfg.vfs_path
        ),
        script_path=(
            cli.script_path
            if cli.script_path is not None
            else file_cfg.script_path
        ),
        config_path=cli.config_path or file_cfg.config_path,
    )


def load_config(argv: Optional[list] = None) -> AppConfig:
    """Полная загрузка: сначала CLI, потом файл, потом склейка."""
    cli = parse_cli(argv)
    file_cfg = None
    if cli.config_path:
        file_cfg = load_toml(cli.config_path)
    return merge_configs(cli, file_cfg)


def format_debug(cfg: AppConfig) -> str:
    """Текст для отладки: что реально получилось."""
    return "\n".join([
        "=== Отладка параметров ===",
        f"  vfs_path    = {cfg.vfs_path!r}",
        f"  script_path = {cfg.script_path!r}",
        f"  config_path = {cfg.config_path!r}",
        "==========================",
    ])
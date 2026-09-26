"""Configuration centralisée du bot SITE-453.

Les valeurs par défaut permettent d'importer le module sans fichier ``.env``.
Le token reste volontairement absent par défaut : le bot ne démarre pas sans
``DISCORD_TOKEN``.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", encoding="utf-8-sig")

BOT_NAME = "SITE-453"
BOT_VERSION = "2.0.5"


def _int_env(name: str, default: int = 0) -> int:
    try:
        return int(os.getenv(name, str(default)).strip())
    except (TypeError, ValueError):
        return default


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on", "oui"}


def _ids_env(name: str) -> set[int]:
    result: set[int] = set()
    for chunk in os.getenv(name, "").split(","):
        chunk = chunk.strip()
        if chunk.isdigit() and int(chunk) > 0:
            result.add(int(chunk))
    return result


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
BOT_PREFIX = os.getenv("BOT_PREFIX", "!").strip() or "!"
if BOT_PREFIX == "/":
    BOT_PREFIX = "!"

BOT_ACTIVITY = os.getenv("BOT_ACTIVITY", "").strip() or f"SITE-453 — {BOT_NAME}"
BOT_OWNER_ID = _int_env("BOT_OWNER_ID")
CO_OWNER_IDS = _ids_env("CO_OWNER_IDS")
GLOBAL_ADMIN_IDS = _ids_env("GLOBAL_ADMIN_IDS")
GUILD_ID = _int_env("GUILD_ID")

LOG_CHANNEL_ID = _int_env("LOG_CHANNEL_ID")
SUPPORT_SERVER = os.getenv("SUPPORT_SERVER", "").strip()
DASHBOARD_URL = os.getenv("DASHBOARD_URL", "").strip()
DEV_CREDITS = os.getenv("DEV_CREDITS", "nathanre0100 — fondateur SITE-453").strip()
NEXUS_SECRET = os.getenv("NEXUS_SECRET", "").strip()
NEXUS_PORT = _int_env("NEXUS_PORT", 8765)

ENABLE_MUSIC = _bool_env("ENABLE_MUSIC", False)
ENABLE_TICKETS = _bool_env("ENABLE_TICKETS", True)
ENABLE_LOGS = _bool_env("ENABLE_LOGS", True)
ENABLE_MESSAGE_CONTENT = _bool_env("ENABLE_MESSAGE_CONTENT", True)
ENABLE_MEMBERS = _bool_env("ENABLE_MEMBERS", True)

BOT_MANAGER_IDS = CO_OWNER_IDS | GLOBAL_ADMIN_IDS | ({BOT_OWNER_ID} if BOT_OWNER_ID else set())

DEFAULT_DATABASE_URL = "sqlite:///./data/database.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL).strip() or DEFAULT_DATABASE_URL

COLOR_ERROR = 0xE74C3C
COLOR_SUCCESS = 0x2ECC71
COLOR_INFO = 0x3498DB
COLOR_WARNING = 0xF1C40F


def sqlite_database_path() -> str:
    url = DATABASE_URL
    prefix = "sqlite:///"
    if not url.startswith(prefix):
        url = DEFAULT_DATABASE_URL
    configured = url[len(prefix):]
    if configured in {"", ":memory:"}:
        return ":memory:"

    path = Path(configured)
    if not path.is_absolute():
        path = BASE_DIR / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)

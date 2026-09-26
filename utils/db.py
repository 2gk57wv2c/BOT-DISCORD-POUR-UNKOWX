import sqlite3

DB_PATH = "bot.db"

LEVEL_ORDER = {
    "founder": 5,
    "cofounder": 4,
    "admin": 3,
    "moderator": 2,
    "member": 1,
    "none": 0,
}


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS guild_config (
            guild_id INTEGER PRIMARY KEY,
            raid INTEGER DEFAULT 0,
            anti_spam INTEGER DEFAULT 0,
            logs_channel_id INTEGER DEFAULT NULL,
            verification_role_id INTEGER DEFAULT NULL,
            non_verified_role_id INTEGER DEFAULT NULL,
            welcome_message TEXT DEFAULT NULL,
            bot_prefix TEXT DEFAULT '!'
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS permissions (
            guild_id INTEGER,
            user_id INTEGER,
            level TEXT,
            reason TEXT,
            granted_by INTEGER,
            granted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (guild_id, user_id)
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS warns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS kick_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS bans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS blacklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def get_guild_config(guild_id: int):
    conn = connect_db()
    row = conn.execute("SELECT * FROM guild_config WHERE guild_id = ?", (guild_id,)).fetchone()
    conn.close()

    if row is None:
        conn = connect_db()
        conn.execute("INSERT INTO guild_config (guild_id) VALUES (?)", (guild_id,))
        conn.commit()
        conn.close()
        return {
            "guild_id": guild_id,
            "raid": 0,
            "anti_spam": 0,
            "logs_channel_id": None,
            "verification_role_id": None,
            "non_verified_role_id": None,
            "welcome_message": None,
            "bot_prefix": "!",
        }
    return dict(row)


def update_guild_config(guild_id: int, **kwargs):
    if not kwargs:
        return
    conn = connect_db()
    set_clause = ", ".join(f"{key} = ?" for key in kwargs)
    values = list(kwargs.values()) + [guild_id]
    conn.execute(f"UPDATE guild_config SET {set_clause} WHERE guild_id = ?", tuple(values))
    conn.commit()
    conn.close()


def get_level_for_user(guild_id: int, user_id: int):
    conn = connect_db()
    row = conn.execute(
        "SELECT level FROM permissions WHERE guild_id = ? AND user_id = ?",
        (guild_id, user_id),
    ).fetchone()
    conn.close()
    return row["level"] if row else "none"


def set_user_level(guild_id: int, user_id: int, level: str, reason: str, granted_by: int):
    conn = connect_db()
    conn.execute(
        """
        INSERT INTO permissions (guild_id, user_id, level, reason, granted_by)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(guild_id, user_id)
        DO UPDATE SET
            level = excluded.level,
            reason = excluded.reason,
            granted_by = excluded.granted_by,
            granted_at = CURRENT_TIMESTAMP
        """,
        (guild_id, user_id, level, reason, granted_by),
    )
    conn.commit()
    conn.close()


def remove_user_level(guild_id: int, user_id: int):
    conn = connect_db()
    conn.execute("DELETE FROM permissions WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
    conn.commit()
    conn.close()


def get_all_permissions(guild_id: int):
    conn = connect_db()
    rows = conn.execute(
        "SELECT * FROM permissions WHERE guild_id = ? ORDER BY level DESC, user_id ASC",
        (guild_id,),
    ).fetchall()
    conn.close()
    return rows


def add_warn(guild_id: int, user_id: int, moderator_id: int, reason: str):
    conn = connect_db()
    conn.execute(
        "INSERT INTO warns (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
        (guild_id, user_id, moderator_id, reason),
    )
    conn.commit()
    conn.close()


def get_warns(guild_id: int, user_id: int):
    conn = connect_db()
    rows = conn.execute(
        "SELECT * FROM warns WHERE guild_id = ? AND user_id = ? ORDER BY created_at DESC",
        (guild_id, user_id),
    ).fetchall()
    conn.close()
    return rows


def clear_warns(guild_id: int, user_id: int):
    conn = connect_db()
    conn.execute("DELETE FROM warns WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
    conn.commit()
    conn.close()


def add_kick_log(guild_id: int, user_id: int, moderator_id: int, reason: str):
    conn = connect_db()
    conn.execute(
        "INSERT INTO kick_logs (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
        (guild_id, user_id, moderator_id, reason),
    )
    conn.commit()
    conn.close()


def get_kick_logs(guild_id: int, user_id: int):
    conn = connect_db()
    rows = conn.execute(
        "SELECT * FROM kick_logs WHERE guild_id = ? AND user_id = ? ORDER BY created_at DESC",
        (guild_id, user_id),
    ).fetchall()
    conn.close()
    return rows


def add_ban(guild_id: int, user_id: int, moderator_id: int, reason: str):
    conn = connect_db()
    conn.execute(
        "INSERT INTO bans (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
        (guild_id, user_id, moderator_id, reason),
    )
    conn.commit()
    conn.close()


def get_bans(guild_id: int):
    conn = connect_db()
    rows = conn.execute(
        "SELECT * FROM bans WHERE guild_id = ? ORDER BY created_at DESC",
        (guild_id,),
    ).fetchall()
    conn.close()
    return rows


def add_blacklist(guild_id: int, user_id: int, moderator_id: int, reason: str):
    conn = connect_db()
    conn.execute(
        "INSERT INTO blacklist (guild_id, user_id, moderator_id, reason) VALUES (?, ?, ?, ?)",
        (guild_id, user_id, moderator_id, reason),
    )
    conn.commit()
    conn.close()


def get_blacklist(guild_id: int):
    conn = connect_db()
    rows = conn.execute(
        "SELECT * FROM blacklist WHERE guild_id = ? ORDER BY created_at DESC",
        (guild_id,),
    ).fetchall()
    conn.close()
    return rows


def remove_blacklist(guild_id: int, user_id: int):
    conn = connect_db()
    conn.execute("DELETE FROM blacklist WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
    conn.commit()
    conn.close()


def ensure_owner(user_id: int, owner_ids):
    return user_id in owner_ids


def user_has_at_least(guild_id: int, user_id: int, required_level: str, owner_ids=None, level_order=None):
    if owner_ids is not None and user_id in owner_ids:
        return True
    if level_order is None:
        level_order = LEVEL_ORDER
    current = get_level_for_user(guild_id, user_id)
    current_rank = level_order.get(current, 0)
    required_rank = level_order.get(required_level, 0)
    return current_rank >= required_rank


def log_event(guild, title: str, message: str):
    import asyncio
    import discord

    cfg = get_guild_config(guild.id)
    channel_id = cfg.get("logs_channel_id")
    if not channel_id:
        return
    channel = guild.get_channel(channel_id)
    if channel is None:
        return

    embed = discord.Embed(
        title=title,
        description=message,
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow(),
    )
    try:
        asyncio.create_task(channel.send(embed=embed))
    except Exception:
        pass

import aiosqlite

DB_PATH = "log_matrix.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT,
                group_id TEXT,
                timestamp TEXT,
                user TEXT,
                content TEXT,
                meta TEXT
            )"""
        )
        await db.commit()

async def log_message(data):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO logs (platform, group_id, timestamp, user, content, meta) VALUES (?, ?, ?, ?, ?, ?)",
            (
                data["platform"],
                str(data["group_id"]),
                data["timestamp"],
                data["user"],
                data["content"],
                str(data["meta"])
            )
        )
        await db.commit()

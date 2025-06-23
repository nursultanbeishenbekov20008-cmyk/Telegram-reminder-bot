import aiosqlite

async def init_db():
    async with aiosqlite.connect("reminders.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                remind_at DATETIME
            )
        """)
        await db.commit()

async def add_reminder(user_id, text, remind_at):
    async with aiosqlite.connect("reminders.db") as db:
        await db.execute("INSERT INTO reminders (user_id, text, remind_at) VALUES (?, ?, ?)", 
                         (user_id, text, remind_at))
        await db.commit()
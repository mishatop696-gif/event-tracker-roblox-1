
import sqlite3

DB_NAME = "events.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                username TEXT NOT NULL,
                event_name TEXT,
                game_url TEXT,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                notifications INTEGER DEFAULT 1,
                admin_enabled INTEGER DEFAULT 1,
                video_star_enabled INTEGER DEFAULT 1,
                developers_enabled INTEGER DEFAULT 1
            )
        """)

def add_detection(category, username, event_name="", game_url=""):
    with connect() as db:
        db.execute(
            """INSERT INTO detections
            (category, username, event_name, game_url)
            VALUES (?, ?, ?, ?)""",
            (category, username, event_name, game_url)
        )

def get_latest(limit=10):
    with connect() as db:
        return db.execute(
            """SELECT category, username, event_name,
            game_url, detected_at
            FROM detections
            ORDER BY id DESC LIMIT ?""",
            (limit,)
        ).fetchall()

def save_user(user_id):
    with connect() as db:
        db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,)
        )

if __name__ == "__main__":
    init_db()
    print("Database initialized!")
  

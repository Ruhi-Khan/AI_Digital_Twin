import sqlite3
from pathlib import Path
from contextlib import contextmanager


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Database folder
DATABASE_DIR = BASE_DIR / "database"

# Create database folder if it does not exist
DATABASE_DIR.mkdir(exist_ok=True)

# Database file
DATABASE_PATH = DATABASE_DIR / "digital_twin.db"


@contextmanager
def get_db():
    """
    Opens a connection to the SQLite database.

    The connection automatically closes after use.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    """
    Creates all required database tables.
    """

    with get_db() as db:

        # Users table
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                points INTEGER DEFAULT 0
            )
        """)

        # Technologies table
        db.execute("""
            CREATE TABLE IF NOT EXISTS technologies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                score INTEGER NOT NULL,
                growth REAL NOT NULL,
                popularity INTEGER NOT NULL
            )
        """)

        # Hiring signals
        db.execute("""
            CREATE TABLE IF NOT EXISTS hiring_signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                sector TEXT NOT NULL,
                openings INTEGER NOT NULL,
                growth REAL NOT NULL,
                signal TEXT NOT NULL
            )
        """)

        # AI tools
        db.execute("""
            CREATE TABLE IF NOT EXISTS ai_tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                popularity INTEGER NOT NULL,
                weekly_change REAL NOT NULL
            )
        """)

        # Cyber threats
        db.execute("""
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                severity TEXT NOT NULL,
                category TEXT NOT NULL,
                activity TEXT NOT NULL
            )
        """)

        # Startups
        db.execute("""
            CREATE TABLE IF NOT EXISTS startups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sector TEXT NOT NULL,
                location TEXT NOT NULL,
                funding TEXT NOT NULL,
                momentum INTEGER NOT NULL
            )
        """)

        # Activity feed
        db.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def fetch_all(table_name):
    """
    Safely fetches all rows from a known table.
    """

    allowed_tables = {
        "technologies",
        "hiring_signals",
        "ai_tools",
        "threats",
        "startups",
        "activities",
        "users"
    }

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name")

    with get_db() as db:
        rows = db.execute(
            f"SELECT * FROM {table_name}"
        ).fetchall()

    return [dict(row) for row in rows]


def fetch_one(query, parameters=()):
    """
    Executes a SELECT query and returns one row.
    """

    with get_db() as db:
        row = db.execute(query, parameters).fetchone()

    if row:
        return dict(row)

    return None


def execute(query, parameters=()):
    """
    Executes INSERT, UPDATE or DELETE query.
    """

    with get_db() as db:
        cursor = db.execute(query, parameters)
        return cursor.lastrowid
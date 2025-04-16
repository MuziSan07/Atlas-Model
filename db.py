import sqlite3
from pathlib import Path

DB_PATH = "gateway.db"

def get_db():
    """
    Connect to the SQLite database and return a connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables dict-like row access
    return conn

def init_db():
    """
    Initialize database tables for tokens and logs.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Create tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            tier TEXT,
            rate_limit INTEGER,
            is_active INTEGER DEFAULT 1
        );
    """)

    # Create usage logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT,
            endpoint TEXT,
            status_code INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()

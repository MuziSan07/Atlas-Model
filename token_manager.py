import secrets
from db import get_db

def generate_token(tier: str = "free", rate_limit: int = 60):
    """
    Generate a new unique token with optional tier and rate limit.
    """
    token = secrets.token_hex(16)
    conn = get_db()
    conn.execute(
        "INSERT INTO tokens (token, tier, rate_limit) VALUES (?, ?, ?)",
        (token, tier, rate_limit)
    )
    conn.commit()
    conn.close()
    return token

def update_token_status(token: str, is_active: int):
    """
    Set a token's active status. (1 = active, 0 = revoked)
    """
    conn = get_db()
    conn.execute(
        "UPDATE tokens SET is_active=? WHERE token=?",
        (is_active, token)
    )
    conn.commit()
    conn.close()

def delete_token(token: str):
    """
    Permanently delete a token from the database.
    """
    conn = get_db()
    conn.execute("DELETE FROM tokens WHERE token=?", (token,))
    conn.commit()
    conn.close()

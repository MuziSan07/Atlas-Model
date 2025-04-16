from fastapi import Request, HTTPException
from db import get_db

def validate_token(request: Request):
    """
    Validate token from Authorization header.
    Checks if the token exists and is active.
    """
    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization token.")

    conn = get_db()
    cursor = conn.execute(
        "SELECT * FROM tokens WHERE token = ?", (token,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=403, detail="Invalid token.")

    if not row["is_active"]:
        raise HTTPException(status_code=403, detail="Token has been revoked.")

    return dict(row)  # includes tier, rate_limit, etc.

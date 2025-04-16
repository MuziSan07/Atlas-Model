from fastapi import APIRouter, HTTPException
from token_manager import generate_token, update_token_status, delete_token
from db import get_db

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/token/")
def create_token(tier: str = "free", rate_limit: int = 60):
    """
    Create a new token with a tier and rate limit.
    """
    token = generate_token(tier, rate_limit)
    return {"token": token}

@router.post("/revoke/")
def revoke_token(token: str):
    """
    Revoke (deactivate) a token.
    """
    update_token_status(token, is_active=0)
    return {"status": "revoked", "token": token}

@router.post("/restore/")
def restore_token(token: str):
    """
    Restore (reactivate) a token.
    """
    update_token_status(token, is_active=1)
    return {"status": "restored", "token": token}

@router.delete("/token/")
def remove_token(token: str):
    """
    Permanently delete a token.
    """
    delete_token(token)
    return {"status": "deleted", "token": token}

@router.get("/logs/")
def get_usage_logs(limit: int = 100):
    """
    Get recent usage logs (default: 100 latest).
    """
    conn = get_db()
    cursor = conn.execute(
        "SELECT * FROM usage_logs ORDER BY timestamp DESC LIMIT ?", (limit,)
    )
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"logs": logs}

import time
from fastapi import HTTPException

# In-memory store for token request timestamps
request_timestamps = {}

def check_rate_limit(token: str, rate_limit: int):
    """
    Check and enforce the rate limit for a given token.
    """
    now = time.time()
    window = 60  # 60 seconds (1 minute)

    # Get previous timestamps or initialize
    timestamps = request_timestamps.get(token, [])
    
    # Keep only requests within the last 60 seconds
    timestamps = [ts for ts in timestamps if now - ts < window]

    if len(timestamps) >= rate_limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded ({rate_limit} requests/minute)."
        )

    # Add current timestamp and update store
    timestamps.append(now)
    request_timestamps[token] = timestamps

from fastapi import APIRouter, Request, HTTPException
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from auth import validate_token
from rate_limiter import check_rate_limit
from db import get_db

# Load model & tokenizer once when the server starts
tokenizer = AutoTokenizer.from_pretrained("MBZUAI-Paris/Atlas-Chat-2B")
model = AutoModelForCausalLM.from_pretrained("MBZUAI-Paris/Atlas-Chat-2B")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

router = APIRouter()

@router.post("/proxy/")
async def proxy(request: Request):
    """
    Secure proxy endpoint to locally run the model and return a response.
    Expects: { "messages": [{ "role": "user", "content": "..." }, ...] }
    """
    token_data = validate_token(request)
    token_str = request.headers.get("Authorization")
    check_rate_limit(token_str, token_data["rate_limit"])

    data = await request.json()
    messages = data.get("messages")

    if not messages:
        raise HTTPException(status_code=400, detail="Missing 'messages' in request body.")

    # Build a simple prompt from chat-style messages
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages]) + "\nassistant:"

    try:
        output = pipe(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)[0]["generated_text"]
        response_text = output[len(prompt):].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Log the request
    conn = get_db()
    conn.execute(
        "INSERT INTO usage_logs (token, endpoint, status_code) VALUES (?, ?, ?)",
        (token_str, "/proxy/", 200)
    )
    conn.commit()
    conn.close()

    return {"response": response_text}

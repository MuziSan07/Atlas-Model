# from fastapi import FastAPI
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
# from db import init_db
# from proxy import router as proxy_router
# from admin import router as admin_router
# from rate_limiter import check_rate_limit
# import logging

# # Initialize the database (tables)
# init_db()

# # Create FastAPI app instance
# app = FastAPI()

# # Middleware to log all requests
# @app.middleware("http")
# async def log_requests(request, call_next):
#     # Log request info (for debugging)
#     logging.info(f"Request: {request.method} {request.url}")
    
#     response = await call_next(request)
    
#     # You can log response details as well if needed
#     logging.info(f"Response: {response.status_code}")
    
#     return response

# # Include proxy and admin routes
# app.include_router(proxy_router)
# app.include_router(admin_router)

# # To protect from invalid host headers or unauthorized routes (example)
# app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"])

# # Optionally, configure logging
# logging.basicConfig(level=logging.INFO)


from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from db import init_db
from proxy import router as proxy_router
from admin import router as admin_router
from rate_limiter import check_rate_limit
from fastapi.responses import HTMLResponse
from fastapi import Request
import logging
import os

# Initialize the database (tables)
init_db()

# Create FastAPI app instance
app = FastAPI()

# Register templates folder
templates = Jinja2Templates(directory="templates")

# Static files setup (if you have CSS or JS to serve)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Middleware to log all requests
@app.middleware("http")
async def log_requests(request, call_next):
    # Log request info (for debugging)
    logging.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # You can log response details as well if needed
    logging.info(f"Response: {response.status_code}")
    
    return response

# Include proxy and admin routes
app.include_router(proxy_router)
app.include_router(admin_router)

# To protect from invalid host headers or unauthorized routes (example)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"])

# Optionally, configure logging
logging.basicConfig(level=logging.INFO)

# Home route to test the templates
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# Route to serve the token testing page
@app.get("/test-model", response_class=HTMLResponse)
async def test_model_page(request: Request):
    return templates.TemplateResponse("test_model.html", {"request": request})

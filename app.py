# app.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers.game_router import router as game_router
from game_logic import database # Import database to ensure initialization runs on startup
import os

app = FastAPI(title="Tic Tac Toe Game API")

# --- Configuration for Static Files and Templates ---
# Get the absolute path of the directory containing app.py
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

# Mount static files directory
# Ensure the 'static' directory exists relative to app.py
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"Warning: Static directory not found at {static_dir}")

# Configure templates
# Ensure the 'templates' directory exists relative to app.py
if os.path.isdir(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    print(f"Warning: Templates directory not found at {templates_dir}")
    templates = None # Handle case where templates are missing

# --- Include API Routers ---
app.include_router(game_router, prefix="/api", tags=["Game API"])

# --- Root Endpoint to Serve HTML ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    if templates:
        # Pass the request object to the template context
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return HTMLResponse("<html><body><h1>Error: Template directory not found.</h1></body></html>", status_code=500)

# --- Optional: Add simple health check endpoint ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# --- (Optional) Run database initialization check on startup ---
# database.initialize_database() # Already called when database module is imported

if __name__ == "__main__":
    import uvicorn
    print("Starting server with Uvicorn...")
    # For development, run directly: uvicorn app:app --reload
    # The following line is usually not needed if using `uvicorn app:app` command
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    print("Hint: Run the server using the command: uvicorn app:app --reload")
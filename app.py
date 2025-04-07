# === app.py ===
"""
Tic‑Tac‑Toe FastAPI entry point.

This module is responsible for:
- Creating the FastAPI application instance.
- Configuring static file and Jinja2 template handling so the front‑end assets
  can be served by the same process that hosts the JSON API.
- Registering the API routes defined in *routers/game_router.py* under the
  "/api" prefix.
- Providing a root endpoint that returns the HTML page where the user can play
  the game.
- Offering a lightweight health‑check endpoint useful for deployment
  monitoring.

Run locally with:
    uvicorn app:app --reload
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers.game_router import router as game_router
from game_logic import database  # Import database to ensure initialization runs on startup
import os

# ----------------------------------------------------------------------------
# Application initialisation
# ----------------------------------------------------------------------------
app = FastAPI(title="Tic Tac Toe Game API")

# --- Configuration for Static Files and Templates ---
# Get the absolute path of the directory containing app.py so the application
# works no matter where it is launched from.
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

# Mount the directory that contains CSS / JS / images at the URL path "/static".
# This allows the front‑end to request, e.g. /static/style.css.
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    # Failing silently would make debugging difficult, so print a warning.
    print(f"Warning: Static directory not found at {static_dir}")

# Configure the Jinja2 template loader.  The HTML templates live in the
# *templates* folder next to *app.py*.
if os.path.isdir(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    print(f"Warning: Templates directory not found at {templates_dir}")
    templates = None  # Fallback when templates are missing

# --- Include API Routers ---
# All JSON endpoints for the game are grouped in *game_router* and mounted under
# "/api".  Tagging them as "Game API" improves the automatically generated docs
# at /docs.
app.include_router(game_router, prefix="/api", tags=["Game API"])

# ----------------------------------------------------------------------------
# HTTP endpoints
# ----------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Return the main web page or a 500 error if templates are unavailable."""
    if templates:
        # Jinja2 needs the *request* in the context for url_for() to work.
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return HTMLResponse(
            "<html><body><h1>Error: Template directory not found.</h1></body></html>",
            status_code=500,
        )


@app.get("/health")
async def health_check():
    """Simple liveness probe endpoint used by orchestration platforms."""
    return {"status": "ok"}

# Database initialisation is executed when *game_logic.database* is imported at
# the top of this file, therefore no explicit startup hook is necessary.

# ----------------------------------------------------------------------------
# Convenience for running via `python app.py` (not required in production)
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    print("Starting server with Uvicorn...")
    # During development you can simply execute: uvicorn app:app --reload
    # The explicit call below is commented out because running the module with
    # `python app.py` is less common in modern ASGI deployments.
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    print("Hint: Run the server using the command: uvicorn app:app --reload")
"""This will be the main entry point for the server."""

import secrets
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.sessions import SessionMiddleware
from fastapi_tailwind import tailwind
from os import path

from routers import htmx, reports, users
from utils import config

secret = secrets.token_hex(32)

static_files = StaticFiles(directory="public")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI app."""

    # Setup Tailwind

    styles_dir = path.join(str(static_files.directory), "styles")

    process = tailwind.compile(
        path.join(styles_dir, "output.css"),
        tailwind_stylesheet_path=path.join(styles_dir, "input.css"),
    )

    """Connect to the database."""
    client = AsyncIOMotorClient(config.mongo_uri)
    db = client.get_database(config.mongo_db_name)

    setattr(app, "mongodb", db)
    yield

    # Terminate Tailwind

    process.terminate()

    # Close the database connection when the app is shutting down
    client.close()


app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

app.mount("/static", static_files, name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=secret,
    max_age=3600,  # 1 hour
)

app.include_router(htmx.router)
app.include_router(users.router)
app.include_router(reports.router)


@app.get("/")
async def root(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/login", 302)
    return templates.TemplateResponse("index.html", context={"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000)

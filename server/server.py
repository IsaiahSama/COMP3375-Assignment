"""This will be the main entry point for the server."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_tailwind import tailwind

from dotenv import dotenv_values
from pymongo import MongoClient

from os import path

config = dotenv_values(".env")

try:
    from .routers import htmx, users, reports
except ImportError:
    from routers import htmx, users, reports

static_files = StaticFiles(directory="public")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI app."""

    # Setup Tailwind

    styles_dir = path.join(str(static_files.directory), "styles")

    process = tailwind.compile(
        path.join(styles_dir, "output.css"),
        tailwind_stylesheet_path=path.join(styles_dir, "input.css")
    )

    """Connect to the database."""
#     app.mongodb_client = MongoClient(config["MONGO_URI"])
#     app.mongodb = app.mongodb_client[config["MONGO_DB_NAME"]]
    yield

    # Terminate Tailwind 
    
    process.terminate()

    # Close the database connection when the app is shutting down
#     if hasattr(app, "mongodb_client"):
#         app.mongodb_client.close()

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

app.include_router(htmx.router)
app.include_router(users.router)
app.include_router(reports.router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request, "text": "Hello from the server!"})


if __name__ == "__main__":    
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000)

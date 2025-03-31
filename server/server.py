"""This will be the main entry point for the server."""

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

try:
    from .routers import htmx
except ImportError:
    from routers import htmx

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="public"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(htmx.router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request, "text": "Hello from the server!"})


if __name__ == "__main__":    
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000)
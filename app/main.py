from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse

from app.db.database import engine, Base
from app.models.analysis import Analysis
from app.models.rules import Rules

from app.api import analyze


Base.metadata.create_all(bind=engine)

app = FastAPI(title="docx-validation-ai-system")

app.include_router(analyze.router)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = str(BASE_DIR.parent / "static")


@app.get("/checkfile")
async def serve_frontend():
    return FileResponse(
        str(STATIC_DIR + "/index.html"),
        headers={"Cache-Control": "no-store, no-cache, must-revalidate"},
    )


@app.get("/")
async def redirect_to_app():
    return RedirectResponse(url="/checkfile", status_code=302)

app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse


app = FastAPI(title="docx-validation-ai-system")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = str(BASE_DIR.parent / "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/checkfile")
async def serve_frontend():
    return FileResponse(str(STATIC_DIR + "/index.html"))

@app.get("/")
async def redirect_to_app():
    return RedirectResponse(url="/checkfile", status_code=302)
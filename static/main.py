from fastapi import FastAPI

app = FastAPI(title="docx-validation-ai-system")

@app.get("/health")
def health():
    return {"status": "ok"}

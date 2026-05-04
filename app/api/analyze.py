from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.ai_service import analyze_rules
from app.db.database import get_db
from app.utils import extract_text_from_docx

# יצירת הראוטר
router = APIRouter(prefix="/api", tags=["Analysis"])

@router.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    rules: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")

    if not rules.strip():
        raise HTTPException(status_code=400, detail="Rules cannot be empty")

    try:
        document_text = extract_text_from_docx(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

    if not document_text:
        raise HTTPException(status_code=400, detail="Document is empty")

    print("--- Extracted Text (first 200 chars) ---")
    print(document_text[:200])
    print("--- Extracted Rules ---")
    print(rules)

    try:
        
        violations = analyze_rules(document_text, rules)
    except Exception as e:
        print(f"AI analysis failed: {e}")
        raise HTTPException(status_code=502, detail=f"AI analysis failed: {str(e)}")

    print("--- Violations ---")
    print(violations)

    return {"violations": violations}
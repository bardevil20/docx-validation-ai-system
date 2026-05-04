import docx
from typing import BinaryIO

def extract_text_from_docx(file_stream: BinaryIO) -> str:
    """
    Extracts text from a DOCX file stream.
    Skips empty paragraphs to keep the text clean for the LLM.
    """
    doc = docx.Document(file_stream)
    full_text = []
    
    for para in doc.paragraphs:
        cleaned_text = para.text.strip()
        if cleaned_text:
            full_text.append(cleaned_text)
            
    return "\n".join(full_text)
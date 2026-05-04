# docx-validation-ai-system

# Document Rule Checker API

## Overview
This is a backend-focused web application designed to analyze `.docx` documents against a set of user-defined compliance rules. 

It uses **FastAPI** for the core routing and API management, **PostgreSQL** for storing analysis history and rule violations, and Google's **Gemini AI** (via Structured Outputs) to semantically evaluate the document text and extract exact quotes when a violation is found.

## Features
* **File Parsing:** Extracts clean text from `.docx` files using `python-docx` without relying on AI for binary file reading.
* **AI Integration:** Uses `gemini-2.5-flash` with strict temperature (0.0) and Pydantic schemas to ensure deterministic, structured JSON responses.
* **Persistent Storage:** Saves job history and identified violations in a PostgreSQL database using `SQLAlchemy`.
* **Simple UI:** A vanilla JavaScript and HTML frontend for easy testing.

## Project Structure
```text
├── app/
│   ├── main.py             # FastAPI application instance and table creation
│   ├── database.py         # SQLAlchemy engine and DB session setup
│   ├── models/             # DB Schemas (Analysis and Rules)
│   ├── routers/            # API endpoints (e.g., analyze.py)
│   ├── ai_service.py       # Gemini API integration and prompting logic
│   └── utils.py            # Helper functions (e.g., DOCX text extraction)
├── static/
│   └── index.html          # Simple Vanilla JS frontend
├── docker-compose.yml      # PostgreSQL container setup
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (Not committed)

## Prerequisites
* Python 3.10+
* Docker & Docker Compose (for the database)
* A valid Google Gemini API Key

## Setup and Installation
1. Clone the repository and set up a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\\Scripts\\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Environment Variables:
Create a .env file in the root directory and add the following:

```
DATABASE_URL=postgresql://user:password@localhost:5432/doc_checker
GEMINI_API_KEY=your_google_api_key_here
```

5. Run the Server:
The application will automatically create the required database tables on startup.

```
uvicorn app.main:app --reload
```

## How to Use and Test
###Through the UI:

Open your browser and go to http://localhost:8000/checkfile.

Upload a .docx file.

Enter your rules (e.g., "Find any numerical description that reveals operational performance").

Click "Run Analysis" and view the extracted violations and quotes.


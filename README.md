# Patient Summary Assistant - Track 1

From code to care: this project implements **Track 1 - Patient Summary Assistant**
from HackWithChicago 2.0.

It builds a live Pathway powered backend that ingests patient records in streaming
mode and generates specialist specific summaries with citations back to the source
records.

## What it does

- Ingests patient documents (labs, notes, imaging reports) as a live or simulated stream
- Maintains a Pathway table and hybrid index of all records by patient
- Generates a 1-2 page specialist focused summary through an LLM
- Returns traceable citations for every bullet in the summary
- Demonstrates real time behavior when new records arrive

## Why it matters

Doctors and patients lose time reconstructing history from scattered PDFs and portals.
A structured, specialist targeted summary lets the visit focus on decision making instead
of paperwork, while still respecting privacy and traceability.

This prototype is decision support only and does not make diagnoses.

## Tech stack

- **Pathway** for streaming ingestion, live tables, and indexing
- **Pathway LLM xPack** as the orchestration layer for RAG style summaries
- **FastAPI** for the HTTP API
- **PaddleOCR** hook ready for scanned documents
- Python 3.11

## Repository layout

- `backend/app/main.py` - FastAPI application
- `backend/app/schemas.py` - Pydantic models
- `backend/app/pipeline.py` - in memory summary logic plus Pathway bridge
- `backend/app/pathway_pipeline.py` - Pathway streaming pipeline and connectors
- `docs/architecture.md` - Mermaid architecture diagram for the judges
- `requirements.txt`, `Dockerfile`, `docker-compose.yml` - environment and deployment

## Running locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start the API
uvicorn backend.app.main:app --reload --port 8000
```

Then open `http://localhost:8000/docs` for interactive docs.

## Simulated live data

Place newline separated JSON files under `data/stream/patient_summary/` with fields:

```json
{"patient_id": "p1", "doc_type": "lab", "content": "HbA1c 8.1 percent", "source": "lab_2025_01_01.pdf"}
```

Pathway will watch this folder in streaming mode. During the demo, add a new file and
regenerate the summary to show it update.

## Demo flow

1. Upload or stream a few patient documents using the `/patients/{id}/documents` endpoint.
2. Call `/summaries` with `patient_id` and `specialist`.
3. Show the structured summary and its citations.
4. Append a new document in `data/stream/patient_summary`.
5. Regenerate the summary and point out the new lab or note included.

## Safety and privacy

- Example data only, no real PHI is used.
- This tool is for education and workflow support, not for diagnosis or treatment.
- In a production setting you would integrate Aparavi for PHI redaction and data policy.

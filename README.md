# BugFlow Tracker

**Live Demo:** [https://bugflow-tracker.onrender.com](https://bugflow-tracker.onrender.com)

BugFlow is a lean, AI-powered bug tracking system designed for speed and clarity. It helps teams report issues and leverages LLMs to automatically triage them by category and severity.

## Features
- **Modern UI**: A clean, Linear-inspired dashboard built with React and Tailwind CSS.
- **AI Triage**: Automatically suggests bug category (UI, Backend, Performance) and severity (Low, Medium, High) using Google Gemini.
- **State Enforcement**: Strict workflow transitions (OPEN → IN_PROGRESS → RESOLVED → CLOSED).
- **Mandatory Documentation**: Requires resolution notes before a bug can be closed.

## Tech Stack
- **Frontend**: React 19 (Vite), Tailwind CSS 4
- **Backend**: Python (Flask)
- **Database**: SQLite (SQLAlchemy)
- **AI**: Google Gemini Pro API
- **Production**: Gunicorn (Web Server)

## Key Decisions
- **Unified Service**: To simplify deployment and reduce complexity, the Flask backend serves the compiled React production build.
- **Absolute Paths**: Used for SQLite database location to ensure data persistence across different deployment environments.
- **Smart Fallback**: Implemented a keyword-based triage layer that takes over if the AI model is unavailable or returns invalid data.
- **Pragmatic Architecture**: Avoided over-engineering by keeping logic concentrated in a few well-defined files (`app.py`, `services.py`, `models.py`).

## Safe AI Usage
- **Temperature Control**: Set to `0.2` to ensure deterministic and predictable triaging results.
- **Validation Layer**: All AI outputs are validated against strictly defined schemas before being saved.
- **Privacy**: Only the bug title and description are sent to the LLM; no user or system metadata is exposed.

## Known Limitations
- **File System**: Uses a local SQLite file. For high-availability production, an external database (PostgreSQL) would be recommended.
- **Authentication**: Intentionally omitted to maintain the "lean" philosophy of the initial assessment project.

## Local Development
1. **Backend**: 
   - `pip install -r backend/requirements.txt`
   - `flask run` (ensure `GEMINI_API_KEY` is in `backend/.env`)
2. **Frontend**:
   - `cd frontend && npm install && npm run dev`

## Evaluation Criteria (How this system meets them)

- **Structure**: Clear separation between UI (React) and Logic (Flask). Backend logic is logically grouped by concern (`models`, `schemas`, `services`).
- **Simplicity**: Avoided complex state management or heavy middleware. Standard REST patterns make the code predictable.
- **Correctness**: The `BugService` strictly enforces business rules, preventing invalid status transitions and ensuring closure requirements are met.
- **Interface Safety**: **Pydantic** models guard every entry point, ensuring types are correct before they touch the database.
- **Verification**: Automated tests in `backend/tests/test_bugs.py` prove that core rules (like status flow) remain intact.
- **Observability**: Added debug logging for AI triaging and comprehensive error handling for malformed JSON responses.
- **AI Usage**: Gemini Pro is used strategically for data enrichment (triage), with a robust validation layer and a deterministic fallback heuristic.



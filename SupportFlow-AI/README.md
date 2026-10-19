# SupportFlow AI — Support Ticket Automation

SupportFlow AI is a small, explainable support-ticket automation API built with FastAPI, SQLAlchemy, and SQLite. It categorizes incoming tickets, assigns a team, suggests a priority, drafts a response, and keeps tickets in a review state until a person approves them.

> **Demo / assessment project:** the classifier is a transparent keyword baseline, not a trained AI model. The approval endpoint is not authenticated. Do not expose this implementation publicly as a production support system without adding authentication, authorization, audit logging, and a production database.

## Features
- Create and store support tickets.
- Explainable keyword-based category classification: Billing, Technical, Access, General.
- Rule-based priority suggestion: Critical, High, Medium, Low.
- Team assignment and draft-response generation.
- Ambiguous messages are flagged for human review.
- Human approval endpoint before status becomes `READY`.
- List and retrieve tickets.
- Input validation and duplicate-ID handling.
- Automated tests and GitHub Actions CI.
- Docker support and a manually triggered Azure deployment workflow template.

## Requirements
- Python 3.12
- Git (only needed to clone/push the repository)
- Docker Desktop (optional)

## Run locally — Windows PowerShell

Clone the repository or open the downloaded project directory, then run these commands from the project root:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

If PowerShell blocks virtual-environment activation, run this in the same terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run locally — macOS/Linux

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Example request

Use `POST /tickets` in Swagger UI with:

```json
{
  "ticket_id": "TKT-1001",
  "message": "I was charged twice for my monthly subscription."
}
```

Expected key fields include `category: "Billing"`, `priority: "High"`, and `assigned_team: "Billing Team"`. The ticket is not marked `READY` until approved.

To approve it, call `POST /tickets/TKT-1001/approve`. This demo endpoint has no authentication and is intended only for local demonstration.

Other endpoints:
- `GET /tickets` — list tickets
- `GET /tickets/{ticket_id}` — retrieve one ticket
- `POST /tickets/{ticket_id}/approve` — approve a draft

## Tests and evaluation

Run automated tests:

```bash
python -m pytest -v
```

Run the small held-out sample evaluation:

```bash
python -m app.evaluate
```

The sample file has 30 fictional labeled records: the first 20 are marked `train` (for rule/policy development) and the last 10 are marked `test`. Do not tune rules using the test records if reporting an honest holdout score. The test set is small and synthetic, so its score is not evidence of production performance. Report the actual output from the evaluation command rather than claiming an assumed accuracy.

## Docker

Build and run (Docker Desktop must be installed and running):

```bash
docker build -t supportflow-ai .
docker run --rm -p 8000:8000 supportflow-ai
```

The container uses a local SQLite database. For production deployments, configure a managed persistent database.

## GitHub

Create an empty repository on GitHub, then from the project root:

```bash
git init
git add .
git commit -m "Build SupportFlow AI ticket automation API"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your actual repository URL. Do not commit passwords, tokens, `.env` files, virtual environments, or local database files.

GitHub Actions runs the tests on pushes and pull requests. The Azure workflow is manually triggered and requires Azure resources, OIDC configuration, and repository secrets/variables; see `docs/azure-plan.md`.

## Project structure

```text
SupportFlow-AI/
├── app/
│   ├── __init__.py
│   ├── classifier.py
│   ├── database.py
│   ├── evaluate.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── services.py
├── docs/
│   ├── azure-plan.md
│   └── priority-policy.md
├── sample_data/
│   ├── expected_results.json
│   └── tickets.json
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_approval.py
│   ├── test_classifier.py
│   └── test_tickets.py
├── .github/workflows/
│   ├── ci.yml
│   └── deploy.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
└── requirements.txt
```

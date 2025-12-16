# FastAPI Feature Assignment (Calculator + Profile + Reports)

This project includes:
- FastAPI backend + SQLAlchemy + Alembic
- User auth (register/login) + profile update + change password
- Calculator API + calculation history
- Reports endpoint (stats like total calculations, average operands)
- Front-end pages (basic HTML)
- Tests: unit + integration (pytest) + E2E (Playwright)
- Docker + GitHub Actions workflow

## 1) Run locally (Python)

**Terminal 1 (backend):**
```powershell
cd "<YOUR_PROJECT_FOLDER>"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Apply DB migrations (SQLite local by default)
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000/ (home)
- http://127.0.0.1:8000/register
- http://127.0.0.1:8000/calculator
- http://127.0.0.1:8000/reports

## 2) Run tests (unit + integration)

**In the same project folder:**
```powershell
.\.venv\Scripts\activate
python -m pytest
```

> If you ever see coverage warnings like “Module calculator was never imported”, you likely have `PYTEST_ADDOPTS` set from an old project.
> Fix it with:
```powershell
Remove-Item Env:PYTEST_ADDOPTS -ErrorAction SilentlyContinue
```

## 3) Run E2E tests (Playwright)

**Make sure the backend is running on http://127.0.0.1:8000 first (Terminal 1).**

**Terminal 2 (E2E):**
```powershell
cd "<YOUR_PROJECT_FOLDER>\e2e"
npm install
npx playwright install
npx playwright test
```

✅ IMPORTANT: `package.json` is inside the `e2e` folder, so you must run `npm install` from `e2e`.

### Cleaning node_modules (PowerShell)
```powershell
cd "<YOUR_PROJECT_FOLDER>\e2e"
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item -Force package-lock.json -ErrorAction SilentlyContinue
npm install
```

## 4) Run with Docker (Postgres)

```powershell
cd "<YOUR_PROJECT_FOLDER>"
docker compose up --build
```

- App: http://127.0.0.1:8000
- Postgres is mapped to host port **5437** (change it in `docker-compose.yml` if you get “port is already allocated”)


# AI PDF Chatbot

A gradually built, production-minded PDF question-answering application using a React 19 + Vite frontend and a FastAPI backend.

The durable product and implementation context lives in [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md). Update that document whenever the product scope or architecture changes so the original PDF is not needed again.

## Current structure

```text
pdf-chatbot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── tests/
│   │   └── test_health.py
│   └── pyproject.toml
├── docs/
│   └── PROJECT_CONTEXT.md
├── frontend/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── main.tsx
│   │   └── vite-env.d.ts
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── .env.example
└── .gitignore
```

## Run locally

Backend (PowerShell):

```powershell
Copy-Item .env.example .env
# Edit .env if your local PostgreSQL values differ.
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
fastapi dev app/main.py --host 127.0.0.1 --port 8001
```

Frontend (a second terminal):

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5174`. The API health endpoint is `http://127.0.0.1:8001/api/health`.

## Current document API

- `POST /api/documents` accepts one PDF in the multipart field named `file`.
- `GET /api/documents` lists every uploaded document.
- Files are stored under the ignored `backend/data/uploads/` directory.
- Document metadata is stored in PostgreSQL. The database and `documents` table are created manually for now.

Use `http://127.0.0.1:8001/docs` to upload and inspect documents without a frontend form.

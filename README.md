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

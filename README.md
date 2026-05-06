# 💰 WealthMind AI — Personalized Investment Advisor


**An end-to-end AI-powered financial advisory platform** — combining LangGraph agent orchestration, a trained ML risk model, RAG knowledge retrieval, and live market data into one automated investment pipeline.

--- 

## 🧠 What Is WealthMind AI?

WealthMind AI is a full-stack AI investment advisor that takes a user's financial profile — age, income, savings, risk tolerance, goals — and runs it through an **8-step LangGraph agent pipeline** to produce a fully personalized investment strategy, complete with:

- Asset allocation breakdown (Stocks, ETFs, Bonds, Crypto, Cash)
- ML-predicted risk score (0–100)
- Compound growth simulation with monthly contributions
- Plain-English or investor-level explanation (your choice)
- Live market context (S&P 500, Nasdaq, BTC, ETH)
- RAG-backed investment wisdom from a ChromaDB knowledge base

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **LangGraph Pipeline** | 8 chained AI agents — profile → RAG → market → strategy → risk → simulate → advisor → memory |
| 🧮 **ML Risk Engine** | Decision Tree model (scikit-learn) blended with rule-based scoring for risk prediction |
| 📚 **RAG Knowledge Base** | ChromaDB vector store with investment research — answers backed by real knowledge, not hallucinations |
| 📈 **Growth Simulation** | Compound interest + monthly contribution projection, year by year |
| 💬 **Conversational Memory** | In-session chat with strategy context so the AI remembers your profile |
| 📊 **Live Market Data** | yfinance + CoinGecko for real-time S&P 500, Nasdaq, Gold, BTC, ETH prices |
| 🔐 **JWT Authentication** | Argon2 password hashing, secure JWT tokens, protected routes |
| 🐳 **Fully Containerized** | Docker Compose — backend, frontend, PostgreSQL, Nginx in one command |
| ⚙️ **CI/CD Pipeline** | Jenkins → Docker Hub → AWS EC2 automated deploy with GitHub webhook |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                         │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP :80
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Nginx Reverse Proxy                      │
│        /           →   React Frontend (port 80)             │
│        /api/       →   FastAPI Backend (port 8000)          │
└──────────┬──────────────────────────┬───────────────────────┘
           │                          │
           ▼                          ▼
┌──────────────────┐      ┌───────────────────────┐
│  React Frontend  │      │    FastAPI Backend     │
│  - Home Page     │      │  - /auth  (register,   │
│  - Login/Register│      │           login)       │
│  - Chat/Advisor  │      │  - /users (JWT verify) │
│  - AuthContext   │      │  - /ai    (analyze)    │
└──────────────────┘      └───────────┬───────────┘
                                      │
                          ┌───────────▼───────────┐
                          │   LangGraph Pipeline  │
                          │   (8 Agent Nodes)     │
                          └───────────┬───────────┘
                                      │
           ┌──────────────────────────┼──────────────────────┐
           ▼                          ▼                       ▼
┌──────────────────┐     ┌────────────────────┐  ┌───────────────────┐
│   PostgreSQL DB  │     │  ChromaDB (RAG)    │  │  OpenRouter LLM   │
│   User accounts  │     │  Investment KB     │  │  (gpt-4o-mini)    │
└──────────────────┘     └────────────────────┘  └───────────────────┘
```

---

## 🔄 AI Pipeline

The heart of WealthMind is a **LangGraph StateGraph** — each step passes enriched state to the next:

```
[1] Profile Agent      → Classifies investor type via LLM
        ↓
[2] RAG Retrieval      → Fetches relevant investment knowledge from ChromaDB
        ↓
[3] Market Data        → Fetches live prices (yfinance + CoinGecko)
        ↓
[4] Strategy Agent     → Generates asset allocation JSON via LLM
        ↓
[5] Risk Engine        → Blends rule-based + Decision Tree ML score (0–100)
        ↓
[6] Simulation Engine  → Compound growth projection, year by year
        ↓
[7] Advisor Agent      → Generates plain-English or investor explanation
        ↓
[8] Memory Store       → Saves strategy context for follow-up chat
```

Each node has graceful fallbacks — if any agent fails, the pipeline continues with safe defaults.

---

## 🤖 ML Risk Model

The risk scoring engine blends two approaches (50/50 average):

**Rule-Based Engine** — scores based on allocation weights, age, time horizon, and stated risk tolerance.

**Decision Tree Regressor** — trained on synthetic portfolio data:

```
Features:  age, time_horizon, risk_tolerance, stocks%, etfs%, bonds%, crypto%, cash%
Target:    risk_score (0–100)
Model:     DecisionTreeRegressor (max_depth=8, min_samples_leaf=10)
```

- Preprocessing: LabelEncoder for categoricals, StandardScaler for numerics
- Artifacts saved: `risk_model.pkl`, `scaler.pkl`, `label_encoder.pkl`
- Fallback: if model files not found, rule-based engine takes over automatically

---

## 📂 Project Structure

```
WealthMind-AI/
├── backend/
│   ├── main.py                        # FastAPI app entry point
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env                           # secrets (not committed)
│   └── app/
│       ├── api/
│       │   ├── auth.py                # register / login endpoints
│       │   ├── users.py               # JWT validation, /me endpoint
│       │   └── ai_model.py            # /ai/analyze protected endpoint
│       ├── core/
│       │   ├── config.py              # env var loading
│       │   └── security.py            # Argon2 hashing, JWT creation
│       ├── db/
│       │   ├── database.py            # SQLAlchemy engine + session
│       │   ├── models.py              # User model
│       │   └── schemas.py             # Pydantic schemas
│       └── ai_module/app/
│           ├── graph.py               # LangGraph pipeline (main brain)
│           ├── schemas.py             # AI data models
│           ├── agents/
│           │   ├── profile_agent.py   # investor classification
│           │   ├── strategy_agent.py  # allocation generation
│           │   └── advisor_agent.py   # explanation + chat
│           ├── engines/
│           │   ├── risk_engine.py     # ML + rule-based risk scoring
│           │   ├── market_engine.py   # live market data
│           │   └── simulation_engine.py # compound growth
│           ├── rag/
│           │   ├── rag_store.py       # ChromaDB vector store
│           │   └── ingest.py          # knowledge base population
│           ├── memory/
│           │   └── memory_store.py    # in-session chat memory
│           └── ml_model/
│               ├── train_model.py     # training script
│               ├── predict.py         # prediction helper
│               └── risk_model.pkl     # trained model artifact
├── frontend/
│   ├── Dockerfile
│   └── src/
│       ├── App.jsx
│       ├── api/axios.js               # Axios + JWT interceptor
│       ├── context/
│       │   ├── AuthContext.jsx        # global auth state
│       │   └── ProtectedRoute.jsx     # route guard
│       └── pages/
│           ├── Home.jsx               # landing page
│           ├── Login.jsx
│           ├── Register.jsx
│           └── Chat.jsx               # main advisor UI
├── nginx/
│   └── nginx.conf                     # reverse proxy config
├── docker-compose.yml
└── Jenkinsfile                        # CI/CD pipeline
```

---

## 🚀 Setup

### Prerequisites

- Docker + Docker Compose
- (Optional) Python 3.10+ for local development

### 1. Clone the Repository

```bash
git clone https://github.com/stack-ai-dev/WealthMind_AI.git
cd WealthMind_AI
```

### 2. Configure Environment Variables

Create `backend/.env`:

```env
OPENAI_API_KEY=your_openrouter_api_key
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/postgres
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CHROMA_PATH=app/ai_module/chroma_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=postgres
```

> 💡 This project uses [OpenRouter](https://openrouter.ai) as the LLM provider — compatible with the OpenAI SDK, supports gpt-4o-mini.

### 3. Populate the RAG Knowledge Base

```bash
# Inside the backend container or locally
python -m app.ai_module.app.rag.ingest
```

### 4. Train the ML Risk Model

```bash
python -m app.ai_module.app.ml_model.train_model
```

### 5. Start Everything

```bash
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost/api |
| API Docs (Swagger) | http://localhost:8000/docs |
| PostgreSQL | localhost:1457 |

---

## ⚙️ CI/CD Pipeline

Fully automated pipeline using **Jenkins + Docker Hub + AWS EC2**:

```
GitHub Push (main branch)
        ↓  (webhook trigger)
Jenkins Pipeline
        ├── Clone Repository
        ├── Create .env from Jenkins Credentials Store
        ├── Build Docker Images (backend + frontend)
        ├── Tag with BUILD_NUMBER + latest
        ├── Push to Docker Hub
        └── SSH into EC2 → docker-compose pull + up -d
```

**Secrets Management:** All sensitive values (API keys, DB passwords, SSH key) are stored in Jenkins Credentials — never in source code.

**Images Published:**
- `itsnotdocker/wealthmind-backend`
- `itsnotdocker/wealthmind-frontend`

---

## 📡 API Reference

### Auth

```
POST /auth/register     { email, password }    → Register new user
POST /auth/login        { email, password }    → Returns JWT token
```

### Users

```
GET  /users/me          Authorization: Bearer <token>   → Current user info
```

### AI (Protected)

```
POST /ai/analyze        Authorization: Bearer <token>
Body:
{
  "profile": {
    "name": "string",
    "age": 28,
    "income": 60000,
    "savings": 15000,
    "risk_tolerance": "medium",
    "goal": "retirement",
    "time_horizon": 20
  },
  "session_id": "default",
  "monthly_contribution": 500,
  "explain_mode": "beginner"
}

Response: FullAdvice
{
  "strategy": {
    "profile_type": "Moderate Growth Investor",
    "risk_score": 58.5,
    "risk_label": "Medium",
    "allocation": { "stocks": 45, "etfs": 25, "bonds": 15, "crypto": 5, "cash": 10 },
    "expected_annual_return": 8.5,
    "confidence_score": 82,
    "recommendations": [...],
    "risks": [...],
    "explanation": "..."
  },
  "simulation": {
    "years": [0,1,2,...,20],
    "portfolio_values": [...],
    "final_value": 98450.00,
    "total_invested": 57000.00,
    "total_gain": 41450.00,
    "goal_progress_percent": 68.2
  },
  "rag_insight": "...",
  "market_summary": "S&P 500: 5420 (+0.5%) | Bitcoin: $67,000 (+2.1%)"
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18, React Router, Axios |
| **Backend** | FastAPI, Uvicorn, SQLAlchemy |
| **AI Orchestration** | LangGraph, LangChain |
| **LLM** | OpenRouter (gpt-4o-mini) |
| **ML Model** | scikit-learn (Decision Tree Regressor) |
| **Vector DB** | ChromaDB |
| **Market Data** | yfinance, CoinGecko API |
| **Auth** | JWT (python-jose), Argon2 (passlib) |
| **Database** | PostgreSQL 15 |
| **Containerization** | Docker, Docker Compose |
| **Reverse Proxy** | Nginx |
| **CI/CD** | Jenkins, Docker Hub, AWS EC2 |
| **Version Control** | GitHub (webhook → Jenkins) |

---

## 📄 License

MIT License — feel free to use, modify, and build on this project.

---


Built with using FastAPI · LangGraph · React · Docker · Jenkins · AWS

# ⚡ AdaptPrep AI — Adaptive DSA Practice & AI Code Review Platform

**AdaptPrep AI** is a full-stack web application designed for placement interview preparation. It features an adaptive Data Structures & Algorithms (DSA) scoring engine, sandboxed code execution for **Python** and **C++**, and structured **LangChain AI code reviews**.

---

## 🚀 Tech Stack

- **Frontend**: React 18, Monaco Editor (`@monaco-editor/react`), Recharts (Analytics Dashboard), Lucide Icons, Tailwind CSS.
- **Backend**: Python 3.11, FastAPI, SQLAlchemy ORM, Pydantic v2, Passlib (bcrypt), PyJWT.
- **Database**: PostgreSQL (Dockerized) with SQLite fallback for zero-config local development.
- **AI Layer**: LangChain with `ChatOpenAI` (configurable to local Ollama / LM Studio or deterministic fallback reviewer).
- **Code Execution Sandbox**: Subprocess execution with 5-second timeouts, stdout/stderr capture, and isolated temp file management supporting Python 3 and C++ (g++).

---

## 📁 Project Architecture

```
adaptprep-ai/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI entrypoint, CORS, router mounts, DB startup seeder
│   │   ├── database.py           # SQLAlchemy engine & session management
│   │   ├── models.py             # User, Question, TopicScore, Submission ORM models
│   │   ├── schemas.py            # Pydantic schemas for Auth, Submissions, AI Feedback, Analytics
│   │   ├── auth.py               # Password hashing (bcrypt) & JWT token handling
│   │   ├── sandbox.py            # Isolated execution module for Python 3 & C++ (g++)
│   │   ├── adaptive.py           # EMA scoring engine (alpha=0.3) & /next-question algorithm
│   │   ├── ai_review.py          # LangChain structured chain with few-shot prompts
│   │   ├── seed_data.py          # 20 curated DSA questions across 5 core topics
│   │   └── routers/
│   │       ├── auth_router.py        # /api/auth/signup, /api/auth/login, /api/auth/me
│   │       ├── questions_router.py   # /api/questions, /api/questions/{id}, /api/questions/next-question
│   │       ├── submissions_router.py # /api/submissions/submit, /api/submissions/history
│   │       └── analytics_router.py   # /api/analytics/scores, /api/analytics/dashboard
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx          # Brand logo, adaptive next trigger, user controls
│   │   │   ├── CodeEditor.jsx      # Monaco Editor wrapper with language switcher
│   │   │   ├── TestResults.jsx     # Test case pass/fail list, execution timing & diffs
│   │   │   ├── AIFeedback.jsx      # LangChain structured review (bugs, complexities, tips)
│   │   │   ├── ScoreRadarChart.jsx # Recharts Radar & Bar visual mastery analytics
│   │   │   └── ProtectedRoute.jsx  # Auth route guard
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx       # Auth login + instant placement demo button
│   │   │   ├── SignupPage.jsx      # Registration page
│   │   │   ├── PracticePage.jsx    # Split-screen problem view, editor, results, AI feedback
│   │   │   ├── DashboardPage.jsx   # Radar chart, mastery breakdown, submission history
│   │   │   └── QuestionListPage.jsx# Question bank with topic & difficulty filters
│   │   ├── context/AuthContext.jsx # User state & token management
│   │   └── services/api.js         # Axios HTTP client with JWT interceptor
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🧮 How the Adaptive Scoring Engine Works

User performance across 5 core DSA topics (**Arrays, Strings, Dynamic Programming, Graphs, Trees**) is tracked dynamically using an **Exponential Moving Average (EMA)** algorithm.

### 1. EMA Update Formula
$$Score_{new} = Score_{old} + \alpha \times (Result - Score_{old})$$

- $\alpha = 0.3$ (Smoothing factor weighting recent submissions while maintaining score stability).
- $Result$ Values:
  - **`1.0`**: All test cases passed with optimal runtime ($\le 200\text{ ms}$).
  - **`0.8`**: All test cases passed with slightly elevated runtime.
  - **`0.4`**: Partial pass ($\ge 50\%$ test cases passed).
  - **`0.0`**: Submission failed or encountered a compilation/runtime error.

### 2. Next Question Recommendation (`/api/questions/next-question`)
1. Finds the topic where the user currently holds the **minimum score** in `topic_scores`.
2. Maps current score to target difficulty:
   - $\text{Score} < 0.4 \rightarrow \mathbf{Easy}$
   - $0.4 \le \text{Score} < 0.7 \rightarrow \mathbf{Medium}$
   - $\text{Score} \ge 0.7 \rightarrow \mathbf{Hard}$
3. Recommends an unsolved question in that topic matching the target difficulty.

---

## 🤖 LangChain AI Code Review Architecture

Every code submission triggers a LangChain chain (`ai_review.py`) that returns structured JSON feedback:

```json
{
  "bugs": ["Edge case issue: array out of bounds when N=0"],
  "time_complexity": "O(N log N)",
  "space_complexity": "O(1)",
  "optimization_tips": [
    "Use a Hash Map to store complement values for O(N) linear time complexity."
  ],
  "corrected_snippet": "def twoSum(nums, target): ..."
}
```

### Prompt Engineering & Few-Shot Learning
The prompt utilizes **1-2 few-shot examples** demonstrating ideal JSON output formatting for both Python and C++ solutions.

### Swapping Model Providers
To switch model providers (e.g., to run locally with **Ollama** or **LM Studio**):
Set the environment variables in your `.env` or Docker config:
```bash
LLM_MODEL="llama3"
LLM_BASE_URL="http://localhost:11434/v1"
```

If no `OPENAI_API_KEY` is supplied, the app automatically falls back to an offline rule-based code reviewer.

---

## 🛡️ Code Execution Sandbox & Security Notes

- **Python**: Subprocess execution with strict 5-second time limit, stdout capture, and isolated memory footprint.
- **C++**: Source code is written to a temporary directory (`tempfile.TemporaryDirectory()`), compiled via `g++ -O2`, executed with stdin inputs, and immediately cleaned up.

> ⚠️ **Production Security Note**:
> For this portfolio demo, execution uses isolated local subprocesses with strict timeout bounds. A production-grade implementation (e.g., LeetCode/Codeforces style) would run untrusted code inside isolated **Docker containers** (Docker-in-Docker) or utilize dedicated sandbox isolation tools like **Judge0** / **gVisor** / **AWS Lambda** to restrict syscalls, memory limits, and network access.

---

## 🛠️ How to Run Locally

### Option A: Quick Start via Docker Compose (Recommended)

```bash
# 1. Clone or navigate to the project directory
cd adaptprep-ai

# 2. Build and spin up containers (Postgres + FastAPI + React)
docker-compose up --build
```

Access the Web Application at: **`http://localhost:5173`**
Backend Swagger API Docs: **`http://localhost:8000/docs`**

---

### Option B: Manual Local Setup (Without Docker)

#### 1. Backend Setup (FastAPI)

```bash
cd adaptprep-ai/backend

# Create virtual environment
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server (SQLite database will be auto-created & seeded with 20 questions)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup (React + Vite)

```bash
cd adaptprep-ai/frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```

App will run at: **`http://localhost:5173`**

---

## 🎯 Candidate Portfolio Demo Guide

1. Click **"Instant Placement Demo Login"** on the login page to log in as a test candidate.
2. View your initial **Skill Mastery Radar Chart** on the Dashboard across all 5 DSA topics.
3. Click **"Adaptive Next"** in the top navigation bar to let the algorithm analyze your lowest-scoring topic and present a targeted question.
4. Write code in **Python 3** or **C++** in the Monaco Editor and click **Submit Solution**.
5. Inspect the pass/fail breakdown, runtime, and the **LangChain AI Code Review** (bugs list, time/space complexity, optimization tips, corrected code).
6. Return to the **Dashboard** to see your EMA mastery score update live on the Recharts Radar and Bar charts!

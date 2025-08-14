# Choose Your Adventure - AI Story Generator

This project is a full-stack web application that allows users to generate and play through unique "Choose Your Own Adventure" style stories. Users provide a theme, and the backend leverages the Anthropic Claude LLM via LangChain to create complete, branching narratives served through an interactive React frontend.

## 📁 Project Structure

```
Choose-Your-Adventure/
├── backend/                 # FastAPI backend
│   ├── core/               # Core configuration and utilities
│   ├── db/                 # Database models and connection
│   ├── models/             # SQLAlchemy models
│   ├── routers/            # API route handlers
│   ├── main.py             # FastAPI application entry point
│   ├── pyproject.toml      # uv/Python project configuration
│   ├── requirements.txt    # Python dependencies
│   └── vercel.json         # Vercel deployment config
├── frontend/               # React frontend
│   ├── public/             # Static assets
│   ├── src/                # React source code
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node.js dependencies
│   ├── vite.config.js      # Vite configuration
│   └── vercel.json         # Vercel deployment config
└── README.md               
```

## ✨ Features

- **🤖 Dynamic Story Generation**: Creates unique stories based on any user-provided theme
- **⚡ Asynchronous Processing**: Story generation handled in background with job polling
- **🎮 Interactive Gameplay**: Navigate stories by making choices that affect the narrative
- **🌳 Branching Narratives**: Multiple paths with winning and losing endings
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🔄 Real-time Updates**: Live status updates during story generation
- **☁️ Cloud Deployment**: Fully deployed on Vercel with PostgreSQL database

## 🛠️ Tech Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- **Package Manager**: [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- **LLM Integration**: [LangChain](https://python.langchain.com/) - LLM orchestration framework
- **AI Model**: [Anthropic Claude 3 Haiku](https://www.anthropic.com/claude) - Fast, intelligent AI model
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- **Database**: PostgreSQL (production), SQLite (development)
- **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation using Python type hints
- **ASGI Adapter**: [Uvicorn](https://www.uvicorn.org/) - Lightning-fast ASGI server
- **Deployment**: [Vercel](https://vercel.com/) - Serverless functions

### Frontend
- **Framework**: [React 18](https://react.dev/) - Modern React with hooks
- **Build Tool**: [Vite](https://vitejs.dev/) - Next generation frontend tooling
- **Routing**: [React Router](https://reactrouter.com/) - Declarative routing for React
- **HTTP Client**: [Axios](https://axios-http.com/) - Promise-based HTTP client
- **Styling**: CSS with CSS Variables
- **Package Manager**: npm
- **Deployment**: [Vercel](https://vercel.com/) - Static site hosting

## 🏗️ Architecture

```
graph TD
    A[React Frontend] -->|POST /api/stories/create| B[FastAPI Backend]
    B -->|Creates job| C[PostgreSQL Database]
    B -->|Background task| D[Anthropic Claude API]
    D -->|Generated story| B
    A -->|Polls status| E[GET /api/jobs/{job_id}]
    E -->|Job complete| A
    A -->|Fetch story| F[GET /api/stories/{story_id}/complete]
    F -->|Story data| A
```

1. **React Frontend** prompts user for a story theme
2. **FastAPI Backend** receives request at `POST /api/stories/create`
3. Backend creates a `StoryJob` record and starts background task
4. Background task calls **Anthropic Claude LLM** via **LangChain**
5. LLM response parsed and saved as `Story` with multiple `StoryNode` entries
6. Frontend polls `GET /api/jobs/{job_id}` for generation status
7. On completion, frontend fetches full story from `GET /api/stories/{story_id}/complete`
8. User navigates through story by making choices

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** with [uv](https://github.com/astral-sh/uv) installed
- **Node.js 18+** and npm
- **Anthropic API Key** ([Get one here](https://console.anthropic.com/dashboard))

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies with uv:**
   ```bash
   uv sync
   ```

3. **Activate virtual environment:**
   ```bash
   uv venv
   ```

4. **Create environment file:**
   ```bash
   # backend/.env
   ANTHROPIC_API_KEY="sk-ant-your-api-key-here"
   API_PREFIX=/api
   DATABASE_URL="sqlite:///./database.db"
   ALLOWED_ORIGINS="http://localhost:5173"
   DEBUG=true
   ```

4. **Start backend service:**
    ```bash
    uv run main.py
    ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```
   
3. **Start development server:**
   ```bash
   npm run dev
   ```

## 📚 API Documentation

Once the backend is running, visit:
- **Local**: http://localhost:8000/docs

### Key Endpoints
- `POST /api/stories/create` - Create a new story generation job
- `GET /api/jobs/{job_id}` - Check job status
- `GET /api/stories/{story_id}/complete` - Retrieve complete story data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

***

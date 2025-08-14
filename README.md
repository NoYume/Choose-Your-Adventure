# Choose Your Adventure - AI Story Generator

This project is a full-stack web application that allows users to generate and play through unique "Choose Your Own Adventure" style stories. A user provides a theme, and the backend leverages the Anthropic Claude LLM via Langchain to create a complete, branching narrative which is then served to the user through an interactive React frontend.

## Features

- **Dynamic Story Generation**: Creates unique stories based on any user-provided theme.
- **Asynchronous Job Processing**: Story generation is handled in the background, allowing the UI to remain responsive.
- **Interactive Gameplay**: Users navigate the story by making choices that lead to different paths.
- **Branching Narratives**: Stories include multiple paths, with at least one winning and several losing endings.
- **Full-Stack Application**: Complete with a React frontend and a FastAPI backend.
- **Vercel Deployment**: Seamlessly deployed on Vercel for both frontend and backend services.

## Tech Stack

### Backend

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **LLM Integration**: [LangChain](https://python.langchain.com/)
- **AI Model**: [Anthropic Claude 3 Haiku](https://www.anthropic.com/claude)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: SQLite (for development), PostgreSQL (for production)
- **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)
- **Deployment**: [Vercel](https://vercel.com/)

### Frontend

- **Framework**: [React](https://react.dev/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Routing**: [React Router](https://reactrouter.com/)
- **HTTP Client**: [Axios](https://axios-http.com/)
- **Styling**: CSS with CSS Variables
- **Deployment**: [Vercel](https://vercel.com/)

## Architecture

1.  The **React Frontend** prompts the user for a story theme.
2.  On submission, it sends a request to the **FastAPI Backend** at the `POST /api/stories/create` endpoint.
3.  The backend creates a `StoryJob` record in the database and starts a background task.
4.  The background task uses **LangChain** to call the **Anthropic Claude LLM** with a detailed prompt, requesting a full branching story in a specific JSON format.
5.  The LLM's response is parsed and saved to the database as a `Story` with multiple `StoryNode` entries.
6.  The frontend polls the `GET /api/jobs/{job_id}` endpoint to check the status of the generation job.
7.  Once the job is complete, the frontend navigates to the story page, fetching the full story data from `GET /api/stories/{story_id}/complete`.
8.  The user can then play through the story, with each choice loading the next node's content.

## Local Development

### Prerequisites

- Python 3.13+
- Node.js & npm
- An [Anthropic API Key](https://console.anthropic.com/dashboard)

### Backend Setup

1.  Navigate to the backend directory:
    ```sh
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4.  Create a `.env` file and add your Anthropic API key:
    ```
    # backend/.env
    ANTHROPIC_API_KEY="sk-ant-..."
    DATABASE_URL="sqlite:///./database.db"
    ```
5.  Initialize the database:
    ```sh
    python init_db.py
    ```
6.  Run the development server:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

### Frontend Setup

1.  Navigate to the frontend directory:
    ```sh
    cd frontend
    ```
2.  Install dependencies:
    ```sh
    npm install
    ```
3.  Create a `.env.local` file to proxy requests to your local backend:
    ```
    # frontend/.env.local
    VITE_API_URL=/api
    VITE_DEBUG=true
    ```
    _Note: The `vite.config.js` is configured to use this variable to set up a proxy._
4.  Run the development server:
    ```sh
    npm run dev
    ```
    The application will be available at `http://localhost:5173`.

## Deployment

This project is configured for deployment on [Vercel](https://vercel.com/). Both the `frontend` and `backend` directories contain a `vercel.json` file that configures the build and deployment settings.

- **Frontend**: Deployed as a Vite application.
- **Backend**: Deployed as a Vercel Serverless Function using the Python runtime.

The live application can be found at:

- **Frontend**: [https://choose-your-adventure.vercel.app/](https://choose-your-adventure.vercel.app/)
- **Backend API**: [https://choose-your-adventure-backend.vercel.app/](https://choose-your-adventure-backend.vercel.app/)

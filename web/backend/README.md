# Vietnamese Writing Skills - Backend API

FastAPI backend service exposing linter analysis, pattern metadata, Gemini rewrite integration, and contribution staging for the Vietnamese Writing Skills web application.

## Quick Start (Local Development)

1. Ensure the parent package is installed:
   ```bash
   pip install -e ../..
   ```

2. Install backend dependencies:
   ```bash
   pip install -e .
   ```

3. Copy environment settings:
   ```bash
   cp .env.example .env
   ```

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

   The backend will start at `http://localhost:8000`. You can inspect OpenAPI docs at `http://localhost:8000/docs`.

## Running Tests

```bash
pytest
```

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.config import settings
from app.db import models  # noqa: F401 - ensure models are registered with Base
from app.db.database import Base, engine
from app.limiter import limiter
from app.routers import admin, contributions, health, lint, patterns, rewrite


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Vietnamese Writing Skills API",
    description="Web API service for Vietnamese writing style analysis and skills",
    version="0.2.0",
    lifespan=lifespan,
)

# Slowapi setup
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS setup
origins = [origin.strip() for origin in settings.FRONTEND_ORIGIN.split(",") if origin.strip()]
if not origins:
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts=["*"])

# Include Routers
app.include_router(health.router)
app.include_router(lint.router)
app.include_router(patterns.router)
app.include_router(rewrite.router)
app.include_router(contributions.router)
app.include_router(admin.router)

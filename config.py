from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Database configuration
DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_aVFeM96EgyWd@ep-autumn-hill-ad4xrr4g-pooler.c-2.us-east-1.aws.neon.tech/neondb?ssl=require"
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# FastAPI app configuration
app = FastAPI(title="BazaarHub")

# Templates configuration
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
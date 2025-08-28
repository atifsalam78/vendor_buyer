from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

# Base declarative class
Base = declarative_base()

# Database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./bazaarhub.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI app configuration
app = FastAPI(title="BazaarHub")

# Templates configuration
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
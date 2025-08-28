from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
from pathlib import Path

# Import models and database
from models import Base, User, Vendor, Buyer
from config import engine, SessionLocal, app, templates

# Drop all tables and recreate them
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/main", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/plans", response_class=HTMLResponse)
async def plans(request: Request):
    return templates.TemplateResponse("plans.html", {"request": request})

@app.post("/register/vendor")
async def register_vendor(
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    email = form_data.get("email")
    password = form_data.get("password")
    mobile = form_data.get("mobile")
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.mobile == mobile)
        ).first()
        
        if existing_user:
            return {
                "success": False, 
                "message": "Email or mobile already exists",
                "details": {
                    "email_exists": existing_user.email == email,
                    "mobile_exists": existing_user.mobile == mobile
                }
            }
            
        # Create new vendor
        new_vendor = Vendor(
            email=email,
            mobile=mobile,
            type="vendor"  # Explicitly set the type
        )
        new_vendor.set_password(password)
        
        # Add to database
        db.add(new_vendor)
        db.commit()
        
        return {"success": True, "message": "Vendor registered successfully"}
    except IntegrityError:
        db.rollback()
        return {"success": False, "message": "Email or mobile already exists"}
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")  # Log the error
        return {"success": False, "message": "Registration failed. Please try again."}

@app.post("/register/buyer")
async def register_buyer(
    request: Request,
    db: Session = Depends(get_db)
):
    form_data = await request.form()
    email = form_data.get("email")
    password = form_data.get("password")
    mobile = form_data.get("mobile")
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == email) | (User.mobile == mobile)
        ).first()
        
        if existing_user:
            return {
                "success": False, 
                "message": "Email or mobile already exists",
                "details": {
                    "email_exists": existing_user.email == email,
                    "mobile_exists": existing_user.mobile == mobile
                }
            }
            
        # Create new buyer
        new_buyer = Buyer(
            email=email,
            mobile=mobile,
            type="buyer"  # Explicitly set the type
        )
        new_buyer.set_password(password)
        
        # Add to database
        db.add(new_buyer)
        db.commit()
        
        return {"success": True, "message": "Buyer registered successfully"}
    except IntegrityError:
        db.rollback()
        return {"success": False, "message": "Email or mobile already exists"}
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")  # Log the error
        return {"success": False, "message": "Registration failed. Please try again."}
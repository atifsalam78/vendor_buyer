from fastapi import Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

# Import models and database
from models import Base, User, Vendor, Buyer
from config import engine, AsyncSessionLocal, app, templates

# Async function to drop and recreate tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
 
# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    await init_db()

# Async dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

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
    db: AsyncSession = Depends(get_db)
):
    form_data = await request.form()
    email = form_data.get("email")
    password = form_data.get("password")
    mobile = form_data.get("mobile")
    try:
        # Check if user already exists
        result = await db.execute(
            select(User).where(
                (User.email == email) | (User.mobile == mobile)
            )
        )
        existing_user = result.scalars().first()
        
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
        await db.commit()
        
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
    db: AsyncSession = Depends(get_db)
):
    form_data = await request.form()
    email = form_data.get("email")
    password = form_data.get("password")
    mobile = form_data.get("mobile")
    try:
        # Check if user already exists
        result = await db.execute(
            select(User).where(
                (User.email == email) | (User.mobile == mobile)
            )
        )
        existing_user = result.scalars().first()
        
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
        await db.commit()
        
        return {"success": True, "message": "Buyer registered successfully"}
    except IntegrityError:
        db.rollback()
        return {"success": False, "message": "Email or mobile already exists"}
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")  # Log the error
        return {"success": False, "message": "Registration failed. Please try again."}
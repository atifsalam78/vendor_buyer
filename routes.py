from fastapi import APIRouter, HTTPException, Depends, Request, Form, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime, timedelta
import bcrypt
import jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import BusinessCategory, BusinessType, Designation, Gender, User, Vendor, Buyer
from config import templates, get_db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT settings
SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # In production, use a secure key and store in environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
# Helper functions for authentication

# Routes for pages
@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/plan", response_class=HTMLResponse)
async def plan_page(request: Request):
    return templates.TemplateResponse("plan.html", {"request": request})

# Registration routes
@router.post("/register/vendor")
async def register_vendor(
    request: Request,
    email: str = Form(...),
    mobile: str = Form(...),
    password: str = Form(...),
    business_name: str = Form(...),
    year_established: int = Form(...),
    business_category: str = Form(...),
    business_type: str = Form(...),
    business_address: str = Form(...),
    country: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    postal_code: str = Form(None),
    ntn: str = Form(...),
    landline: str = Form(None),
    website: str = Form(None),
    gender: str = Form(...),
    geo_lat: float = Form(None),
    geo_lng: float = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Create new vendor
        new_vendor = Vendor(
            email=email,
            mobile=mobile,
            gender=gender,
            business_name=business_name,
            year_established=year_established,
            business_category=business_category,
            business_type=business_type,
            business_address=business_address,
            country=country,
            state=state,
            city=city,
            postal_code=postal_code,
            ntn=ntn,
            landline=landline,
            website=website,
            geo_lat=geo_lat,
            geo_lng=geo_lng
        )
        
        # Set password
        new_vendor.set_password(password)
        
        # Add to database
        db.add(new_vendor)
        db.commit()
        db.refresh(new_vendor)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Vendor registered successfully", "success": True}
        )
    
    except IntegrityError as e:
        db.rollback()
        error_message = str(e)
        if "email" in error_message:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Email already registered", "success": False}
            )
        elif "mobile" in error_message:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Mobile number already registered", "success": False}
            )
        elif "ntn" in error_message:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "NTN already registered", "success": False}
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Registration failed", "success": False}
            )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"An error occurred: {str(e)}", "success": False}
        )

@router.post("/register/buyer")
async def register_buyer(
    request: Request,
    email: str = Form(...),
    mobile: str = Form(...),
    password: str = Form(...),
    buyer_name: str = Form(...),
    company_name: str = Form(...),
    designation: str = Form(...),
    company_address: str = Form(...),
    country: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    website: str = Form(None),
    gender: str = Form(...),
    geo_lat: float = Form(None),
    geo_lng: float = Form(None),
    db: Session = Depends(get_db)
):
    try:
        # Create new buyer
        new_buyer = Buyer(
            email=email,
            mobile=mobile,
            gender=gender,
            buyer_name=buyer_name,
            company_name=company_name,
            designation=designation,
            company_address=company_address,
            country=country,
            state=state,
            city=city,
            website=website,
            geo_lat=geo_lat,
            geo_lng=geo_lng
        )
        
        # Set password
        new_buyer.set_password(password)
        
        # Add to database
        db.add(new_buyer)
        db.commit()
        db.refresh(new_buyer)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Buyer registered successfully", "success": True}
        )
    
    except IntegrityError as e:
        db.rollback()
        error_message = str(e)
        if "email" in error_message:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Email already registered", "success": False}
            )
        elif "mobile" in error_message:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Mobile number already registered", "success": False}
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "Registration failed", "success": False}
            )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"An error occurred: {str(e)}", "success": False}
        )
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: Optional[str] = None
    user_type: Optional[str] = None
    
class VendorRegistration(BaseModel):
    email: EmailStr
    password: str
    business_name: str
    year_established: int
    business_category: str
    business_type: str
    business_address: str
    country: str
    state: str
    city: str
    postal_code: str
    ntn: str
    mobile: str
    landline: Optional[str] = None
    website: Optional[str] = None
    gender: str
    
class BuyerRegistration(BaseModel):
    email: EmailStr
    password: str
    buyer_name: str
    company_name: str
    designation: str
    company_address: str
    country: str
    state: str
    city: str
    mobile: str
    website: Optional[str] = None
    gender: str

async def authenticate_user(db, email, password):
    # Try to find user in vendor table
    vendor = db.query(Vendor).filter(Vendor.email == email).first()
    if vendor and vendor.verify_password(password):
        return {"email": vendor.email, "user_type": "vendor", "id": vendor.id}
    
    # Try to find user in buyer table
    buyer = db.query(Buyer).filter(Buyer.email == email).first()
    if buyer and buyer.verify_password(password):
        return {"email": buyer.email, "user_type": "buyer", "id": buyer.id}
    
    return None

# Page routes
@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@router.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@router.get("/plans", response_class=HTMLResponse)
async def plans_page(request: Request):
    return templates.TemplateResponse("plans.html", {"request": request})

@router.get("/api/profile")
async def get_profile(request: Request, db=Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        user_type = payload.get("user_type")
        
        if not email:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        # Query the database based on user type
        if user_type == "vendor":
            query = "SELECT * FROM vendor WHERE email = $1"
        else:
            query = "SELECT * FROM buyer WHERE email = $1"
            
        user = await db.fetchrow(query, email)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert to dict and return
        user_dict = dict(user)
        user_dict["user_type"] = user_type
        
        return user_dict
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# API endpoints
@router.post("/api/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Determine user type
    user_type = "vendor" if isinstance(user, Vendor) else "buyer"
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_type": user_type, "user_id": user.id}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/api/register/vendor", status_code=status.HTTP_201_CREATED)
async def register_vendor(vendor: VendorRegistration, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_email = await db.fetchval("SELECT id FROM vendor WHERE email = $1", vendor.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if mobile already exists
    existing_mobile = await db.fetchval("SELECT id FROM vendor WHERE mobile = $1", vendor.mobile)
    if existing_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    # Check if NTN already exists
    existing_ntn = await db.fetchval("SELECT id FROM vendor WHERE ntn = $1", vendor.ntn)
    if existing_ntn:
        raise HTTPException(status_code=400, detail="NTN already registered")
    
    # Hash the password
    hashed_password = get_password_hash(vendor.password)
    
    # Insert into database
    try:
        await db.execute("""
            INSERT INTO vendor (
                email, password, business_name, year_established, business_category, 
                business_type, business_address, country, state, city, postal_code, 
                ntn, mobile, landline, website, gender, geo_lat, geo_lng, date_joined
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19)
        """, 
        vendor.email, hashed_password, vendor.business_name, vendor.year_established, 
        vendor.business_category, vendor.business_type, vendor.business_address, 
        vendor.country, vendor.state, vendor.city, vendor.postal_code, vendor.ntn, 
        vendor.mobile, vendor.landline, str(vendor.website) if vendor.website else None, 
        vendor.gender, vendor.geo_lat, vendor.geo_lng, datetime.now())
        
        return {"message": "Vendor registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/api/register/buyer", status_code=status.HTTP_201_CREATED)
async def register_buyer(buyer: BuyerRegistration, db: asyncpg.Connection = Depends(get_db)):
    # Check if email already exists
    existing_email = await db.fetchval("SELECT id FROM buyer WHERE email = $1", buyer.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if mobile already exists
    existing_mobile = await db.fetchval("SELECT id FROM buyer WHERE mobile = $1", buyer.mobile)
    if existing_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    # Hash the password
    hashed_password = get_password_hash(buyer.password)
    
    # Insert into database
    try:
        await db.execute("""
            INSERT INTO buyer (
                email, password, buyer_name, company_name, designation, 
                company_address, country, state, city, mobile, website, 
                gender, geo_lat, geo_lng, date_joined
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        """, 
        buyer.email, hashed_password, buyer.buyer_name, buyer.company_name, 
        buyer.designation, buyer.company_address, buyer.country, buyer.state, 
        buyer.city, buyer.mobile, str(buyer.website) if buyer.website else None, 
        buyer.gender, buyer.geo_lat, buyer.geo_lng, datetime.now())
        
        return {"message": "Buyer registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/api/check-email")
async def check_email(email: str, type: str, db: asyncpg.Connection = Depends(get_db)):
    if type == "vendor":
        exists = await db.fetchval("SELECT EXISTS(SELECT 1 FROM vendor WHERE email = $1)", email)
    else:
        exists = await db.fetchval("SELECT EXISTS(SELECT 1 FROM buyer WHERE email = $1)", email)
    return {"exists": exists}

@router.get("/api/check-mobile")
async def check_mobile(mobile: str, type: str, db: asyncpg.Connection = Depends(get_db)):
    if type == "vendor":
        exists = await db.fetchval("SELECT EXISTS(SELECT 1 FROM vendor WHERE mobile = $1)", mobile)
    else:
        exists = await db.fetchval("SELECT EXISTS(SELECT 1 FROM buyer WHERE mobile = $1)", mobile)
    return {"exists": exists}

@router.get("/api/check-ntn")
async def check_ntn(ntn: str, db: asyncpg.Connection = Depends(get_db)):
    exists = await db.fetchval("SELECT EXISTS(SELECT 1 FROM vendor WHERE ntn = $1)", ntn)
    return {"exists": exists}

class VendorRegistration(BaseModel):
    email: EmailStr
    password: str
    business_name: str
    year_of_establishment: int
    business_category: BusinessCategory
    business_type: BusinessType
    address: str
    country: str
    state: str
    city: str
    postal_code: Optional[str] = None
    ntn: Optional[str] = None
    mobile_number: str
    landline_number: Optional[str] = None
    website: Optional[str] = None
    gender: Gender

class BuyerRegistration(BaseModel):
    email: EmailStr
    password: str
    name: str
    company_name: str
    designation: Designation
    address: str
    country: str
    state: str
    city: str
    mobile_number: str
    website: Optional[str] = None
    gender: Gender

@router.post("/register/vendor")
async def register_vendor(vendor: VendorRegistration, pool: asyncpg.Pool = Depends(get_db)):
    try:
        async with pool.acquire() as connection:
            # Check if email or mobile already exists
            exists = await connection.fetchval(
                """SELECT 1 FROM vendor WHERE email = $1 OR mobile_number = $2""",
                vendor.email, vendor.mobile_number
            )
            if exists:
                raise HTTPException(status_code=400, detail="Email or mobile number already registered")
            
            # Insert new vendor
            await connection.execute(
                """
                INSERT INTO vendor (
                    email, password, business_name, year_of_establishment,
                    business_category, business_type, address, country, state, city,
                    postal_code, ntn, mobile_number, landline_number, website, gender
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
                """,
                vendor.email, vendor.password, vendor.business_name, vendor.year_of_establishment,
                vendor.business_category.value, vendor.business_type.value, vendor.address,
                vendor.country, vendor.state, vendor.city, vendor.postal_code, vendor.ntn,
                vendor.mobile_number, vendor.landline_number, vendor.website, vendor.gender.value
            )
            return {"message": "Vendor registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register/buyer")
async def register_buyer(buyer: BuyerRegistration, pool: asyncpg.Pool = Depends(get_db)):
    try:
        async with pool.acquire() as connection:
            # Check if email or mobile already exists
            exists = await connection.fetchval(
                """SELECT 1 FROM buyer WHERE email = $1 OR mobile_number = $2""",
                buyer.email, buyer.mobile_number
            )
            if exists:
                raise HTTPException(status_code=400, detail="Email or mobile number already registered")
            
            # Insert new buyer
            await connection.execute(
                """
                INSERT INTO buyer (
                    email, password, name, company_name, designation,
                    address, country, state, city, mobile_number, website, gender
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                """,
                buyer.email, buyer.password, buyer.name, buyer.company_name,
                buyer.designation.value, buyer.address, buyer.country, buyer.state,
                buyer.city, buyer.mobile_number, buyer.website, buyer.gender.value
            )
            return {"message": "Buyer registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
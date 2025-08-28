from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Enum, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Enum classes
class BusinessCategory(enum.Enum):
    RETAIL = "Retail"
    WHOLESALE = "Wholesale"
    MANUFACTURING = "Manufacturing"
    SERVICE = "Service"

class BusinessType(enum.Enum):
    SOLE_PROPRIETORSHIP = "Sole Proprietorship"
    PARTNERSHIP = "Partnership"
    CORPORATION = "Corporation"
    LLC = "Limited Liability Company"

class Designation(enum.Enum):
    CEO = "Chief Executive Officer"
    MANAGER = "Manager"
    OWNER = "Owner"
    DIRECTOR = "Director"

class Gender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

# Base User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    mobile = Column(String, unique=True)
    type = Column(String(50), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }
    
    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

# Vendor model
class Vendor(User):
    __tablename__ = "vendors"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    business_name = Column(String, nullable=True)
    ntn = Column(String, unique=True, nullable=True)
    business_category = Column(String, nullable=True)
    business_type = Column(String, nullable=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'vendor',
    }

# Buyer model
class Buyer(User):
    __tablename__ = "buyers"
    
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'buyer',
    }
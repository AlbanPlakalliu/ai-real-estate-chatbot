from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserPreferences(BaseModel):
    preferred_locations: List[str] = []
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    preferred_bedrooms: Optional[int] = None
    preferred_property_types: List[str] = []
    must_have_features: List[str] = []

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True
    preferences: Optional[UserPreferences] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class SavedProperty(BaseModel):
    property_id: int
    saved_at: datetime
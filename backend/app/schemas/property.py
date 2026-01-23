from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PropertyBase(BaseModel):
    title: str
    description: str
    price: float
    bedrooms: int
    bathrooms: int
    area: Optional[float] = None  # square meters
    address: str
    city: str = "London"
    postcode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_type: str  # apartment, house, flat, etc.
    image_urls: List[str] = []
    features: List[str] = []  # parking, garden, balcony, etc.
    is_available: bool = True

class PropertyCreate(PropertyBase):
    pass

class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None

class Property(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    views: int = 0
    
    class Config:
        from_attributes = True

class PropertySearchRequest(BaseModel):
    location: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    bedrooms: Optional[int] = Field(None, ge=0, le=10)
    bathrooms: Optional[int] = Field(None, ge=0, le=10)
    property_type: Optional[str] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    features: Optional[List[str]] = []
    sort_by: Optional[str] = "price"  # price, date, views
    sort_order: Optional[str] = "asc"  # asc, desc
    page: int = Field(1, ge=1)
    page_size: int = Field(10, ge=1, le=100)

class PropertySearchResponse(BaseModel):
    properties: List[Property]
    total: int
    page: int
    page_size: int
    total_pages: int
# zomato_v1: Basic Pydantic imports for restaurant schemas
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import time, datetime
# zomato_v2: Decimal import for menu item price handling
from decimal import Decimal
import re

# zomato_v1: Restaurant schemas for basic CRUD operations
class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: str = Field(..., min_length=1, max_length=50)
    address: str = Field(..., min_length=1, max_length=255)
    phone_number: str = Field(..., min_length=10, max_length=20)
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    is_active: bool = Field(default=True)
    opening_time: time
    closing_time: time
    
    # zomato_v1: Phone number validation as per V1 requirements
    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        # Basic phone number validation - digits, spaces, hyphens, parentheses, plus
        pattern = r'^[\+]?[1-9][\d\s\-\(\)]{8,18}$'
        if not re.match(pattern, v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
            raise ValueError('Invalid phone number format')
        return v
    
    # zomato_v1: Time validation as per V1 requirements
    @field_validator('closing_time')
    def validate_closing_time(cls, v, values):
        if 'opening_time' in values and v <= values['opening_time']:
            raise ValueError('Closing time must be after opening time')
        return v

# zomato_v1: Restaurant create schema
class RestaurantCreate(RestaurantBase):
    pass

# zomato_v1: Restaurant update schema
class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: Optional[str] = Field(None, min_length=1, max_length=50)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=20)
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_active: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    
    # zomato_v1: Phone number validation for updates
    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if v is not None:
            pattern = r'^[\+]?[1-9][\d\s\-\(\)]{8,18}$'
            if not re.match(pattern, v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
                raise ValueError('Invalid phone number format')
        return v

# zomato_v1: Restaurant response schema
class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# zomato_v2: Menu Item schemas for menu management
class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    is_vegetarian: bool = Field(default=False)
    is_vegan: bool = Field(default=False)
    is_available: bool = Field(default=True)
    preparation_time: Optional[int] = Field(None, gt=0)
    
    # zomato_v2: Price validation for menu items
    @field_validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        # Ensure price has at most 2 decimal places
        return v.quantize(Decimal('0.01'))

# zomato_v2: Menu item create schema
class MenuItemCreate(MenuItemBase):
    pass

# zomato_v2: Menu item update schema
class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, gt=0)
    
    # zomato_v2: Price validation for menu item updates
    @field_validator('price')
    def validate_price(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError('Price must be positive')
            # Ensure price has at most 2 decimal places
            return v.quantize(Decimal('0.01'))
        return v

# zomato_v2: Menu item response schema
class MenuItemResponse(MenuItemBase):
    id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# zomato_v2: Menu item with restaurant details schema
class MenuItemWithRestaurant(MenuItemResponse):
    restaurant: RestaurantResponse

# zomato_v2: Restaurant with menu items schema (nested relationship)
class RestaurantWithMenu(RestaurantResponse):
    menu_items: List[MenuItemResponse] = []
# zomato_v1: Basic SQLAlchemy imports for restaurant model
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Time, DateTime, ForeignKey, Numeric
# zomato_v2: Relationship import for one-to-many relationships
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# zomato_v1: Restaurant model with all required V1 fields
class Restaurant(Base):
    __tablename__ = "restaurants"
    
    # zomato_v1: All basic restaurant fields as per V1 requirements
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    cuisine_type = Column(String(50), nullable=False, index=True)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True, index=True)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # zomato_v2: Relationship with menu items (one-to-many)
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")

# zomato_v2: MenuItem model for menu management with relationships
class MenuItem(Base):
    __tablename__ = "menu_items"
    
    # zomato_v2: All menu item fields as per V2 requirements
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    is_vegetarian = Column(Boolean, default=False, index=True)
    is_vegan = Column(Boolean, default=False, index=True)
    is_available = Column(Boolean, default=True, index=True)
    preparation_time = Column(Integer, nullable=True)  # in minutes
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # zomato_v2: Relationship back to restaurant
    restaurant = relationship("Restaurant", back_populates="menu_items")
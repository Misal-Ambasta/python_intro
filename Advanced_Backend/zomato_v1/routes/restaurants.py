# zomato_v1: Basic FastAPI imports for restaurant routes
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_database
# zomato_v1: Restaurant schemas for basic CRUD
from schemas import RestaurantCreate, RestaurantUpdate, RestaurantResponse, RestaurantWithMenu
import crud

# zomato_v1: Restaurant router with basic endpoints
router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# zomato_v1: Create restaurant endpoint as per V1 requirements
@router.post("/", response_model=RestaurantResponse, status_code=201)
async def create_restaurant(
    restaurant: RestaurantCreate,
    db: AsyncSession = Depends(get_database)
):
    """Create a new restaurant"""
    # Check if restaurant name already exists
    existing_restaurant = await crud.get_restaurant_by_name(db, restaurant.name)
    if existing_restaurant:
        raise HTTPException(
            status_code=400,
            detail="Restaurant with this name already exists"
        )
    
    return await crud.create_restaurant(db, restaurant)

# zomato_v1: List all restaurants with pagination
@router.get("/", response_model=List[RestaurantResponse])
async def list_restaurants(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """List all restaurants with pagination"""
    return await crud.get_restaurants(db, skip=skip, limit=limit)

# zomato_v1: List active restaurants endpoint
@router.get("/active", response_model=List[RestaurantResponse])
async def list_active_restaurants(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """List only active restaurants with pagination"""
    return await crud.get_active_restaurants(db, skip=skip, limit=limit)

# zomato_v1: Search restaurants by cuisine endpoint
@router.get("/search", response_model=List[RestaurantResponse])
async def search_restaurants(
    cuisine: str = Query(..., description="Cuisine type to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """Search restaurants by cuisine type"""
    return await crud.search_restaurants_by_cuisine(db, cuisine, skip=skip, limit=limit)

# zomato_v1: Get specific restaurant by ID
@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific restaurant by ID"""
    restaurant = await crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# zomato_v2: Get restaurant with menu items (relationship endpoint)
@router.get("/{restaurant_id}/with-menu", response_model=RestaurantWithMenu)
async def get_restaurant_with_menu(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get restaurant with all menu items"""
    restaurant = await crud.get_restaurant_with_menu(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

# zomato_v1: Update restaurant endpoint
@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    restaurant_update: RestaurantUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update a restaurant"""
    # Check if restaurant exists
    existing_restaurant = await crud.get_restaurant(db, restaurant_id)
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Check if name is being updated and if it conflicts with existing restaurant
    if restaurant_update.name:
        name_conflict = await crud.get_restaurant_by_name(db, restaurant_update.name)
        if name_conflict and name_conflict.id != restaurant_id:
            raise HTTPException(
                status_code=400,
                detail="Restaurant with this name already exists"
            )
    
    updated_restaurant = await crud.update_restaurant(db, restaurant_id, restaurant_update)
    return updated_restaurant

# zomato_v1: Delete restaurant endpoint
@router.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete a restaurant"""
    success = await crud.delete_restaurant(db, restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
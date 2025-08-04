from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_database
from schemas import RestaurantCreate, RestaurantUpdate, RestaurantResponse
import crud

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

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

@router.get("/", response_model=List[RestaurantResponse])
async def list_restaurants(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """List all restaurants with pagination"""
    return await crud.get_restaurants(db, skip=skip, limit=limit)

@router.get("/active", response_model=List[RestaurantResponse])
async def list_active_restaurants(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """List only active restaurants with pagination"""
    return await crud.get_active_restaurants(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[RestaurantResponse])
async def search_restaurants(
    cuisine: str = Query(..., description="Cuisine type to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """Search restaurants by cuisine type"""
    return await crud.search_restaurants_by_cuisine(db, cuisine, skip=skip, limit=limit)

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

@router.delete("/{restaurant_id}", status_code=204)
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete a restaurant"""
    success = await crud.delete_restaurant(db, restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
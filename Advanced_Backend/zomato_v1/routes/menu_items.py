# zomato_v2: FastAPI imports for menu item routes (V2 feature)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from database import get_database
# zomato_v2: Menu item schemas for menu management
from schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse, MenuItemWithRestaurant
import crud

# zomato_v2: Menu items router for menu management
router = APIRouter(tags=["menu-items"])

# zomato_v2: Add menu item to restaurant endpoint
@router.post("/restaurants/{restaurant_id}/menu-items/", response_model=MenuItemResponse, status_code=201)
async def add_menu_item_to_restaurant(
    restaurant_id: int,
    menu_item: MenuItemCreate,
    db: AsyncSession = Depends(get_database)
):
    """Add menu item to restaurant"""
    # Check if restaurant exists
    restaurant = await crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return await crud.create_menu_item(db, menu_item, restaurant_id)

# zomato_v2: List all menu items endpoint
@router.get("/menu-items/", response_model=List[MenuItemResponse])
async def list_menu_items(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """List all menu items"""
    return await crud.get_menu_items(db, skip=skip, limit=limit)

# zomato_v2: Get specific menu item endpoint
@router.get("/menu-items/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get specific menu item"""
    menu_item = await crud.get_menu_item(db, item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item

# zomato_v2: Get menu item with restaurant details endpoint
@router.get("/menu-items/{item_id}/with-restaurant", response_model=MenuItemWithRestaurant)
async def get_menu_item_with_restaurant(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get menu item with restaurant details"""
    menu_item = await crud.get_menu_item_with_restaurant(db, item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item

# zomato_v2: Get all menu items for a restaurant endpoint
@router.get("/restaurants/{restaurant_id}/menu", response_model=List[MenuItemResponse])
async def get_restaurant_menu(
    restaurant_id: int,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get all menu items for a restaurant"""
    # Check if restaurant exists
    restaurant = await crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return await crud.get_restaurant_menu(db, restaurant_id, skip=skip, limit=limit)

# zomato_v2: Search menu items with advanced filters endpoint
@router.get("/menu-items/search", response_model=List[MenuItemResponse])
async def search_menu_items(
    category: Optional[str] = Query(None, description="Filter by category"),
    vegetarian: Optional[bool] = Query(None, description="Filter by vegetarian status"),
    vegan: Optional[bool] = Query(None, description="Filter by vegan status"),
    available: Optional[bool] = Query(None, description="Filter by availability"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: AsyncSession = Depends(get_database)
):
    """Search menu items by various filters"""
    return await crud.search_menu_items(
        db, 
        category=category, 
        vegetarian=vegetarian,
        vegan=vegan,
        available=available,
        skip=skip, 
        limit=limit
    )

# zomato_v2: Update menu item endpoint
@router.put("/menu-items/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    menu_item_update: MenuItemUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update menu item"""
    # Check if menu item exists
    existing_item = await crud.get_menu_item(db, item_id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    updated_item = await crud.update_menu_item(db, item_id, menu_item_update)
    return updated_item

# zomato_v2: Delete menu item endpoint
@router.delete("/menu-items/{item_id}", status_code=204)
async def delete_menu_item(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete menu item"""
    success = await crud.delete_menu_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")

# zomato_v2: Calculate average menu price per restaurant endpoint
@router.get("/restaurants/{restaurant_id}/average-price")
async def get_restaurant_average_price(
    restaurant_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Calculate average menu price per restaurant"""
    # Check if restaurant exists
    restaurant = await crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    avg_price = await crud.get_restaurant_average_price(db, restaurant_id)
    return {
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant.name,
        "average_price": avg_price
    }
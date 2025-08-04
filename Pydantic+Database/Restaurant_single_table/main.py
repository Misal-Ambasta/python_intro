from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import List, Optional
from decimal import Decimal
import re

app = FastAPI()


menu_db = {}
id_counter = 1

class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"

class FoodItem(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: FoodCategory
    price: Decimal = Field(..., gt=0, max_digits=5, decimal_places=2)
    is_available: bool = True
    preparation_time: int = Field(..., ge=1, le=120)
    ingredients: List[str] = Field(..., min_items=1)
    calories: Optional[int] = Field(None, gt=0)
    is_vegetarian: bool = False
    is_spicy: bool = False

    @field_validator("name")
    def name_letter_spaces_only(cls, v):
        if not re.match(r"^[A-Za-z\s]+$", v):
            raise ValueError("Name should contain only letters and spaces")
        return v

    @field_validator("price")
    def price_range(cls, v):
        if not (Decimal("1.00") <= v <= Decimal("100.00")):
            raise ValueError("Price must be between $1.00 and $100.00")
        return v

    @field_validator("is_spicy")
    def dessert_beverage_not_spicy(cls, v, values):
        if "category" in values and values["category"] in [FoodCategory.DESSERT, FoodCategory.BEVERAGE] and v:
            raise ValueError("Desserts and Beverages cannot be spicy")
        return v

    @field_validator("calories")
    def calories_limit_if_vegetarian(cls, v, values):
        if v and values.get("is_vegetarian") and v >= 800:
            raise ValueError("Vegetarian items must have calories less than 800")
        return v

    @field_validator("preparation_time")
    def prep_time_for_beverage(cls, v, values):
        if values.get("category") == FoodCategory.BEVERAGE and v > 10:
            raise ValueError("Beverage preparation time should be ≤ 10 minutes")
        return v

    @property
    def price_category(self):
        if self.price < 10:
            return "Budget"
        elif self.price <= 25:
            return "Mid-range"
        return "Premium"

    @property
    def dietary_info(self):
        info = []
        if self.is_vegetarian:
            info.append("Vegetarian")
        if self.is_spicy:
            info.append("Spicy")
        return info


# Helper: add ID & computed fields
def with_computed_fields(item_id, item: FoodItem):
    data = item.dict()
    data["id"] = item_id
    data["price_category"] = item.price_category
    data["dietary_info"] = item.dietary_info
    return data


# Routes

@app.get("/menu")
def get_all_menu():
    return [with_computed_fields(i, item) for i, item in menu_db.items()]

@app.get("/menu/{item_id}")
def get_menu_item(item_id: int = Path(..., ge=1)):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return with_computed_fields(item_id, menu_db[item_id])

@app.get("/menu/category/{category}")
def get_by_category(category: FoodCategory):
    result = []
    for i, item in menu_db.items():
        if item.category == category:
            result.append(with_computed_fields(i, item))
    return result

@app.post("/menu", status_code=201)
def add_menu_item(item: FoodItem):
    global id_counter
    menu_db[id_counter] = item
    response = with_computed_fields(id_counter, item)
    id_counter += 1
    return response

@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, item: FoodItem):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    menu_db[item_id] = item
    return with_computed_fields(item_id, item)

@app.delete("/menu/{item_id}", status_code=204)
def delete_menu_item(item_id: int):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del menu_db[item_id]
    return
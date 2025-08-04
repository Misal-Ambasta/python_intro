# Problem 2: Simple Restaurant Ordering System (Two Tables with Nested Models)

## Problem Statement

Extend the basic system to handle customer orders. You'll manage both the menu and customer orders using nested models to show relationships. This is a simplified version focusing on nested model concepts without complex business logic.

## Requirements

### Database Structure
- `menu_db = {}` - Dictionary storing FoodItem objects (same as Problem 1)
- `orders_db = {}` - Dictionary storing Order objects
- Orders contain nested customer info and order items

### Additional API Endpoints
- `POST /orders` - Create new order
- `GET /orders` - Get all orders
- `GET /orders/{order_id}` - Get specific order details
- `PUT /orders/{order_id}/status` - Update order status

## Simple Nested Data Models

Keep the same FoodItem model from Problem 1 (no changes needed).

### New Models with Simple Nesting

```python
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    DELIVERED = "delivered"

class OrderItem(BaseModel):
    # Simple nested model for items in order
    menu_item_id: int = Field(..., gt=0)
    menu_item_name: str = Field(..., min_length=1, max_length=100)  # Store name for easy access
    quantity: int = Field(..., gt=0, le=10)
    unit_price: Decimal = Field(..., gt=0, max_digits=6, decimal_places=2)

    # Simple computed property
    @property
    def item_total(self) -> Decimal:
        return self.quantity * self.unit_price

class Customer(BaseModel):
    # Simple nested customer model
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., regex=r'^\d{10}')
```

## 🧪 Simple Test Cases

1. **Valid Order**: Create order with 2 items and valid customer info
2. **Empty Items**: Try to create order with no items (should fail)
3. **Invalid Phone**: Try customer with phone "123" (should fail)
4. **Large Quantity**: Try to order 15 of one item (should fail, max is 10)
5. **Status Update**: Update order from PENDING to CONFIRMED

## 💡 Simple Sample Order Data

```python
sample_order = {
    "customer": {
        "name": "Alice Smith",
        "phone": "5551234567",
        "address": "123 Oak Street, Springfield"
    },
    "items": [
        {
            "menu_item_id": 1,  # Reference to Margherita Pizza
            "menu_item_name": "Margherita Pizza",  # Store name for easy access
            "quantity": 1,
            "unit_price": "15.99"
        },
        {
            "menu_item_id": 2,  # Reference to Chicken Wings
            "menu_item_name": "Spicy Chicken Wings",
            "quantity": 2,
            "unit_price": "12.50"
        }
    ]
}
```

### When created, this order will have:
- `customer.name = "Alice Smith"`
- `items[0].item_total = 15.99`
- `items[1].item_total = 25.00`
- `items_total = 40.99`
- `total_amount = 43.98` (including $2.99 delivery)
- `total_items_count = 3`

## Focus Areas for Learning

### Nested Model Concepts
- **Creating nested models**: How Customer and OrderItem are embedded in Order
- **Validation in nested structures**: How validation works across model levels
- **Accessing nested data**: `order.customer.name` vs `order.items[0].quantity`
- **JSON serialization**: How nested models convert to/from JSON

### Simple Business Logic
- **Computed properties**: Calculate totals across nested items
- **Basic validation**: Ensure order has items and valid data
- **Model relationships**: How orders reference menu items by ID

## Technical Implementation Guidelines

### FastAPI Setup
```python
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
import uvicorn

app = FastAPI(
    title="Restaurant Ordering System",
    description="API for managing restaurant menu and orders",
    version="1.0.0"
)
```

### Error Handling
- Use appropriate HTTP status codes (200, 201, 400, 404, 422)
- Return meaningful error messages
- Handle ValidationError from Pydantic models
- Implement custom exception handlers

### Database Operations
```python
# Example structure
menu_db: Dict[int, FoodItem] = {}
orders_db: Dict[int, Order] = {}

# Auto-incrementing IDs
next_menu_id = 1
next_order_id = 1
```

### Response Models
Create separate response models for different scenarios:
- `FoodItemResponse` - For returning food items
- `OrderResponse` - For returning orders
- `OrderSummaryResponse` - For listing orders
- `ErrorResponse` - For error messages
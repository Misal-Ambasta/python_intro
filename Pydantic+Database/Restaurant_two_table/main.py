from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, List
from enum import Enum
from decimal import Decimal

app = FastAPI(
    title="Restaurant Ordering System",
    description="API for managing restaurant menu and orders",
    version="1.0.0"
)

# --------------------- Models ---------------------

class FoodItem(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., gt=0, max_digits=6, decimal_places=2)
    description: str = Field(..., max_length=255)


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    DELIVERED = "delivered"


class OrderItem(BaseModel):
    menu_item_id: int = Field(..., gt=0)
    menu_item_name: str = Field(..., min_length=1, max_length=100)
    quantity: int = Field(..., gt=0, le=10)
    unit_price: Decimal = Field(..., gt=0, max_digits=6, decimal_places=2)

    @property
    def item_total(self) -> Decimal:
        return self.quantity * self.unit_price


class Customer(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., regex=r'^\d{10}')
    address: str = Field(..., min_length=5, max_length=100)


class Order(BaseModel):
    id: int
    customer: Customer
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING

    @property
    def total_items_count(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def items_total(self) -> Decimal:
        return sum(item.item_total for item in self.items)

    @property
    def total_amount(self) -> Decimal:
        delivery_fee = Decimal("2.99")
        return self.items_total + delivery_fee


# Response model for readability
class OrderResponse(BaseModel):
    id: int
    customer: Customer
    items: List[OrderItem]
    total_items_count: int
    items_total: Decimal
    total_amount: Decimal
    status: OrderStatus


# --------------------- DBs ---------------------
menu_db: Dict[int, FoodItem] = {}
orders_db: Dict[int, Order] = {}
next_menu_id = 1
next_order_id = 1

# --------------------- Menu API (Optional Helper) ---------------------

@app.post("/menu", status_code=201)
def add_menu_item(item: FoodItem):
    global next_menu_id
    item.id = next_menu_id
    menu_db[next_menu_id] = item
    next_menu_id += 1
    return item


@app.get("/menu", response_model=List[FoodItem])
def get_menu():
    return list(menu_db.values())


# --------------------- Orders API ---------------------

@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order_data: dict):
    global next_order_id

    try:
        customer = Customer(**order_data["customer"])
        items_data = order_data.get("items", [])
        if not items_data:
            raise HTTPException(status_code=400, detail="Order must contain at least one item.")

        order_items = []
        for item in items_data:
            order_item = OrderItem(**item)
            order_items.append(order_item)

        order = Order(
            id=next_order_id,
            customer=customer,
            items=order_items
        )
        orders_db[next_order_id] = order
        next_order_id += 1

        return OrderResponse(
            id=order.id,
            customer=order.customer,
            items=order.items,
            total_items_count=order.total_items_count,
            items_total=order.items_total,
            total_amount=order.total_amount,
            status=order.status
        )

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())


@app.get("/orders", response_model=List[OrderResponse])
def get_all_orders():
    return [
        OrderResponse(
            id=o.id,
            customer=o.customer,
            items=o.items,
            total_items_count=o.total_items_count,
            items_total=o.items_total,
            total_amount=o.total_amount,
            status=o.status
        ) for o in orders_db.values()
    ]


@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int = Path(..., gt=0)):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderResponse(
        id=order.id,
        customer=order.customer,
        items=order.items,
        total_items_count=order.total_items_count,
        items_total=order.items_total,
        total_amount=order.total_amount,
        status=order.status
    )


@app.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status: OrderStatus):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status
    return OrderResponse(
        id=order.id,
        customer=order.customer,
        items=order.items,
        total_items_count=order.total_items_count,
        items_total=order.items_total,
        total_amount=order.total_amount,
        status=order.status
    )


# Product Class for E-commerce Platform

## Problem Statement
Create a Product class for an e-commerce platform with smart validation and automatic calculations.

## Requirements

### Private Attributes:
- `_name`
- `_base_price`
- `_discount_percent`
- `_stock_quantity`
- `_category`

### Use @property and setters with validation:

#### name:
- Must be 3-50 characters
- No special characters except hyphens and spaces

#### base_price:
- Must be positive
- Maximum $50,000

#### discount_percent:
- Must be 0-75%
- Automatically rounds to 2 decimal places

#### stock_quantity:
- Must be non-negative integer
- Maximum 10,000 units

#### category:
- Must be from predefined list: `['Electronics', 'Clothing', 'Books', 'Home', 'Sports']`

### Calculated Properties:

#### final_price:
- Base price minus discount

#### savings_amount:
- Amount saved due to discount

#### availability_status:
- "In Stock"
- "Low Stock" (<10)
- "Out of Stock"

#### product_summary:
- Formatted string with all key information
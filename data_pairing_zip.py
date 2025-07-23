products = ["Laptop", "Mouse", "Keyboard", "Monitor"]
prices = [999.99, 25.50, 75.00, 299.99]
quantities = [5, 20, 15, 8]

# Use zip() to pair each product with its corresponding price.
def pair_products_with_prices(products, prices):
    return list(zip(products, prices))

# For each product, calculate the total inventory value using the formula: price × quantity
def calculate_inventory_value(products, prices, quantities):
    return {product: price * quantity for product, price, quantity in zip(products, prices, quantities)}

# Create a dictionary where each product maps to another dictionary containing its price and quantity.
def create_inventory_dict(products, prices, quantities):
    return {product: {"price": price, "quantity": quantity} for product, price, quantity in zip(products, prices, quantities)}

# Identify and print the names of products with a quantity less than 10
def low_stock_products(products, quantities, threshold=10):
    return [product for product, quantity in zip(products, quantities) if quantity < threshold]

print(low_stock_products(products, quantities))
print(pair_products_with_prices(products, prices))
print(calculate_inventory_value(products, prices, quantities))  
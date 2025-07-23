inventory = {
    "apples":  {"price": 1.50, "quantity": 100},
    "bananas": {"price": 0.75, "quantity": 150},
    "oranges": {"price": 2.00, "quantity": 80}
}


def add_new_product(product_name, price, quantity):
    if product_name not in inventory:
        inventory[product_name] = {"price": price, "quantity": quantity}
    else:
        print(f"{product_name} already exists in the inventory.")

def update_product_price(product_name, new_price):
    if product_name in inventory:
        inventory[product_name]["price"] = new_price
    else:
        print(f"{product_name} does not exist in the inventory.")

def calculate_total_inventory_value():
    total_value = sum(item["price"] * item["quantity"] for item in inventory.values())
    print(f"Total inventory value: ${total_value:.2f}")

def low_stock_products(threshold):
    low_stock = {product: details for product, details in inventory.items() if details["quantity"] < threshold}
    print("Low stock products:", low_stock)


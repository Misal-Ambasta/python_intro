import math
items = 3;
output = {}
for i in range(items):
    item_price = float(input(f"Enter the price of item {i+1}: "))
    item_quantity = int(input(f"Enter the quantity of item {i+1}: "))
    output["item"+str(i+1)]= [item_price, item_quantity]

# print("Shopping List:", output)
sum = 0
for item, (price, quantity) in output.items():
    total = price * quantity
    print(f"{item}: {price} * {quantity} = {total}")
    sum += total

print(f"Subtotal: {sum}")
print(f"Tax (8.5%): {round(sum * 0.085, 2)}")
print(f"Total: {sum + (sum * 0.085)}")
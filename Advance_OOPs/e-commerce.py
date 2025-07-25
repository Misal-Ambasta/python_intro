import re

class Product:
    _allowed_categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
    
    def __init__(self, name, base_price, discount_percent, stock_quantity, category):
        self._name = name
        self._base_price = base_price
        self._discount_percent = discount_percent
        self._stock_quantity = stock_quantity
        self._category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not ( 3 <= len(value) <=50):
            raise ValueError("Name must be 3-50 characters")
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', value):
            raise ValueError("Name can only contain letters, digits, spaces, and hyphens.")
        self._name = value.strip()

    @property
    def base_price(self):
        return self._base_price

    @base_price.setter
    def base_price(self, value):
        if not (0 < value <= 50000):
            raise ValueError("Base price must be greater than 0 and at most $50,000.")
        self._base_price = float(value)

    @property
    def discount_percent(self):
        return self._discount_percent

    @discount_percent.setter
    def discount_percent(self, value):
        if not (0 <= value <=75):
            raise ValueError("Discount percent must be between 0 and 75.")
        self._discount_percent = round(float(value), 2)

    @property
    def stock_quantity(self):
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        if not (isinstance(value, int) and value >= 0 and value <= 10000):
            raise ValueError("Stock quantity must be an integer between 0 and 10,000.")
        self._stock_quantity = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value not in Product._allowed_categories:
            raise ValueError(f"Category must be one of: {Product._allowed_categories}")
        self._category = value

    @property
    def final_price(self):
        return round(self.base_price * (1 - self.discount_percent / 100), 2)

    @property
    def savings_amount(self):
        return round(self.base_price - self.final_price, 2)

    @property
    def availability_status(self):
        if self.stock_quantity == 0:
            return "Out of Stock"
        elif self.stock_quantity < 10:
            return "Low Stock"
        else:
            return "In Stock"

    @property
    def product_summary(self):
        return (
            f"Product Summary:\n"
            f"Name: {self.name}\n"
            f"Category: {self.category}\n"
            f"Base Price: ${self.base_price:.2f}\n"
            f"Discount: {self.discount_percent:.2f}%\n"
            f"Final Price: ${self.final_price:.2f}\n"
            f"You Save: ${self.savings_amount:.2f}\n"
            f"Stock: {self.stock_quantity} units ({self.availability_status})"
        )

    
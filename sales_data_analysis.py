sales_data = [
    ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)]),
    ("Q2", [("Apr", 1300), ("May", 1250), ("Jun", 1400)]),
    ("Q3", [("Jul", 1350), ("Aug", 1450), ("Sep", 1300)])
]

def calculate_total_sales_per_quarter(sales_data):
    total_sales = {}
    for quarter, months in sales_data:
        total_sales[quarter] = sum(sale for month, sale in months)
    print(total_sales)

calculate_total_sales_per_quarter(sales_data)

def highest_monthly_sales(sales_data):
    highest_sales = {}
    for quarter, months in sales_data:
        highest_month = max(months, key=lambda x: x[1])
        highest_sales[quarter] = highest_month
    print(highest_sales)

highest_monthly_sales(sales_data)
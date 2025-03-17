import json

# Load categories on startup
def load_categories(filepath="data/categories.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

CATEGORIES = load_categories()

# Optional: create a dict for quick lookup by name or id
CATEGORY_NAME_TO_ID = {f"{item['emoji']} {item['name']}": item['id'] for item in CATEGORIES}
CATEGORY_ID_TO_NAME = {item['id']: f"{item['emoji']} {item['name']}" for item in CATEGORIES}

# Load products
def load_products(filepath="data/products.json"):
    with open(filepath, "r",, encoding="utf-8") as f:
        return json.load(file)
        
PRODUCTS = json.load(f)

def get_products_by_category(category_id: str):
    return [product for product in PRODUCTS if product["category_id"] == category_id]

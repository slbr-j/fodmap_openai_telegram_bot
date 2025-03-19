import json
import os

# --- FILE PATHS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app/data_loader.py
DATA_DIR = os.path.join(BASE_DIR, "data")  # app/data

CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")


# --- LOAD CATEGORIES ---
def load_categories(filepath=CATEGORIES_FILE):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


CATEGORIES = load_categories()

# --- Create lookup dictionaries for categories ---
CATEGORY_NAME_TO_ID = {
    f"{item['emoji']} {item['name']}": item["id"] for item in CATEGORIES
}

CATEGORY_ID_TO_NAME = {
    item["id"]: f"{item['emoji']} {item['name']}" for item in CATEGORIES
}


# --- LOAD PRODUCTS ---
def load_products(filepath=PRODUCTS_FILE):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


PRODUCTS = load_products()


# --- UTILS ---
def get_products_by_category(category_id: str):
    """
    Returns a list of products filtered by category_id
    """
    return [
        product for product in PRODUCTS if product.get("category_id") == category_id
    ]

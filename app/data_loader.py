import json

# Load categories on startup
def load_categories(filepath="data/categories.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

CATEGORIES = load_categories()

# Optional: create a dict for quick lookup by name or id
CATEGORY_NAME_TO_ID = {f"{item['emoji']} {item['name']}": item['id'] for item in CATEGORIES}
CATEGORY_ID_TO_NAME = {item['id']: f"{item['emoji']} {item['name']}" for item in CATEGORIES}

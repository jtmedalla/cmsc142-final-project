food_items_db = {}

def add_food_item(name, serving_size, value_serving, tolerance):
    food_items_db[name] = {
        "serving_size": float(serving_size),
        "value_serving": float(value_serving),
        "tolerance": float(tolerance)
    }

def delete_food(name):
    food_items_db.pop(name, None)

def get_all_food():
    """
    Returns the current list of all food items stored in the database.
    """
    return food_items_db
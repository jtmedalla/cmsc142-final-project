def run_knapsack(max_weight: float, food_items: dict) -> dict:
 
    if max_weight <= 0:
        return {"allocations": [], "total_value": 0.0, "total_weight": 0.0}
 
    # candidate list
    candidates = []
    for name, details in food_items.items():
        serving_size = details["serving_size"]
        value_serving = details["value_serving"]
        tolerance = details["tolerance"]
 
        # skip no values
        if serving_size <= 0 or value_serving <= 0 or tolerance <= 0:
            continue
 
        ratio = value_serving / serving_size          # value per gram
        max_weight_from_item = tolerance * serving_size  # upper bound for this food
 
        candidates.append({
            "name": name,
            "serving_size": serving_size,
            "value_serving": value_serving,
            "tolerance": tolerance,
            "ratio": ratio,
            "max_weight_allowed": max_weight_from_item,
        })
 
    # sort descending
    candidates.sort(key=lambda x: x["ratio"], reverse=True)
 
    # greedy selection
    remaining_capacity = max_weight
    allocations = []
    total_value  = 0.0
    total_weight = 0.0
 
    for item in candidates:
        if remaining_capacity <= 0:
            break

        takeable_weight = min(item["max_weight_allowed"], remaining_capacity)
 
        servings_taken = takeable_weight / item["serving_size"]
 
        # partial serving handler
        full_servings = round(servings_taken)
        is_partial = abs(servings_taken - full_servings) > 1e-9
 
        weight_taken = servings_taken * item["serving_size"]
        value_gained = servings_taken * item["value_serving"]
 
        allocations.append({
            "name": item["name"],
            "servings_taken": round(servings_taken, 4),
            "weight_taken": round(weight_taken,   4),
            "value_gained": round(value_gained,   4),
            "is_partial": is_partial,
        })
 
        remaining_capacity -= weight_taken
        total_value += value_gained
        total_weight += weight_taken
 
    return {
        "allocations": allocations,
        "total_value": round(total_value,  4),
        "total_weight": round(total_weight, 4),
    }
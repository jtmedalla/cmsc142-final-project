# tester of knapsack
from core.knapsack import run_knapsack

# tester of graph
from core.graph import get_graph
import core.db as db

def test_knapsack():
    # sample food items
    food_items = {
        "Apple": {
            "serving_size": 150,   # grams
            "value_serving": 10,   # arbitrary value
            "tolerance": 3         # max servings allowed
        },
        "Bread": {
            "serving_size": 50,
            "value_serving": 8,
            "tolerance": 5
        },
        "Cheese": {
            "serving_size": 30,
            "value_serving": 12,
            "tolerance": 4
        },
        "Cake": {
            "serving_size": 200,
            "value_serving": 25,
            "tolerance": 2
        }
    }

    # run kanpsack
    max_weight = 500  # grams
    result = run_knapsack(max_weight, food_items)

    # print results
    print("=== Knapsack Test ===")
    print(f"Max Weight: {max_weight} g")
    print(f"Total Value: {result['total_value']}")
    print(f"Total Weight: {result['total_weight']}")
    print("\nAllocations:")
    for alloc in result["allocations"]:
        print(f"- {alloc['name']}: {alloc['servings_taken']} servings "
              f"({alloc['weight_taken']} g, value {alloc['value_gained']}, "
              f"partial={alloc['is_partial']})")
        
def test_graph():
    db.set_max_weight(1000)
    db.add_food_item("Adobo", 300, 200, 2)
    db.add_food_item("Sinigang", 100, 100, 1)
    db.add_food_item("Rice", 50, 50, 1)

    max_w = db.get_max_weight()
    max_food = db.get_all_food()

    result = run_knapsack(max_w, max_food)

    print(result["allocations"])

    get_graph(result["allocations"])

if __name__ == "__main__":
    test_graph()

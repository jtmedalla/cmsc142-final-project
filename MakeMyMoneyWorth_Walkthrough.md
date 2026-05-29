# Make My Money Worth (3MW)

## Overview

**Buffet Value Maximizer** is a desktop application built with Python and Tkinter that helps buffet-goers make smart eating decisions. It applies the **Greedy Knapsack algorithm** to determine the optimal combination of food items to maximize total monetary value (price recovery) while staying within a user-defined weight limit.

The application is the final project for **CMSC 142 — Design and Analysis of Algorithms**.

---

## The Problem It Solves

Imagine you're at a buffet. You have a limited stomach capacity (max weight), and each food item has:

- **Serving size** — how heavy one serving is (in grams)
- **Value per serving** — the price or cost of one serving (e.g., in pesos)
- **Max tolerance** — the maximum number of servings you'd be willing to eat

The app computes the best combination of servings — possibly including partial servings — to **maximize total monetary value** without exceeding your weight limit. This is a classic **fractional knapsack** variant solved greedily by value-to-weight ratio.

---

## Project Structure

```
cmsc142-final-project/
├── README.md
├── WALKTHROUGH.md                  ← You are here
├── src/
│   ├── main.py                     ← Entry point — launches the app
│   ├── test.py                     ← Standalone test script for core modules
│   ├── core/                       ← Algorithm & data logic (no UI)
│   │   ├── db.py                   ← In-memory database (food items + max weight)
│   │   ├── knapsack.py             ← Greedy fractional knapsack solver
│   │   └── graph.py                ← Pie chart generator (matplotlib)
│   └── ui/                         ← Graphical interface (Tkinter)
│       ├── main_GUI.py             ← Main window layout & widgets
│       ├── helpers.py              ← Shared UI logic (toasts, table, delete, calculate)
│       ├── add_item.py             ← "Add Food Item" popup form
│       └── edit_item.py            ← "Edit Food Item" popup form
```

---

## How to Run the Application

### Prerequisites

- Python 3.8 or higher
- Required packages: `tkinter` (built-in), `matplotlib`, `Pillow`

### Steps

1. **Install dependencies** (if not already installed):

   ```bash
   pip install matplotlib Pillow
   ```

2. **Run the app** from the project root:

   ```bash
   python src/main.py
   ```

   This calls `start_app_ui()` from `ui/main_GUI.py`, which builds and displays the main window.

---

## User Interface Walkthrough

### 1. Main Window

When you launch the app, you'll see a centered 950×550 window titled **"Buffet Value Maximizer 🍖♨️"** with a dark blue and light blue theme.

The window is split into two panels:

```
┌─────────────────────────────────────────────────────────┐
│  Buffet Value Maximizer 🍖♨️                           │
├──────────────────────────┬──────────────────────────────┤
│  Max Weight Consumable   │  Optimal Eating Allocation   │
│  [   Entry / Set    ]    │  Strategy                    │
│                          │                              │
│  ┌────────────────────┐  │  ┌──────────────────────┐    │
│  │ Food Item Table    │  │  │   Pie Chart          │    │
│  │ (Treeview)         │  │  │   (renders here)     │    │
│  │                    │  │  │                      │    │
│  └────────────────────┘  │  └──────────────────────┘    │
│                          │                              │
│  [➕ Add] [📝 Edit] [🗑️ Delete] │  [🚀 CALCULATE]     │
└──────────────────────────┴──────────────────────────────┘
```

### 2. Setting the Max Weight

- In the **top-left**, you'll see the label `Max Weight Consumable (g):`.
- If no weight is set, an entry field and a **Set** button appear.
- Type a number (grams) and click **Set**. A green toast confirms the value.
- Once set, the weight is displayed as read-only with an **✏️ Edit** button to change it.

### 3. Adding Food Items

Click the **➕ Add Food Item** button. A popup form appears with four fields:

| Field               | Description                                      | Validation                          |
|---------------------|--------------------------------------------------|-------------------------------------|
| Food Item Name      | Name of the dish (e.g., "Adobo")                 | Cannot be empty; must be unique     |
| Serving Size (g)    | Weight of one serving in grams                   | Must be a number > 0                |
| Value Per Serving   | The price/cost of one serving (e.g., in pesos)   | Must be a number > 0                |
| Max Tolerance       | Max servings you'd eat of this item              | Must be a number > 0                |

Click **Save Item** to add it to the table. A green toast confirms success.

### 4. Viewing Food Items in the Table

All added items appear in the **Treeview table** with columns:
- **Food Item Name**
- **Serving Size (g)**
- **Value Per Serving**
- **Max Tolerance**

### 5. Editing a Food Item

1. Click a row in the table to select it.
2. Click **📝 Edit Selected** — a popup appears pre-filled with the current values.
3. Modify any field and click **Save Changes**.

### 6. Deleting Food Items

The delete button has a **two-step checklist mode** to prevent accidental deletion:

1. **First click** — enters checklist mode. Each item gets a ☐ prefix.
2. **Click a row** to toggle ☐ → ☑ (checked).
3. **Second click on the button** (now labeled "Confirm Delete Checked") — permanently removes all checked items.

If items are already selected (highlighted) when you click **🗑️ Delete Selected**, they are deleted immediately without checklist mode.

### 7. Calculating the Optimal Strategy

1. Ensure you've set a **max weight** and added at least **one food item**.
2. Click the **🚀 CALCULATE OPTIMAL STRATEGY** button.
3. The app runs the knapsack algorithm and:
   - Displays a **pie chart** on the right panel showing the optimal allocation of servings.
   - Shows a green toast: ✅ *"Optimal strategy calculated!"*

### 8. Understanding the Pie Chart

The pie chart visualizes how many servings of each food item you should eat. Each slice is labeled with the food name and the exact serving count. This chart is generated using `matplotlib` and saved as `src/ui/graph.png`.

---

## Core Algorithm: Greedy Fractional Knapsack

Located in `src/core/knapsack.py`, the `run_knapsack()` function implements a **greedy algorithm**:

### Steps

1. **Build candidates** — For each food item, compute:
   - `value_per_gram = value_per_serving / serving_size`
   - `max_weight_allowed = tolerance × serving_size`

2. **Sort by ratio** — Sort all items in **descending order** of value-per-gram (best value first).

3. **Greedy selection** — Iterate through sorted items:
   - Take as much as possible of the current item (up to its max tolerance or remaining capacity).
   - Support **partial servings** (fractional knapsack) — if only part of a serving fits, take that fraction.
   - Track weight taken, value gained, and whether the serving is partial.

4. **Return result** — A dictionary with:
   - `allocations` — list of `{name, servings_taken, weight_taken, value_gained, is_partial}`
   - `total_value` — sum of all value gained
   - `total_weight` — sum of all weight consumed

### Why Greedy?

The fractional knapsack problem has the **optimal substructure** property — a greedy approach by value-to-weight ratio guarantees an optimal solution (unlike 0/1 knapsack, which requires dynamic programming).

---

## Data Layer

Located in `src/core/db.py`, the "database" is an **in-memory Python dictionary**:

```python
food_items_db = {
    "Adobo": {
        "serving_size": 300.0,
        "value_serving": 200.0,
        "tolerance": 2.0
    },
    ...
}
max_consumable_weight = 0.0  # global max weight
```

Functions: `add_food_item()`, `delete_food()`, `get_all_food()`, `update_food_item()`, `set_max_weight()`, `get_max_weight()`.

> ⚠️ **Note:** Data is not persisted to disk — it resets when the app closes.

---

## Graph Generation

Located in `src/core/graph.py`, the `get_graph()` function:
1. Extracts food names and serving counts from the knapsack result.
2. Creates a **pie chart** using `matplotlib`.
3. Saves it as `src/ui/graph.png` (overwrites previous chart).
4. The UI then loads this image and displays it on a `tk.Canvas`.

---

## Toast Notification System

The `show_toast()` function in `src/ui/helpers.py` creates a temporary overlay window:
- Appears centered on screen
- Auto-dismisses after 2.5 seconds
- Color-coded: 🟢 green for success, 🔴 red for errors/warnings

---

## Testing

A standalone test script is available at `src/test.py`. It tests:
- **Knapsack solver** — with sample food items (Apple, Bread, Cheese, Cake)
- **Graph generation** — with Filipino dishes (Adobo, Sinigang, Rice)

Run it with:

```bash
python src/test.py
```

---

## Summary of Key Files

| File                    | Role                                      |
|-------------------------|-------------------------------------------|
| `src/main.py`           | Application entry point                   |
| `src/ui/main_GUI.py`    | Main window layout, styling, event wiring |
| `src/ui/helpers.py`     | Shared UI functions (toast, table, etc.)  |
| `src/ui/add_item.py`    | Add item form dialog                      |
| `src/ui/edit_item.py`   | Edit item form dialog                     |
| `src/core/knapsack.py`  | Greedy fractional knapsack algorithm      |
| `src/core/db.py`        | In-memory data store                      |
| `src/core/graph.py`     | Pie chart generation                      |
| `src/test.py`           | Test script for core modules              |


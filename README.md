# 🍖 Buffet Value Maximizer

A desktop application built with **Python** and **Tkinter** that helps buffet-goers make smart eating decisions. It applies the **Greedy Fractional Knapsack Algorithm** to determine the optimal combination of food items — maximizing total monetary value (price recovery) while staying within a user-defined stomach capacity.

> Final project for **CMSC 142 — Design and Analysis of Algorithms**.

---

## ✨ Features

- **➕ Add Food Items** — Register buffet dishes with serving size, price, and max tolerance
- **📝 Edit / 🗑️ Delete Items** — Modify or remove food entries with a convenient checklist mode
- **⚖️ Set Max Weight** — Define your stomach capacity in grams
- **🚀 Calculate Optimal Strategy** — Runs the greedy knapsack algorithm to maximize value
- **📊 Pie Chart Visualization** — See your optimal meal allocation at a glance
- **🔔 Toast Notifications** — Color-coded feedback for every action

---

## 🧠 How It Works

Each food item has three properties:

| Property         | Description                                    |
|------------------|------------------------------------------------|
| **Serving Size** | Weight of one serving (in grams)               |
| **Value (Price)**| Cost or price of one serving (e.g., in pesos)  |
| **Tolerance**    | Maximum number of servings you'd eat of it     |

The algorithm:
1. Computes a **price-per-gram** ratio for every item
2. Sorts items from **best to worst** ratio
3. Takes as many servings as possible from the top item (up to its tolerance)
4. Moves to the next item, repeating until your stomach capacity is full

---

## 🏗️ Project Structure

```
src/
├── main.py                 ← Entry point
├── core/
│   ├── db.py               ← In-memory database
│   ├── knapsack.py         ← Greedy fractional knapsack solver
│   └── graph.py            ← Pie chart generator (matplotlib)
└── ui/
    ├── main_GUI.py         ← Main window layout & styling
    ├── helpers.py          ← Shared UI logic
    ├── add_item.py         ← Add item dialog
    └── edit_item.py        ← Edit item dialog
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
pip install matplotlib Pillow
```

### Run the App

```bash
python src/main.py
```

---

## 📖 Walkthrough

For a detailed step-by-step guide covering every screen, feature, and the algorithm in depth, see [`WALKTHROUGH.md`](./WALKTHROUGH.md).

---

## 🧪 Running Tests

```bash
python src/test.py
```

Tests the knapsack solver and graph generator with sample data.

---

## 🛠️ Built With

- **[Python](https://www.python.org/)** — Core language
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)** — GUI framework (built-in)
- **[Matplotlib](https://matplotlib.org/)** — Pie chart rendering
- **[Pillow (PIL)](https://python-pillow.org/)** — Image handling in Tkinter

---

## Members
- Leona Mae Blancaflor
- Julian Medalla
- Kenneth Mondejar
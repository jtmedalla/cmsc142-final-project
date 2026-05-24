import tkinter as tk
from tkinter import ttk

from ui.add_item import open_add_item_window
from core.db import get_all_food_items, delete_food_item_by_name

def start_app_ui():
    root = tk.Tk()
    root.title("Buffet Value Maximizer")
    root.geometry("950x550")
    root.configure(bg="#f8fafc")


    main_container = ttk.Frame(root, padding=20)
    main_container.pack(fill="both", expand=True)

    title_label = ttk.Label(main_container, text="🍲 Buffet Value Maximizer", style="Title.TLabel")
    title_label.pack(anchor="w", pady=(0, 20))

    content_pane = ttk.Frame(main_container)
    content_pane.pack(fill="both", expand=True)

    left_frame = ttk.Frame(content_pane)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

    right_frame = ttk.Frame(content_pane)
    right_frame.pack(side="right", fill="both", padx=(15, 0))

    # Weight Input
    input_sub_frame = ttk.Frame(left_frame)
    input_sub_frame.pack(fill="x", pady=(0, 10))
    ttk.Label(input_sub_frame, text="Max Weight Consumable (g):", style="Header.TLabel").pack(side="left", padx=(0, 10))
    weight_input = ttk.Entry(input_sub_frame, width=15)
    weight_input.pack(side="left", ipady=2)

    # Treeview Table
    table_frame = ttk.Frame(left_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    column_names = ("item_name", "serving_size", "value_serving", "tolerance")
    food_menu = ttk.Treeview(table_frame, columns=column_names, show="headings")
    food_menu.heading("item_name", text="Food Item Name")
    food_menu.heading("serving_size", text="Serving Size (g)")
    food_menu.heading("value_serving", text="Value Per Serving")
    food_menu.heading("tolerance", text="Max Tolerance")
    
    food_menu.pack(side="left", fill="both", expand=True)
    food_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=food_menu.yview)
    food_menu.configure(yscrollcommand=food_scroll.set)
    food_scroll.pack(side="right", fill="y")

    def refresh_table_display():
        """Clears the table and re-draws rows directly from the core dictionary database."""
        for row in food_menu.get_children():
            food_menu.delete(row)
        
        for name, details in get_all_food_items().items():
            food_menu.insert("", "end", values=(
                name, 
                f"{details['serving_size']:g}", 
                f"{details['value_serving']:g}", 
                details["tolerance"]
            ))

    def delete_selected_item():
        """Finds what row is highlighted, drops it from DB in O(1) time, and refreshes UI."""
        selected_items = food_menu.selection()
        for item in selected_items:
            item_values = food_menu.item(item, 'values')
            if item_values:
                food_name = item_values[0]
                delete_food_item_by_name(food_name)
        refresh_table_display()

    # Table Action Buttons
    action_btn_frame = ttk.Frame(left_frame)
    action_btn_frame.pack(fill="x", pady=(10, 0))

    add_item = ttk.Button(
        action_btn_frame, text="➕ Add Food Item", style="Add.TButton",
        command=lambda: open_add_item_window(root, refresh_table_display)
    )
    add_item.pack(side="left", padx=(0, 5), ipady=5, expand=True, fill="x")

    del_item = ttk.Button(action_btn_frame, text="🗑️ Delete Selected", style="Delete.TButton", command=delete_selected_item)
    del_item.pack(side="right", padx=(5, 0), ipady=5, expand=True, fill="x")

    # Right Panel Visualization Placement
    ttk.Label(right_frame, text="Optimal Eating Allocation Strategy", style="Header.TLabel").pack(anchor="w", pady=(0, 8))
    image_display = tk.Canvas(right_frame, width=350, height=350, bg="white", highlightthickness=1, highlightbackground="#cbd5e1", relief="flat")
    image_display.pack(pady=(0, 15))
    image_display.create_text(175, 175, text="Your optimization pie chart\nwill render here.", fill="#94a3b8", font=("Poppins", 10, "italic"), justify="center")

    calculate = ttk.Button(right_frame, text="🚀 CALCULATE OPTIMAL STRATEGY", style="Calculate.TButton")
    calculate.pack(fill="x", ipady=10)
        
    root.mainloop()
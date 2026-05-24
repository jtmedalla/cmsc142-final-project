import tkinter as tk
from tkinter import ttk
from core.db import add_food_item, get_all_food

def open_add_item(parent_root, on_success_callback):
    add_win = tk.Toplevel(parent_root)
    add_win.title("➕ Add New Food Item")

    add_win.configure(bg="#f8fafc")
    
    add_win.transient(parent_root)
    add_win.grab_set()

    form_frame = ttk.Frame(add_win, padding=20)
    form_frame.pack(fill="both", expand=True)

    def create_form_row(label_text, row_num):
        lbl = ttk.Label(form_frame, text=label_text, font=('Segoe UI', 10, 'bold'))
        lbl.grid(row=row_num, column=0, sticky="w", pady=8, padx=(0, 10))
        entry = ttk.Entry(form_frame, width=25)
        entry.grid(row=row_num, column=1, sticky="ew", pady=8)
        return entry

    name_entry = create_form_row("Food Item Name:", 0)
    size_entry = create_form_row("Serving Size (g):", 1)
    value_entry = create_form_row("Value Per Serving:", 2)
    tolerance_entry = create_form_row("Max Tolerance:", 3)

    error_lbl = ttk.Label(form_frame, text="", foreground="#dc2626", font=('Poppins', 9, 'italic'))
    error_lbl.grid(row=4, column=0, columnspan=2, pady=5)

    def save_item():
        name = name_entry.get().strip()
        size_raw = size_entry.get().strip()
        val_raw = value_entry.get().strip()
        tol_raw = tolerance_entry.get().strip()

        # if not name or not size or not val or not tol:
        #     error_lbl.config(text="⚠️ Please fill in all fields.")
        #     return

        if not name:
            error_lbl.config(text="⚠️ Food Item Name cannot be empty.")
            return

        # Rule 2: Prevent duplicate items (O(1) lookups on your dictionary database!)
        if name in get_all_food():
            error_lbl.config(text=f"⚠️ '{name}' already exists in the menu.")
            return
        
        try:
            serving_size = float(size_raw)
            if serving_size <= 0:
                error_lbl.config(text="⚠️ Serving Size must be greater than 0.")
                return
        except ValueError:
            error_lbl.config(text="⚠️ Serving Size must be a valid number.")
            return

        # Rule 4: Validate Value Per Serving
        try:
            value_serving = float(val_raw)
            if value_serving <= 0:
                error_lbl.config(text="⚠️ Value Per Serving must be greater than 0.")
                return
        except ValueError:
            error_lbl.config(text="⚠️ Value Per Serving must be a valid number.")
            return

        # Rule 5: Validate Max Tolerance
        try:
            tolerance = float(tol_raw)
            if tolerance <= 0:
                error_lbl.config(text="⚠️ Max Tolerance must be greater than 0.")
                return
        except ValueError:
            error_lbl.config(text="⚠️ Max Tolerance must be a valid number.")
            return
        
        add_food_item(name, serving_size, value_serving, tolerance)
        on_success_callback()
        add_win.destroy()

        
        # try:
        #     add_food_item(name, size, val, tol)
        #     on_success_callback()
        #     add_win.destroy()
        # except ValueError:
        #     error_lbl.config(text="⚠️ Size/Value/Tolerance must be valid numbers.")

    save_btn = ttk.Button(form_frame, text="Save Item", style="Calculate.TButton", command=save_item)
    save_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0), ipady=5)

    add_win.update()

    popup_width = add_win.winfo_width()
    popup_height = add_win.winfo_height()
    
    screen_width = add_win.winfo_screenwidth()
    screen_height = add_win.winfo_screenheight()
    
    center_x = int((screen_width - popup_width) / 2)
    center_y = int((screen_height - popup_height) / 2)
    
    add_win.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
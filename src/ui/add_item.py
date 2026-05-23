import tkinter as tk
from tkinter import ttk
from core.db import add_food_item

def open_add_item(parent_root, on_success_callback):
    add_win = tk.Toplevel(parent_root)
    add_win.title("➕ Add New Food Item")
    add_win.geometry("400x320")
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

    error_lbl = ttk.Label(form_frame, text="", foreground="#dc2626", font=('Segoe UI', 9, 'italic'))
    error_lbl.grid(row=4, column=0, columnspan=2, pady=5)

    def save_item():
        name = name_entry.get().strip()
        size = size_entry.get().strip()
        val = value_entry.get().strip()
        tol = tolerance_entry.get().strip()

        if not name or not size or not val or not tol:
            error_lbl.config(text="⚠️ Please fill in all fields.")
            return
        
        try:
            add_food_item(name, size, val, tol)
            on_success_callback()
            add_win.destroy()
        except ValueError:
            error_lbl.config(text="⚠️ Size/Value/Tolerance must be valid numbers.")

    save_btn = ttk.Button(form_frame, text="Save Item", style="Calculate.TButton", command=save_item)
    save_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0), ipady=5)
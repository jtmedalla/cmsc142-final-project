import tkinter as tk
from tkinter import ttk
from core.db import update_food_item, get_all_food

def open_edit_item(parent_root, old_name, current_details, on_success_callback):
    edit_win = tk.Toplevel(parent_root)
    edit_win.title(f"✏️ Edit Food Item: {old_name}")
    edit_win.configure(bg="#f8fafc")
    
    edit_win.transient(parent_root)
    edit_win.grab_set()

    form_frame = ttk.Frame(edit_win, padding=20)
    form_frame.pack(fill="both", expand=True)

    def create_form_row(label_text, row_num, default_value=""):
        lbl = ttk.Label(form_frame, text=label_text, font=('Segoe UI', 10, 'bold'))
        lbl.grid(row=row_num, column=0, sticky="w", pady=8, padx=(0, 10))
        entry = ttk.Entry(form_frame, width=25)
        entry.insert(0, str(default_value))  
        entry.grid(row=row_num, column=1, sticky="ew", pady=8)
        return entry

    name_entry = create_form_row("Food Item Name:", 0, old_name)
    size_entry = create_form_row("Serving Size (g):", 1, f"{current_details['serving_size']:g}")
    value_entry = create_form_row("Value Per Serving:", 2, f"{current_details['value_serving']:g}")
    tolerance_entry = create_form_row("Max Tolerance:", 3, f"{current_details['tolerance']:g}")

    error_lbl = ttk.Label(form_frame, text="", foreground="#dc2626", font=('Segoe UI', 9, 'italic'))
    error_lbl.grid(row=4, column=0, columnspan=2, pady=5)

    def save_changes():
        name = name_entry.get().strip()
        size_raw = size_entry.get().strip()
        val_raw = value_entry.get().strip()
        tol_raw = tolerance_entry.get().strip()

        if not name:
            error_lbl.config(text="⚠️ Food Item Name cannot be empty.")
            return

        if name != old_name and name in get_all_food():
            error_lbl.config(text=f"⚠️ An item named '{name}' already exists.")
            return

        try:
            serving_size = float(size_raw)
            if serving_size <= 0:
                error_lbl.config(text="⚠️ Serving Size must be greater than 0.")
                return
        except ValueError:
            error_lbl.config(text="⚠️ Serving Size must be a valid number.")
            return

        try:
            value_serving = float(val_raw)
            if value_serving <= 0:
                error_lbl.config(text="⚠️ Value Per Serving must be greater than 0.")
                return
        except ValueError:
            error_lbl.config(text="⚠️ Value Per Serving must be a valid number.")
            return

        try:
            tolerance = float(tol_raw)
            if tolerance <= 0:
                error_lbl.config(text="⚠️ Max Tolerance must be greater than 0.")
                return
        except ValueError:
            error_lbl.config(text="⚠️ Max Tolerance must be a valid number.")
            return

        update_food_item(old_name, name, serving_size, value_serving, tolerance)
        on_success_callback()
        edit_win.destroy()

    save_btn = ttk.Button(form_frame, text="Save Changes", style="Calculate.TButton", command=save_changes)
    save_btn.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0), ipady=5)

    edit_win.update()
    popup_width = edit_win.winfo_width()
    popup_height = edit_win.winfo_height()
    screen_width = edit_win.winfo_screenwidth()
    screen_height = edit_win.winfo_screenheight()
    
    center_x = int((screen_width - popup_width) / 2)
    center_y = int((screen_height - popup_height) / 2)
    edit_win.geometry(f"{popup_width}x{popup_height}+{center_x}+{center_y}")
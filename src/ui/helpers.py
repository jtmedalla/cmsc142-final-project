import tkinter as tk
from tkinter import ttk

from ui.edit_item import open_edit_item

from core.db import get_all_food, delete_food, get_max_weight, set_max_weight
from core.knapsack import run_knapsack

def show_toast(root, message, bg_color="#0f172a"):
    toast = tk.Toplevel(root)
    toast.wm_overrideredirect(True)
    toast.configure(bg=bg_color)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    toast_width, toast_height = 320, 42
    x = (screen_width - toast_width) // 2
    y = (screen_height - toast_height) // 2
    toast.geometry(f"{toast_width}x{toast_height}+{x}+{y}")
    toast.attributes("-topmost", True)
    lbl = tk.Label(
        toast, text=message, fg="white", bg=bg_color, font=("Poppins", 10, "bold")
    )
    lbl.pack(expand=True, fill="both", padx=10, pady=5)
    toast.after(2500, toast.destroy)


def render_weight_input(root, weight_container, show_toast, force_edit=False):
    for widget in weight_container.winfo_children():
        widget.destroy()

    current_weight = get_max_weight()

    if current_weight == 0.0 or force_edit:
        weight_entry = ttk.Entry(weight_container, width=15)

        if current_weight > 0:
            weight_entry.insert(0, f"{current_weight:g}")

        weight_entry.pack(side="left", ipady=2)

        def save_weight():
            raw_val = weight_entry.get().strip()

            try:
                val = float(raw_val)
                if val <= 0:
                    show_toast(
                        root, "⚠️ Weight must be greater than 0.", bg_color="#dc2626"
                    )
                    return
                is_update = current_weight > 0
                set_max_weight(val)
                msg = (
                    f"✅ Max weight updated to {val}g"
                    if is_update
                    else f"✅ Max weight set to {val}g"
                )
                show_toast(root, msg, bg_color="#16a34a")
                render_weight_input(root, weight_container, show_toast)
            except ValueError:
                show_toast(root, "⚠️ Valid number required.", bg_color="#dc2626")

        btn_text = "Update" if force_edit and current_weight > 0 else "Set"
        ttk.Button(
            weight_container, text=btn_text, style="Add.TButton", command=save_weight
        ).pack(side="left", padx=(10, 0))
    else:
        ttk.Label(
            weight_container, text=f"{current_weight:g} g", font=("Poppins", 12, "bold")
        ).pack(side="left")
        ttk.Button(
            weight_container,
            text="✏️ Edit",
            style="Edit.TButton",
            command=lambda: render_weight_input(
                root, weight_container, show_toast, force_edit=True
            ),
        ).pack(side="left", padx=(10, 0))


def refresh_table_display(
    root, food_menu, del_item, show_toast, toast_msg=None, is_error=False
):
    for row in food_menu.get_children():
        food_menu.delete(row)

    for name, details in get_all_food().items():
        food_menu.insert(
            "",
            "end",
            values=(
                name,
                f"{details['serving_size']:g}",
                f"{details['value_serving']:g}",
                details["tolerance"],
            ),
        )
    food_menu.checklist_mode = False
    del_item.config(text="🗑️ Delete Selected")
    if toast_msg:
        color = "#dc2626" if is_error else "#16a34a"
        show_toast(root, toast_msg, bg_color=color)


def delete_selected_item(root, food_menu, del_item, show_toast, refresh):
    selected_items = food_menu.selection()

    if selected_items:
        deleted_names = []

        for item in selected_items:
            item_values = food_menu.item(item, "values")
            if item_values:
                food_name = item_values[0]
                delete_food(food_name)
                deleted_names.append(food_name)
        msg = (
            f"Deleted {len(deleted_names)} item(s)"
            if len(deleted_names) > 1
            else f"Removed '{deleted_names[0]}'"
        )
        refresh(root, food_menu, del_item, show_toast, toast_msg=msg, is_error=True)
        return

    if not getattr(food_menu, "checklist_mode", False):
        food_menu.checklist_mode = True
        del_item.config(text="Confirm Delete Checked")

        for item in food_menu.get_children():
            current_vals = list(food_menu.item(item, "values"))

            if current_vals and not current_vals[0].startswith(("☐ ", "☑ ")):
                current_vals[0] = "☐ " + current_vals[0]
                food_menu.item(item, values=current_vals)
    else:
        checked_count = 0

        for item in food_menu.get_children():
            current_vals = list(food_menu.item(item, "values"))

            if current_vals and current_vals[0].startswith("☑ "):
                food_name = current_vals[0].replace("☑ ", "", 1)
                delete_food(food_name)
                checked_count += 1
        food_menu.checklist_mode = False
        del_item.config(text="Delete Selected")
        msg = f"Deleted {checked_count} item(s)" if checked_count > 0 else None
        refresh(root, food_menu, del_item, show_toast, toast_msg=msg, is_error=True)


def toggle_treeview_checkbox(event, food_menu):
    if getattr(food_menu, "checklist_mode", False):
        item = food_menu.identify_row(event.y)

        if item:
            current_vals = list(food_menu.item(item, "values"))

            if current_vals:

                if current_vals[0].startswith("☐ "):
                    current_vals[0] = current_vals[0].replace("☐ ", "☑ ", 1)
                elif current_vals[0].startswith("☑ "):
                    current_vals[0] = current_vals[0].replace("☑ ", "☐ ", 1)

                food_menu.item(item, values=current_vals)

            food_menu.selection_remove(item)


def edit_selected_item(root, food_menu, refresh):
    selected_items = food_menu.selection()

    if not selected_items:
        return

    item = selected_items[0]
    item_values = food_menu.item(item, "values")

    if item_values:
        food_name = item_values[0]
        all_food = get_all_food()
        if food_name in all_food:
            open_edit_item(root, food_name, all_food[food_name], refresh)

def on_calculate(root, summary_var, show_toast):
    max_w = get_max_weight()
    all_food = get_all_food()

    if max_w <= 0:
        show_toast(root, "⚠️ Please set your max consumable weight first.", bg_color="#dc2626")
        return
    if not all_food:
        show_toast(root, "⚠️ Please add at least one food item.", bg_color="#dc2626")
        return

    result = run_knapsack(max_w, all_food)

    if not result["allocations"]:
        show_toast(root, "⚠️ No valid food items to optimise.", bg_color="#dc2626")
        return

    total_v = result["total_value"]
    total_w = result["total_weight"]
    n_items = len(result["allocations"])

    # build chosen items
    chosen_lines = []
    for alloc in result["allocations"]:
        line = f"{alloc['name']} → {alloc['servings_taken']} serving(s), {alloc['weight_taken']} g, value {alloc['value_gained']} /n"
        chosen_lines.append(line)

    # breakdwon
    summary_text = (
        f"🍽 {n_items} item(s) | {total_w:g} g eaten | Total value: {total_v:g}\n"
        + "\n".join(chosen_lines)
    )

    summary_var.set(summary_text)
    show_toast(root, "✅ Optimal strategy calculated!", bg_color="#16a34a")
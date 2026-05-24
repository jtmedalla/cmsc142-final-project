import tkinter as tk
from tkinter import ttk

from ui.add_item import open_add_item
from core.db import get_all_food, delete_food
from ui.edit_item import open_edit_item

# initializations

def start_app_ui():
    root = tk.Tk()
    root.title("Buffet Value Maximizer")

    window_width = 950
    window_height = 550
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate perfect center coordinates
    center_x = int((screen_width - window_width) / 2)
    center_y = int((screen_height - window_height) / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    root.configure(bg="#000000")  

    style = ttk.Style()
    style.theme_use('clam')  

    BG_COLOR = "#abccec"       
    BLUE = "#0f172a"  
    GREEN = "#16a34a"  
    RED = "#dc2626"     
    LELLOW = "#BABD37"

    style.configure('TFrame', background=BG_COLOR)

    # Typography
    style.configure('TLabel', background=BG_COLOR, foreground=BLUE, font=('Poppins', 10))
    style.configure('Title.TLabel', font=('Poppins', 18, 'bold'), foreground=BLUE)
    style.configure('Header.TLabel', font=('Poppins', 12, 'bold'), foreground=BLUE)

    # Entry Fields
    style.configure('TEntry', fieldbackground="white", padding=5)

    # Buttons
    style.configure('Add.TButton', background=BLUE, foreground="white", font=('Poppins', 10, 'bold'), borderwidth=0)
    style.map('Add.TButton', background=[('active', "#0e1e46")])

    style.configure('Delete.TButton', background=RED, foreground="white", font=('Poppins', 10, 'bold'), borderwidth=0)
    style.map('Delete.TButton', background=[('active', "#eb1616")])

    style.configure('Edit.TButton', background=LELLOW, foreground="white", font=('Poppins', 10, 'bold'), borderwidth=0)
    style.map('Edit.TButton', background=[('active', "#DCDF35")])

    style.configure('Calculate.TButton', background=GREEN, foreground="white", font=('Poppins', 12, 'bold'), borderwidth=0)
    style.map('Calculate.TButton', background=[('active', '#15803d')])

    style.configure("Treeview", font=('Poppins', 10), rowheight=25, background="white", fieldbackground="white")
    style.configure("Treeview.Heading", font=('Poppins', 10, 'bold'), background="#e2e8f0", foreground=BLUE, relief="flat")
    style.map("Treeview.Heading", background=[('active', '#cbd5e1')])

    # Main container padding
    main_container = ttk.Frame(root, padding=20)
    main_container.pack(fill="both", expand=True)

    # Top Title Block
    title_label = ttk.Label(main_container, text="Buffet Value Maximizer 🍖♨️", style="Title.TLabel")
    title_label.pack(anchor="w", pady=(0, 20))

    # Two-Column Split Content Pane
    content_pane = ttk.Frame(main_container)
    content_pane.pack(fill="both", expand=True)

    left_frame = ttk.Frame(content_pane)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

    right_frame = ttk.Frame(content_pane)
    right_frame.pack(side="right", fill="both", padx=(15, 0))

    # Weight Input Section
    input_sub_frame = ttk.Frame(left_frame)
    input_sub_frame.pack(fill="x", pady=(0, 10))

    weight_label = ttk.Label(input_sub_frame, text="Max Weight Consumable (g):", style="Header.TLabel")
    weight_label.pack(side="left", padx=(0, 10))

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

    # Explicitly column sizing for visual balance
    food_menu.column("item_name", width=150, anchor="w")
    food_menu.column("serving_size", width=110, anchor="center")
    food_menu.column("value_serving", width=120, anchor="center")
    food_menu.column("tolerance", width=100, anchor="center")

    food_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=food_menu.yview)
    food_menu.configure(yscrollcommand=food_scroll.set)

    food_menu.pack(side="left", fill="both", expand=True)
    food_scroll.pack(side="right", fill="y")


    def refresh_table_display(toast_msg=None, is_error=False):
        """Clears the visual table and populates rows from the dictionary database."""
        for row in food_menu.get_children():
            food_menu.delete(row)
        
        # Pull items out of dictionary fast
        for name, details in get_all_food().items():
            food_menu.insert("", "end", values=(
                name, 
                f"{details['serving_size']:g}", 
                f"{details['value_serving']:g}", 
                details["tolerance"]
            ))
        
        food_menu.checklist_mode = False
        del_item.config(text="🗑️ Delete Selected")

        if toast_msg:
            color = RED if is_error else GREEN
            show_toast(root, toast_msg, bg_color=color)

    def show_toast(root, message, bg_color="#0f172a"):
        toast = tk.Toplevel(root)
        toast.wm_overrideredirect(True)  
        toast.configure(bg=bg_color)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        toast_width = 320
        toast_height = 42
        
        x = (screen_width - toast_width) // 2
        y = (screen_height - toast_height) // 2
        
        toast.geometry(f"{toast_width}x{toast_height}+{x}+{y}")
        toast.attributes("-topmost", True)
        
        lbl = tk.Label(toast, text=message, fg="white", bg=bg_color, font=('Poppins', 10, 'bold'))
        lbl.pack(expand=True, fill="both", padx=10, pady=5)
        
        toast.after(2500, toast.destroy)

    def delete_selected_item():
        """2 states will happened here if the user tap "Delete Button
                -> 1. If no 'highlighted items' checkbox will appear 
                    [user can delete multiple food items at the same time]
                -> 2. If merong na 'highlight' na food, after pressing the
                    delete button, it will be automatically deleted.
        """
        selected_items = food_menu.selection()

        if selected_items:
            for item in selected_items:
                item_values = food_menu.item(item, 'values')
                if item_values:
                    food_name = item_values[0]
                    delete_food(food_name)
            refresh_table_display()
            return
        
        if not food_menu.checklist_mode:
            food_menu.checklist_mode = True
            del_item.config(text="Confirm Delete Checked") 
            
            for item in food_menu.get_children():
                current_vals = list(food_menu.item(item, 'values'))
                if current_vals and not current_vals[0].startswith(("☐ ", "☑ ")):
                    current_vals[0] = "☐ " + current_vals[0]
                    food_menu.item(item, values=current_vals)
        else:
            checked_count = 0
            for item in food_menu.get_children():
                current_vals = list(food_menu.item(item, 'values'))
                if current_vals and current_vals[0].startswith("☑ "):
                    food_name = current_vals[0].replace("☑ ", "", 1)
                    delete_food(food_name)
                    checked_count += 1
            
            food_menu.checklist_mode = False
            del_item.config(text="🗑️ Delete Selected")
            refresh_table_display()

    def toggle_treeview_checkbox(event):
        if getattr(food_menu, 'checklist_mode', False):
            item = food_menu.identify_row(event.y)
            if item:
                current_vals = list(food_menu.item(item, 'values'))
                if current_vals:
                    # Flip the checkbox state
                    if current_vals[0].startswith("☐ "):
                        current_vals[0] = current_vals[0].replace("☐ ", "☑ ", 1)
                    elif current_vals[0].startswith("☑ "):
                        current_vals[0] = current_vals[0].replace("☑ ", "☐ ", 1)
                    
                    food_menu.item(item, values=current_vals)
                
                food_menu.selection_remove(item)

    # Attach the click-release trigger to the treeview
    food_menu.bind("<ButtonRelease-1>", toggle_treeview_checkbox)

    def edit_selected_item():
        selected_items = food_menu.selection()
        if not selected_items:
            return  
        
        item = selected_items[0]
        item_values = food_menu.item(item, 'values')
        if item_values:
            food_name = item_values[0]
            all_food = get_all_food()
            
            if food_name in all_food:
                open_edit_item(root, food_name, all_food[food_name], refresh_table_display)

    # Table Action Buttons
    action_btn_frame = ttk.Frame(left_frame)
    action_btn_frame.pack(fill="x", pady=(10, 0))

    add_item = ttk.Button(action_btn_frame, text="➕ Add Food Item", style="Add.TButton",
                          command=lambda: open_add_item(root, refresh_table_display)
                          )
    add_item.pack(side="left", padx=(0, 5), ipady=5, expand=True, fill="x")

    edit_item_btn = ttk.Button(action_btn_frame, text="📝 Edit Selected", style="Edit.TButton",
                               command=edit_selected_item)
    edit_item_btn.pack(side="left", padx=2, ipady=5, expand=True, fill="x")

    del_item = ttk.Button(action_btn_frame, text="🗑️ Delete Selected", style="Delete.TButton",
                          command=delete_selected_item)
    del_item.pack(side="right", padx=(5, 0), ipady=5, expand=True, fill="x")


    ttk.Label(right_frame, text="Optimal Eating Allocation Strategy", style="Header.TLabel").pack(anchor="w", pady=(0, 8))

    image_display = tk.Canvas(right_frame, width=350, height=350, bg="white", highlightthickness=1, highlightbackground="#cbd5e1", relief="flat")
    image_display.pack(pady=(0, 15))

    image_display.create_text(175, 175, text="Your optimization pie chart\nwill render here.", fill="#94a3b8", font=("Poppins", 10, "italic"), justify="center")

    calculate = ttk.Button(right_frame, text="🚀 CALCULATE OPTIMAL STRATEGY", style="Calculate.TButton")
    calculate.pack(fill="x", ipady=10)
        
    root.mainloop()
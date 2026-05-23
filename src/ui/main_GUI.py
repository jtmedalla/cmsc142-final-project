import tkinter as tk
from tkinter import ttk

# initializations

def start_app_ui():
    root = tk.Tk()
    root.title("Buffet Value Maximizer")
    root.geometry("950x550")  
    root.configure(bg="#000000")  

    style = ttk.Style()
    style.theme_use('clam')  

    BG_COLOR = "#abccec"       
    BLUE = "#0f172a"  
    GREEN = "#16a34a"  
    RED = "#dc2626"     

    style.configure('TFrame', background=BG_COLOR)

    # Typography
    style.configure('TLabel', background=BG_COLOR, foreground=BLUE, font=('Poppins', 10))
    style.configure('Title.TLabel', font=('Poppins', 18, 'bold'), foreground=BLUE)
    style.configure('Header.TLabel', font=('Poppins', 12, 'bold'), foreground=BLUE)

    # Entry Fields
    style.configure('TEntry', fieldbackground="white", padding=5)

    # Buttons
    style.configure('Add.TButton', background=BLUE, foreground="white", font=('Poppins', 10, 'bold'), borderwidth=0)
    style.map('Add.TButton', background=[('active', '#1e293b')])

    style.configure('Delete.TButton', background="#ef4444", foreground="white", font=('Poppins', 10, 'bold'), borderwidth=0)
    style.map('Delete.TButton', background=[('active', '#dc2626')])

    style.configure('Calculate.TButton', background=GREEN, foreground="white", font=('Poppins', 12, 'bold'), borderwidth=0)
    style.map('Calculate.TButton', background=[('active', '#15803d')])

    # Treeview Styling
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

    # Table Action Buttons
    action_btn_frame = ttk.Frame(left_frame)
    action_btn_frame.pack(fill="x", pady=(10, 0))

    add_item = ttk.Button(action_btn_frame, text="➕ Add Food Item", style="Add.TButton")
    add_item.pack(side="left", padx=(0, 5), ipady=5, expand=True, fill="x")

    del_item = ttk.Button(action_btn_frame, text="🗑️ Delete Selected", style="Delete.TButton")
    del_item.pack(side="right", padx=(5, 0), ipady=5, expand=True, fill="x")


    ttk.Label(right_frame, text="Optimal Eating Allocation Strategy", style="Header.TLabel").pack(anchor="w", pady=(0, 8))

    image_display = tk.Canvas(right_frame, width=350, height=350, bg="white", highlightthickness=1, highlightbackground="#cbd5e1", relief="flat")
    image_display.pack(pady=(0, 15))

    image_display.create_text(175, 175, text="Your optimization pie chart\nwill render here.", fill="#94a3b8", font=("Poppins", 10, "italic"), justify="center")

    calculate = ttk.Button(right_frame, text="🚀 CALCULATE OPTIMAL STRATEGY", style="Calculate.TButton")
    calculate.pack(fill="x", ipady=10)
        
    root.mainloop()
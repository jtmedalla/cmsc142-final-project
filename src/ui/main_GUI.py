import tkinter as tk
from tkinter import ttk

from ui.add_item import open_add_item
from ui.helpers import (
    show_toast,
    render_weight_input,
    refresh_table_display,
    delete_selected_item,
    toggle_treeview_checkbox,
    edit_selected_item,
    on_calculate,
)

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
    style.theme_use("clam")

    BG_COLOR = "#abccec"
    BLUE = "#0f172a"
    GREEN = "#16a34a"
    RED = "#dc2626"
    LELLOW = "#BABD37"
    SLATE = "#000511"

    style.configure("TFrame", background=BG_COLOR)

    # Typography
    style.configure(
        "TLabel", background=BG_COLOR, foreground=BLUE, font=("Poppins", 10)
    )
    style.configure("Title.TLabel", font=("Poppins", 18, "bold"), foreground=BLUE)
    style.configure("Header.TLabel", font=("Poppins", 12, "bold"), foreground=BLUE)

    # Entry Fields
    style.configure("TEntry", fieldbackground="white", padding=5)

    # Buttons
    style.configure(
        "Add.TButton",
        background=BLUE,
        foreground="white",
        font=("Poppins", 10, "bold"),
        borderwidth=0,
    )
    style.map("Add.TButton", background=[("active", "#0e1e46")])

    style.configure(
        "Delete.TButton",
        background=RED,
        foreground="white",
        font=("Poppins", 10, "bold"),
        borderwidth=0,
    )
    style.map("Delete.TButton", background=[("active", "#eb1616")])

    style.configure(
        "Edit.TButton",
        background=LELLOW,
        foreground="white",
        font=("Poppins", 10, "bold"),
        borderwidth=0,
    )
    style.map("Edit.TButton", background=[("active", "#DCDF35")])

    style.configure(
        "Calculate.TButton",
        background=GREEN,
        foreground="white",
        font=("Poppins", 12, "bold"),
        borderwidth=0,
    )
    style.map("Calculate.TButton", background=[("active", "#15803d")])

    style.configure(
        "Treeview",
        font=("Poppins", 10),
        rowheight=25,
        background="white",
        fieldbackground="white",
    )
    style.configure(
        "Treeview.Heading",
        font=("Poppins", 10, "bold"),
        background="#e2e8f0",
        foreground=BLUE,
        relief="flat",
    )
    style.map("Treeview.Heading", background=[("active", "#cbd5e1")])

    # Main container padding
    main_container = ttk.Frame(root, padding=20)
    main_container.pack(fill="both", expand=True)

    # Top Title Block
    title_label = ttk.Label(
        main_container, text="Buffet Value Maximizer 🍖♨️", style="Title.TLabel"
    )
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

    weight_label = ttk.Label(
        input_sub_frame, text="Max Weight Consumable (g):", style="Header.TLabel"
    )
    weight_label.pack(side="left", padx=(0, 10))

    weight_container = ttk.Frame(input_sub_frame)
    weight_container.pack(side="left", fill="x", expand=True)

    render_weight_input(root, weight_container, show_toast)

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

    # Attach the click-release trigger to the treeview
    food_menu.bind(
        "<ButtonRelease-1>", lambda e: toggle_treeview_checkbox(e, food_menu)
    )

    # Buttons
    action_btn_frame = ttk.Frame(left_frame)
    action_btn_frame.pack(fill="x", pady=(10, 0))

    add_item = ttk.Button(
        action_btn_frame,
        text="➕ Add Food Item",
        style="Add.TButton",
        command=lambda: open_add_item(
            root,
            lambda msg=None, err=False: refresh_table_display(
                root, food_menu, del_item, show_toast, msg, err
            ),
        ),
    )
    add_item.pack(side="left", padx=(0, 5), ipady=5, expand=True, fill="x")

    edit_item_btn = ttk.Button(
        action_btn_frame,
        text="📝 Edit Selected",
        style="Edit.TButton",
        command=lambda: edit_selected_item(
            root,
            food_menu,
            lambda msg=None, err=False: refresh_table_display(
                root, food_menu, del_item, show_toast, msg, err
            ),
        ),
    )
    edit_item_btn.pack(side="left", padx=2, ipady=5, expand=True, fill="x")

    del_item = ttk.Button(
        action_btn_frame,
        text="🗑️ Delete Selected",
        style="Delete.TButton",
        command=lambda: delete_selected_item(
            root, food_menu, del_item, show_toast, refresh_table_display
        ),
    )
    del_item.pack(side="right", padx=(5, 0), ipady=5, expand=True, fill="x")

    ttk.Label(
        right_frame, text="Optimal Eating Allocation Strategy", style="Header.TLabel"
    ).pack(anchor="w", pady=(0, 8))
    image_display = tk.Canvas(
        right_frame,
        width=350,
        height=350,
        bg="white",
        highlightthickness=1,
        highlightbackground="#cbd5e1",
        relief="flat",
    )
    image_display.pack(pady=(0, 15))
    image_display.create_text(
        175,
        175,
        text="Your optimization pie chart\nwill render here.",
        fill="#94a3b8",
        font=("Poppins", 10, "italic"),
        justify="center",
    )

    # right pannel summary
    summary_var = tk.StringVar(value="")
    summary_lbl = ttk.Label(right_frame, textvariable=summary_var, style="TLabel")
    summary_lbl.pack(anchor="center", pady=(0, 8))

    calculate = ttk.Button(
        right_frame,
        text="🚀 CALCULATE OPTIMAL STRATEGY",
        style="Calculate.TButton",
        command=lambda: on_calculate(root, summary_var, show_toast),
    )
    calculate.pack(fill="x", ipady=10)

    root.mainloop()

    root.mainloop()

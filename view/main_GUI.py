import tkinter as tk
from tkinter import ttk

# initializations

root = tk.Tk()
root.title("Buffet Value Maximizer")
frm = ttk.Frame(root, padding=10)
frm.grid()

# title 
ttk.Label(frm, text="Buffet Value Maximizer").grid(column=0, row=0, columnspan=2, pady=2)

# user input
ttk.Label(frm, text="Max Weight Consumable:").grid(column=0, row=1, pady=2)
weight_input = ttk.Entry(frm)
weight_input.grid(row=1, column=1, pady=2, sticky="ew")

# food list display
column_names = ("item_name", "serving_size", "value_serving", "tolerance")
food_menu = ttk.Treeview(frm, columns=column_names, show="headings")
food_menu.grid(row=2, column=0, rowspan=2, columnspan=2, padx=5, pady=5)

# food list headers
food_menu.heading("item_name", text="Food Item Name")
food_menu.heading("serving_size", text="Serving Size (g)")
food_menu.heading("value_serving", text="Value Per Serving")
food_menu.heading("tolerance", text="Tolerance")

# food_list scrollbar
food_scroll = ttk.Scrollbar(frm, orient="vertical", command=food_menu.yview)
food_scroll.grid(row=2, column=2, rowspan=2, sticky="ns")
food_menu.configure(xscrollcommand=food_scroll.set)

# pie chart image display
image_display = tk.Canvas(frm, borderwidth=2, relief='sunken')
image_display.grid(row=0, column=3, rowspan=4, columnspan=2, pady=5, padx=5)

# add item button
add_item = ttk.Button(frm, text="Add Item")
add_item.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

# delete item button
del_item = ttk.Button(frm, text="Delete Item")
del_item.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

# calculate button
calculate = ttk.Button(frm, text="CALCULATE")
calculate.grid(row=4, column=3, columnspan=2, pady=5, sticky="nsew")
    
root.mainloop()
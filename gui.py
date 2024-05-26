import tkinter as tk
from tkinter import ttk
import random
import time
from main import *
from utils import *


class Business:
    def __init__(self, name, address, category, status, phone_number, reviews_count, rating, latitude, longitude):
        self.name = name
        self.address = address
        self.category = category
        self.status = status
        self.phone_number = phone_number
        self.reviews_count = reviews_count
        self.rating = rating
        self.latitude = latitude
        self.longitude = longitude


global_results = []


def start_search():
    global global_results
    search_for = search_entry.get()
    result_count = result_count_entry.get()
    if not search_for:
        return
    if not result_count:
        return
    try:
        total = int(result_count)
    except ValueError:
        return
    results = perform_search(search_for, total)
    global_results = results
    display_results(results)


def display_results(results):
    for row in result_tree.get_children():
        result_tree.delete(row)
    for idx, result in enumerate(results):
        result_tree.insert(
            "",
            index=tk.END,
            text=str(idx + 1),
            values=(
                result.name,
                result.address,
                result.category,
                result.status,
                result.phone_number,
                result.reviews_count,
                result.rating,
                f"{result.latitude}, {result.longitude}",
                "更多資料",
                "查看評論",
                "路程"
            )
        )


def sort_treeview():
    global global_results
    sort_by = sort_var.get()
    if sort_by == "路程":
        global_results.sort(key=lambda x: (x.latitude, x.longitude))
    elif sort_by == "店名":
        global_results.sort(key=lambda x: x.name)
    elif sort_by == "評分":
        global_results.sort(key=lambda x: float(x.rating), reverse=True)
    display_results(global_results)


def show_more_info(event):
    selected_item = result_tree.focus()
    if selected_item:
        col = result_tree.identify_column(event.x)
        if col == '#9':  # '更多資料' column
            item_values = result_tree.item(selected_item, "values")
            open_more_info_window(item_values)
        elif col == '#10':  # '查看評論' column
            item_values = result_tree.item(selected_item, "values")
            open_comment_window(item_values)
        elif col == '#11':  # '查看路程' column
            item_values = result_tree.item(selected_item, "values")
            open_path_window(item_values)


def open_path_window(item_values):
    # Create a new window
    path_window = tk.Toplevel(root)
    path_window.title("路程信息")
    path_window.geometry("600x400")
    # Create a label to display the path information
    path_label = tk.Label(path_window, text=get_distance(item_values[0], 10))
    path_label.pack(padx=10, pady=10)


def open_comment_window(item_values):
    # Create a new window
    new_window = tk.Toplevel(root)
    new_window.title("查看評論")
    new_window.geometry("600x400")

    # Retrieve comments for the selected item
    comments = get_comments(item_values[0], int(result_count_entry.get()))  # Assuming you want to retrieve 5 comments

    # Generate the comment text
    comment_text = ""
    for i, comment in enumerate(comments, start=1):
        comment_text += f"Comment {i}:\n{comment}\n\n"

    # Create a text box to display the comments
    text_box = tk.Text(new_window, wrap='word')
    text_box.insert('1.0', comment_text)
    text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    text_box.config(state=tk.DISABLED)


def open_more_info_window(item_values):
    new_window = tk.Toplevel(root)
    new_window.title("更多資料")
    new_window.geometry("600x400")
    business_name = item_values[0]
    business = next((b for b in global_results if b.name == business_name), None)

    if business and business.opening_hours:
        for day, hours in business.opening_hours.items():
            label = tk.Label(new_window, text=f"{day}: {hours}")
            label.pack(pady=5)
    else:
        label = tk.Label(new_window, text="沒有營業時間資料")
        label.pack(pady=20)


def show_reviews():
    selected_item = result_tree.focus()
    if selected_item:
        item_values = result_tree.item(selected_item, "values")
        print(f"查看評論: {item_values[0]}")


def show_directions():
    selected_item = result_tree.focus()
    if selected_item:
        item_values = result_tree.item(selected_item, "values")
        print(f"路程: {item_values[0]}")


def on_right_click(event):
    selected_item = result_tree.identify('item', event.x, event.y)
    if selected_item:
        result_tree.selection_set(selected_item)
        menu.post(event.x_root, event.y_root)


def choose_dinner():
    if global_results:
        choice_window = tk.Toplevel(root)
        choice_window.title("晚餐選擇器")
        choice_window.geometry("800x600")

        choice_label = tk.Label(choice_window, text="晚餐選擇器", font=("Arial", 20, "bold"))
        choice_label.pack(pady=20)

        choice_var = tk.StringVar()
        choice_listbox = tk.Listbox(choice_window, listvariable=choice_var, font=("Arial", 16))
        choice_listbox.pack(pady=20, fill=tk.BOTH, expand=True)

        for business in global_results:
            choice_listbox.insert(tk.END, business.name)

        def start_selection():
            for _ in range(30):
                selected_idx = random.randint(0, len(global_results) - 1)
                choice_listbox.selection_clear(0, tk.END)
                choice_listbox.selection_set(selected_idx)
                choice_listbox.activate(selected_idx)
                choice_listbox.see(selected_idx)
                choice_window.update()
                time.sleep(0.1)

            final_choice = global_results[selected_idx]
            result_label.config(text=f"今晚的晚餐選擇是: {final_choice.name}")

        start_button = ttk.Button(choice_window, text="開始選擇", command=start_selection)
        start_button.pack(pady=10)

        result_label = tk.Label(choice_window, text="", font=("Arial", 16, "bold"))
        result_label.pack(pady=20)


root = tk.Tk()
root.title("Google地圖餐廳爬蟲")
root.configure(bg="#F0F0F0")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4CAF50", foreground="white")
style.map("Treeview", background=[("selected", "#E0F7FA")])

title_label = ttk.Label(root, text="Google 地圖餐廳爬蟲工具", font=("Arial", 16, "bold"), background="#4CAF50", foreground="white")
title_label.pack(pady=10, fill=tk.X)

search_frame = ttk.Frame(root, style="TFrame")
search_frame.pack(padx=10, pady=10, fill=tk.X)

search_label = ttk.Label(search_frame, text="搜索餐廳:", style="TLabel")
search_label.pack(side=tk.LEFT)

search_entry = ttk.Entry(search_frame, style="TEntry")
search_entry.pack(side=tk.LEFT, padx=5)

result_count_label = ttk.Label(search_frame, text="結果數量:", style="TLabel")
result_count_label.pack(side=tk.LEFT, padx=5)

result_count_entry = ttk.Entry(search_frame, width=5, style="TEntry")
result_count_entry.pack(side=tk.LEFT)

start_button = ttk.Button(search_frame, text="開始爬蟲", style="TButton", command=start_search)
start_button.pack(side=tk.LEFT, padx=5)

result_frame = ttk.Frame(root, style="TFrame")
result_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

result_tree = ttk.Treeview(result_frame, style="Treeview")
result_tree["columns"] = (
    "name", "address", "category", "status", "phone", "review_count", "rating", "coordinates", "more", "reviews",
    "directions")
result_tree.column("#0", width=50)
result_tree.heading("#0", text="No.")
result_tree.column("name", width=100, anchor=tk.W)
result_tree.heading("name", text="店名")
result_tree.column("address", width=100, anchor=tk.W)
result_tree.heading("address", text="地址")
result_tree.column("category", width=40, anchor=tk.W)
result_tree.heading("category", text="類別")
result_tree.column("status", width=50, anchor=tk.W)
result_tree.heading("status", text="營業狀態")
result_tree.column("phone", width=80, anchor=tk.W)
result_tree.heading("phone", text="電話")
result_tree.column("review_count", width=50, anchor=tk.E)
result_tree.heading("review_count", text="評論數目")
result_tree.column("rating", width=50, anchor=tk.E)
result_tree.heading("rating", text="評分")
result_tree.column("coordinates", width=100, anchor=tk.W)
result_tree.heading("coordinates", text="經緯度")
result_tree.column("more", width=80, anchor=tk.CENTER)
result_tree.heading("more", text="更多資料")
result_tree.column("reviews", width=80, anchor=tk.CENTER)
result_tree.heading("reviews", text="查看評論")
result_tree.column("directions", width=80, anchor=tk.CENTER)
result_tree.heading("directions", text="路程")
result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

root.update_idletasks()
width = result_tree.winfo_reqwidth() + 300
height = result_tree.winfo_reqheight() + 200
root.geometry(f"{width}x{height}")

button_frame = ttk.Frame(root, style="TFrame")
button_frame.pack(padx=10, pady=10, fill=tk.X)

sort_frame = ttk.Frame(button_frame, style="TFrame")
sort_frame.pack(side=tk.LEFT)

sort_label = ttk.Label(sort_frame, text="排序依據:", style="TLabel")
sort_label.pack(side=tk.LEFT)

sort_var = tk.StringVar()
sort_option = ttk.Combobox(sort_frame, textvariable=sort_var, values=["路程", "店名", "評分"], style="TCombobox")
sort_option.pack(side=tk.LEFT, padx=5)

sort_button = ttk.Button(sort_frame, text="排序", style="TButton", command=sort_treeview)
sort_button.pack(side=tk.LEFT, padx=5)

dinner_button = ttk.Button(button_frame, text="晚餐選擇器", style="TButton", command=choose_dinner)
dinner_button.pack(side=tk.RIGHT, padx=5)

# 右鍵菜單
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="更多資料", command=show_more_info)
menu.add_command(label="查看評論", command=show_reviews)
menu.add_command(label="路程", command=show_directions)

result_tree.bind("<Double-1>", show_more_info)
result_tree.bind("<Button-3>", on_right_click)

root.mainloop()

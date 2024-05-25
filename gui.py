import tkinter as tk
from tkinter import ttk

# 創建主視窗
root = tk.Tk()
root.title("Google地圖餐廳爬蟲")
root.configure(bg="#F0F0F0")  # 設置背景顏色

# 自定義樣式
style = ttk.Style()
style.theme_use("clam")  # 設置主題
style.configure("Treeview", rowheight=25)  # 設置行高
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#4CAF50", foreground="white")  # 設置表頭樣式
style.map("Treeview", background=[("selected", "#E0F7FA")])  # 設置選中行的背景顏色

# 創建搜索框
search_frame = ttk.Frame(root, style="TFrame")
search_frame.pack(padx=10, pady=10)

search_label = ttk.Label(search_frame, text="搜索餐廳:", style="TLabel")
search_label.pack(side=tk.LEFT)

search_entry = ttk.Entry(search_frame, style="TEntry")
search_entry.pack(side=tk.LEFT, padx=5)

result_count_label = ttk.Label(search_frame, text="結果數量:", style="TLabel")
result_count_label.pack(side=tk.LEFT, padx=5)

result_count_entry = ttk.Entry(search_frame, width=5, style="TEntry")
result_count_entry.pack(side=tk.LEFT)

# 創建結果顯示區域
result_frame = ttk.Frame(root, style="TFrame")
result_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

result_tree = ttk.Treeview(result_frame, style="Treeview")
result_tree["columns"] = ("name", "address", "category", "status", "phone", "review_count", "rating", "coordinates", "more", "reviews", "directions")
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
result_tree.column("coordinates", width=50, anchor=tk.W)
result_tree.heading("coordinates", text="經緯度")
result_tree.column("more", width=50, anchor=tk.CENTER)
result_tree.heading("more", text="更多資料")
result_tree.column("reviews", width=50, anchor=tk.CENTER)
result_tree.heading("reviews", text="查看評論")
result_tree.column("directions", width=40, anchor=tk.CENTER)
result_tree.heading("directions", text="路程")
result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 自動調整窗口大小以適應內容
root.update_idletasks()
width = result_tree.winfo_reqwidth() + 300
height = result_tree.winfo_reqheight() + 200
root.geometry(f"{width}x{height}")

# 創建開始爬蟲按鈕
start_button = ttk.Button(root, text="開始爬蟲", style="TButton")
start_button.pack(padx=10, pady=10)

# 創建排序選擇框
sort_frame = ttk.Frame(root, style="TFrame")
sort_frame.pack(padx=10, pady=10)

sort_label = ttk.Label(sort_frame, text="排序依據:", style="TLabel")
sort_label.pack(side=tk.LEFT)

sort_var = tk.StringVar()
sort_option = ttk.Combobox(sort_frame, textvariable=sort_var, values=["路程", "店名", "評分"], style="TCombobox")
sort_option.pack(side=tk.LEFT, padx=5)

sort_button = ttk.Button(sort_frame, text="排序", style="TButton")
sort_button.pack(side=tk.LEFT, padx=5)

# 創建更多資料、查看評論和路程按鈕的功能
def show_more_info(event):
    selected_item = result_tree.focus()
    if selected_item:
        item_values = result_tree.item(selected_item, "values")
        # 在這裡處理更多資料的功能
        print(f"更多資料: {item_values[0]}")

def show_reviews(event):
    selected_item = result_tree.focus()
    if selected_item:
        item_values = result_tree.item(selected_item, "values")
        # 在這裡處理查看評論的功能
        print(f"查看評論: {item_values[0]}")

def show_directions(event):
    selected_item = result_tree.focus()
    if selected_item:
        item_values = result_tree.item(selected_item, "values")
        # 在這裡處理路程的功能
        print(f"路程: {item_values[0]}")

result_tree.bind("<Double-1>", show_more_info)
result_tree.bind("<Button-3>", show_reviews)
result_tree.bind("<Button-2>", show_directions)

# 運行主循環
root.mainloop()
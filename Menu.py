import tkinter as tk
from tkinter import ttk, messagebox
from crud.CRUD import read_csv_data, create_data, update_data, delete_data, paginate_data
from tool.tool import sort_data, search_data, filter_data
import pandas as pd

CSV_FILE = "cleaned_and_predicted_data.csv"

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý dữ liệu")
        self.root.geometry("900x900")  # Đặt kích thước cửa sổ là 900x900
        self.root.resizable(False, False)  # Không cho phép thay đổi kích thước cửa sổ
        self.data = pd.DataFrame(read_csv_data())

        # Giao diện chính
        self.create_main_ui()
        
        

    def create_main_ui(self):
        # Menu chính
        ttk.Label(self.root, text="Menu Chính", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        buttons = [
            ("Xem dữ liệu", self.view_data),
            ("Thêm dữ liệu", self.add_data),
            ("Cập nhật dữ liệu", self.update_data),
            ("Xóa dữ liệu", self.delete_data),
            ("Sắp xếp dữ liệu", self.sort_data),
            ("Tìm kiếm dữ liệu", self.search_data),
            ("Lọc dữ liệu", self.filter_data),
            ("Thoát", self.exit_app)
        ]
        

        for i, (label, command) in enumerate(buttons):
            ttk.Button(self.root, text=label, command=command).grid(row=i + 1, column=0, padx=10, pady=5, sticky="ew")

    def view_data(self):
        # Xem dữ liệu với phân trang
        def show_paginated_data(page_size):
            paginated_data = paginate_data(self.data, page_size)
            messagebox.showinfo("Dữ liệu", paginated_data)

        top = tk.Toplevel(self.root)
        top.title("Xem dữ liệu")
        ttk.Label(top, text="Nhập số dòng mỗi trang:").grid(row=0, column=0, padx=10, pady=10)
        page_size_entry = ttk.Entry(top)
        page_size_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(top, text="Xem", command=lambda: show_paginated_data(int(page_size_entry.get()))).grid(
            row=1, column=0, columnspan=2, pady=10
        )

    def add_data(self):
        # Thêm dữ liệu mới
        top = tk.Toplevel(self.root)
        top.title("Thêm dữ liệu")
        entries = {}
        for i, col in enumerate(self.data.columns):
            ttk.Label(top, text=f"Nhập {col}:").grid(row=i, column=0, padx=10, pady=5)
            entry = ttk.Entry(top)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[col] = entry

        def save_new_data():
            new_entry = {col: entry.get() for col, entry in entries.items()}
            create_data(self.data.to_dict("records"), new_entry)
            messagebox.showinfo("Thành công", "Dữ liệu đã được thêm!")
            top.destroy()

        ttk.Button(top, text="Lưu", command=save_new_data).grid(row=len(entries), column=0, columnspan=2, pady=10)

    def update_data(self):
        # Cập nhật dữ liệu
        top = tk.Toplevel(self.root)
        top.title("Cập nhật dữ liệu")
        ttk.Label(top, text="Nhập tên cần cập nhật:").grid(row=0, column=0, padx=10, pady=5)
        target_name_entry = ttk.Entry(top)
        target_name_entry.grid(row=0, column=1, padx=10, pady=5)

        entries = {}
        for i, col in enumerate(self.data.columns):
            ttk.Label(top, text=f"Nhập {col} mới (bỏ qua nếu không cập nhật):").grid(row=i + 1, column=0, padx=10, pady=5)
            entry = ttk.Entry(top)
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            entries[col] = entry

        def save_update_data():
            target_name = target_name_entry.get()
            updated_entry = {col: entry.get() for col, entry in entries.items() if entry.get()}
            if update_data(self.data.to_dict("records"), target_name, updated_entry):
                messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật!")
            else:
                messagebox.showerror("Thất bại", "Không tìm thấy dữ liệu!")
            top.destroy()

        ttk.Button(top, text="Cập nhật", command=save_update_data).grid(row=len(entries) + 1, column=0, columnspan=2, pady=10)

    def delete_data(self):
        # Xóa dữ liệu
        top = tk.Toplevel(self.root)
        top.title("Xóa dữ liệu")
        ttk.Label(top, text="Nhập tên cần xóa (phân cách bằng dấu phẩy):").grid(row=0, column=0, padx=10, pady=10)
        target_names_entry = ttk.Entry(top)
        target_names_entry.grid(row=0, column=1, padx=10, pady=10)

        def delete_selected_data():
            target_names = target_names_entry.get().split(", ")
            if delete_data(self.data.to_dict("records"), target_names):
                messagebox.showinfo("Thành công", "Dữ liệu đã được xóa!")
            else:
                messagebox.showerror("Thất bại", "Không tìm thấy dữ liệu để xóa!")
            top.destroy()

        ttk.Button(top, text="Xóa", command=delete_selected_data).grid(row=1, column=0, columnspan=2, pady=10)

    def sort_data(self):
        sorted_data = sort_data(self.data)
        messagebox.showinfo("Kết quả sắp xếp", sorted_data.to_string())

    def search_data(self):
        search_result = search_data(self.data)
        messagebox.showinfo("Kết quả tìm kiếm", search_result.to_string())

    def filter_data(self):
        filtered_data = filter_data(self.data)
        messagebox.showinfo("Kết quả lọc", filtered_data.to_string())

    def exit_app(self):
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()

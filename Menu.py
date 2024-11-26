import tkinter as tk
from tkinter import ttk, messagebox
from crud.CRUD import read_csv_data, paginate_data, create_data, update_data
import pandas as pd

CSV_FILE = "cleaned_and_predicted_data.csv"

VALID_VALUES = {
    "Smoking Status": ["Non-smoker", "Former", "Current"],
    "Physical Activity Level": ["Sedentary", "Moderate", "Active"],
    "Employment Status": ["Employed", "Unemployed"],
    "Alcohol Consumption": ["Low", "Moderate", "High"],
    "Dietary Habits": ["Healthy", "Moderate", "Unhealthy"],
    "Sleep Patterns": ["Poor", "Good", "Fair"],
    "History of Mental Illness": ["Yes", "No"],
    "History of Substance Abuse": ["Yes", "No"],
    "Family History of Depression": ["Yes", "No"],
    "Chronic Medical Conditions": ["Yes", "No"],
    "Marital Status": ["Single", "Married", "Divorced", "Widowed"],
    "Education Level": ["High School", "Bachelor's Degree", "Master's Degree", "Associate Degree", "PhD"],
    "Depression Risk": ["Low", "Medium", "High", "Very High"]
}


class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý dữ liệu")
        self.root.geometry("1200x600")

        self.data = read_csv_data()
        self.current_page = 1
        self.page_size = 10
        self.total_pages = 1

        # Treeview và thanh cuộn
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree, self.v_scroll, self.h_scroll = self.create_treeview_with_scrollbars(
            parent_frame=self.tree_frame, columns=list(self.data.columns), height=20
        )
        self.tree.bind("<Double-1>", self.on_treeview_double_click)

        # Menu chức năng
        self.menu_frame = ttk.Frame(root)
        self.menu_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        ttk.Button(self.menu_frame, text="Xem dữ liệu", command=self.view_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Thêm dữ liệu", command=self.add_new_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Tìm kiếm dữ liệu", command=self.open_search_window).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Thoát", command=root.quit).pack(side=tk.RIGHT, padx=10)

        # Điều hướng trang
        self.nav_frame = ttk.Frame(root)
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        ttk.Button(self.nav_frame, text="Trang trước", command=self.prev_page).pack(side=tk.LEFT, padx=10)
        self.page_entry = ttk.Entry(self.nav_frame, width=5)
        self.page_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(self.nav_frame, text="Đi tới trang", command=self.goto_page).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.nav_frame, text="Trang sau", command=self.next_page).pack(side=tk.RIGHT, padx=10)

        self.pagination_label = ttk.Label(root, text="Trang: 1/1", font=("Arial", 10))
        self.pagination_label.pack(side=tk.BOTTOM, pady=5)

        self.update_treeview()
        
    def on_treeview_double_click(self, event):
        """
        Xử lý khi người dùng nhấp đúp vào một hàng trong Treeview.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một dòng để thao tác.")
            return

        # Lấy chỉ số của dòng được chọn
        record_index = int(self.tree.item(selected_item)["tags"][0])

        # Hiển thị cửa sổ xác nhận
        action_window = tk.Toplevel(self.root)
        action_window.title("Chọn hành động")
        action_window.geometry("300x150")

        ttk.Label(action_window, text="Bạn muốn thực hiện hành động nào?").pack(pady=10)

        def update_record():
            """
            Gọi hàm cập nhật dữ liệu.
            """
            action_window.destroy()
            self.open_input_window(
                title="Cập nhật dữ liệu",
                action_callback=lambda updated_data: self.handle_update_data(record_index, updated_data),
                record_data=self.data.loc[record_index].to_dict()
            )

        def delete_record():
            """
            Xóa dòng đã chọn và cập nhật file CSV.
            """
            action_window.destroy()
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa dữ liệu này?")
            if confirm:
                try:
                    # Xóa dòng khỏi DataFrame
                    self.data = self.data.drop(record_index).reset_index(drop=True)
                    
                    # Cập nhật lại file CSV
                    self.data.to_csv(CSV_FILE, index=False)

                    # Cập nhật Treeview
                    self.update_treeview()

                    messagebox.showinfo("Thành công", "Dữ liệu đã được xóa.")
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi xóa dữ liệu: {e}")


        ttk.Button(action_window, text="Cập nhật", command=update_record).pack(pady=5)
        ttk.Button(action_window, text="Xóa", command=delete_record).pack(pady=5)
        ttk.Button(action_window, text="Hủy", command=action_window.destroy).pack(pady=5)

        
    def view_data(self):
        """
        Hiển thị dữ liệu trong Treeview dựa trên số dòng mỗi trang.
        """
        def set_page_size():
            """
            Cập nhật số dòng hiển thị mỗi trang.
            """
            try:
                page_size = int(entry.get())
                if page_size <= 0:
                    raise ValueError("Số dòng mỗi trang phải lớn hơn 0.")
                self.page_size = page_size
                self.current_page = 1
                self.update_treeview()
                view_window.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Số dòng mỗi trang phải là số nguyên dương.")

        # Cửa sổ để nhập số dòng mỗi trang
        view_window = tk.Toplevel(self.root)
        view_window.title("Xem dữ liệu")
        view_window.geometry("300x150")

        ttk.Label(view_window, text="Nhập số dòng mỗi trang:").pack(pady=10)
        entry = ttk.Entry(view_window)
        entry.pack(pady=5)

        ttk.Button(view_window, text="Xác nhận", command=set_page_size).pack(pady=10)



    def create_treeview_with_scrollbars(self, parent_frame, columns, height=15):
        tree_frame = ttk.Frame(parent_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=height)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor=tk.CENTER)

        tree.grid(row=0, column=0, sticky="nsew")
        v_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")
        tree.configure(yscrollcommand=v_scroll.set)

        h_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=tree.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")
        tree.configure(xscrollcommand=h_scroll.set)

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        return tree, v_scroll, h_scroll

    def update_treeview(self):
        page_data, self.total_pages = paginate_data(self.data, self.page_size, self.current_page)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for idx, row in page_data.iterrows():
            self.tree.insert("", tk.END, values=list(row), tags=(idx,))
        self.pagination_label.config(text=f"Trang: {self.current_page}/{self.total_pages}")

    def handle_update_data(self, record_index, updated_data):
        """
        Cập nhật dữ liệu tại chỉ số được chọn.
        """
        errors = []
        for col, value in updated_data.items():
            if col == "Age":
                if not str(value).isdigit() or not (0 <= int(value) <= 120):
                    errors.append(f"Trường '{col}' phải là số từ 0 đến 120.")
            elif col == "Income":
                try:
                    value = float(value)
                    if value < 0:
                        errors.append(f"Trường '{col}' phải là số không âm.")
                except ValueError:
                    errors.append(f"Trường '{col}' phải là số.")
            elif col in VALID_VALUES and value not in VALID_VALUES[col]:
                errors.append(f"Trường '{col}' phải thuộc {VALID_VALUES[col]}.")

            # Lưu dữ liệu vào DataFrame nếu không có lỗi
            if not errors:
                if pd.api.types.is_numeric_dtype(self.data[col]):
                    self.data.at[record_index, col] = pd.to_numeric(value, errors="coerce")
                else:
                    self.data.at[record_index, col] = value

        if errors:
            messagebox.showerror("Lỗi nhập liệu", "\n".join(errors))
        else:
            self.data.to_csv(CSV_FILE, index=False)
            self.update_treeview()
            messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật.")


    def open_input_window(self, title, action_callback, record_data=None):
        input_window = tk.Toplevel(self.root)
        input_window.title(title)
        input_window.geometry("600x600")

        widgets = {}
        for i, col in enumerate(self.data.columns):
            ttk.Label(input_window, text=f"{col}:").grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            if col in VALID_VALUES:
                widget = ttk.Combobox(input_window, values=VALID_VALUES[col], state="readonly")
                if record_data:
                    widget.set(record_data.get(col, ""))
            else:
                widget = ttk.Entry(input_window, width=30)
                if record_data:
                    widget.insert(0, record_data.get(col, ""))
            widget.grid(row=i, column=1, padx=10, pady=5)
            widgets[col] = widget

        def save_data():
            data = {}
            errors = []
            for col, widget in widgets.items():
                value = widget.get().strip()
                if col == "Age":
                    if not value.isdigit() or not (0 <= int(value) <= 120):
                        errors.append(f"Trường '{col}' phải là số từ 0 đến 120.")
                    else:
                        data[col] = int(value)
                elif col == "Income":
                    if not value.replace('.', '', 1).isdigit() or float(value) < 0:
                        errors.append(f"Trường '{col}' phải là số không âm.")
                    else:
                        data[col] = float(value)
                elif col in VALID_VALUES and value not in VALID_VALUES[col]:
                    errors.append(f"Trường '{col}' phải thuộc {VALID_VALUES[col]}.")
                else:
                    data[col] = value

            if errors:
                messagebox.showerror("Lỗi nhập liệu", "\n".join(errors))
                return

            action_callback(data)
            input_window.destroy()

        ttk.Button(input_window, text="Lưu", command=save_data).grid(row=len(self.data.columns), column=0, columnspan=2, pady=10)

    def add_new_data(self):
        self.open_input_window("Thêm dữ liệu mới", self.handle_add_data)

    def handle_add_data(self, new_data):
        self.data = create_data(self.data, new_data)
        self.current_page = 1
        self.update_treeview()
        messagebox.showinfo("Thành công", "Dữ liệu mới đã được thêm.")

    def open_search_window(self):
        """
        Mở cửa sổ tìm kiếm để người dùng tìm theo bất kỳ cột nào.
        """
        def perform_search():
            column = column_combobox.get()
            value = value_entry.get().strip()
            if not column or not value:
                messagebox.showerror("Lỗi", "Vui lòng chọn cột và nhập giá trị cần tìm.")
                return
            results = self.data[self.data[column].astype(str).str.contains(value, case=False, na=False)]
            for row in results_tree.get_children():
                results_tree.delete(row)
            for idx, row in results.iterrows():
                results_tree.insert("", tk.END, values=list(row), tags=(idx,))

        search_window = tk.Toplevel(self.root)
        search_window.title("Tìm kiếm dữ liệu")
        search_window.geometry("800x500")

        ttk.Label(search_window, text="Chọn cột để tìm kiếm:").pack(pady=5)
        column_combobox = ttk.Combobox(search_window, values=list(self.data.columns), state="readonly")
        column_combobox.pack(pady=5)

        ttk.Label(search_window, text="Nhập giá trị cần tìm:").pack(pady=5)
        value_entry = ttk.Entry(search_window, width=30)
        value_entry.pack(pady=5)

        ttk.Button(search_window, text="Tìm kiếm", command=perform_search).pack(pady=10)

        results_tree, _, _ = self.create_treeview_with_scrollbars(search_window, list(self.data.columns), height=15)
        results_tree.bind("<Double-1>", self.on_treeview_double_click)  # Thêm sự kiện nhấp đúp

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_treeview()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_treeview()

    def goto_page(self):
        try:
            page = int(self.page_entry.get())
            if 1 <= page <= self.total_pages:
                self.current_page = page
                self.update_treeview()
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Lỗi", "Số trang phải là số hợp lệ.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()

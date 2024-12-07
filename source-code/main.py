import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from crud import read_csv_data, paginate_data, create_data, update_data, delete_records
from search_filter_sort import sort_data, filter_data
from visualization import plot_age_distribution, plot_education_vs_depression, plot_employment_vs_depression, plot_sleep_vs_depression, plot_marital_vs_depression
# from data_cleaning import clean_data
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

CSV_FILE ='dataset\\depression_data.csv'

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
        
        self.data = pd.read_csv(CSV_FILE)
        self.original_data = self.data.copy()  # Lưu trữ dữ liệu gốc
        
        
        # self.data = read_csv_data()
        self.current_page = 1
        self.page_size = 10
        self.total_pages = 1

        # Treeview và thanh cuộn
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.frame_data = ttk.Frame(root)

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
        ttk.Button(self.menu_frame, text="Xóa dữ liệu", command=self.delete_selected_records).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Sắp xếp", command=self.open_sort_window).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Lọc", command=self.open_filter_window).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Xem biểu đồ", command=self.view_chart).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.menu_frame, text="Khôi phục Treeview", command=self.restore_data).pack(side=tk.LEFT, padx=10)
        # ttk.Button(self.menu_frame, text="Lưu thay đổi", command=self.save_changes).pack(side=tk.LEFT, padx=10)
        # ttk.Button(self.menu_frame, text="Khôi phục Treeview", command=self.update_treeview).pack(side=tk.LEFT, padx=10)
        # ttk.Button(self.menu_frame, text="Làm sạch dữ liệu", command=self.clean_data).pack(side=tk.LEFT, padx=10)

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
                    self.data = delete_records(self.data, [record_index])
                    # Cập nhật Treeview
                    self.update_treeview()
                    messagebox.showinfo("Thành công", "Dữ liệu đã được xóa.")
                except ValueError as e:
                    messagebox.showerror("Lỗi", str(e))

        ttk.Button(action_window, text="Cập nhật", command=update_record).pack(pady=5)
        ttk.Button(action_window, text="Xóa", command=delete_record).pack(pady=5)
        ttk.Button(action_window, text="Hủy", command=action_window.destroy).pack(pady=5)


    def delete_selected_records(self):
        """
        Xóa các dòng đã chọn từ Treeview và cập nhật DataFrame.
        """
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một dòng để xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa các dòng đã chọn?")
        if confirm:
            try:
                # Lấy danh sách các chỉ số từ tags trong Treeview
                indices = [int(self.tree.item(item)["tags"][0]) for item in selected_items]

                # Gọi hàm delete_records từ CRUD.py
                self.data = delete_records(self.data, indices)

                # Cập nhật Treeview
                self.update_treeview()

                messagebox.showinfo("Thành công", "Dữ liệu đã được xóa.")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))
                
    def delete_records_in_search(self, results_tree):
        """
        Xóa các dòng được chọn trong cửa sổ tìm kiếm và cập nhật Treeview.
        """
        selected_items = results_tree.selection()
        if not selected_items:
            messagebox.showerror("Lỗi", "Vui lòng chọn ít nhất một dòng để xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa các dòng đã chọn?")
        if confirm:
            try:
                # Lấy danh sách các chỉ số từ tags trong Treeview
                indices = [int(results_tree.item(item)["tags"][0]) for item in selected_items]

                # Gọi hàm delete_records từ CRUD.py
                self.data = delete_records(self.data, indices)

                # Cập nhật Treeview chính và Treeview trong cửa sổ tìm kiếm
                self.update_treeview()

                for item in selected_items:
                    results_tree.delete(item)

                messagebox.showinfo("Thành công", "Dữ liệu đã được xóa.")
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))

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
        """
        Tạo thanh cuộn
        """
        tree_frame = ttk.Frame(parent_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=height, selectmode="extended")

        # tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=height)
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
                if not str(value).isdigit() or not (18 <= int(value) <= 80):
                    errors.append(f"Trường '{col}' phải là số từ 18 đến 80.")
            elif col == "Income":
                try:
                    value = float(value)
                    if value < 0:
                        errors.append(f"Trường '{col}' phải là số không âm.")
                except ValueError:
                    errors.append(f"Trường '{col}' phải là số.")
            elif col == "Number of Children":
                    if not str(value).isdigit() or not (0 <= int(value) <= 20):
                        errors.append(f"Trường '{col}' phải là số từ 0 đến 20.")
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
        """
        Mở cửa số nhập liệu
        """
        input_window = tk.Toplevel(self.root)
        input_window.title(title)
        input_window.geometry("400x600")

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
                elif col == "Number of Children":
                    if not value.isdigit() or not (0 <= int(value) <= 20):
                        errors.append(f"Trường '{col}' phải là số từ 0 đến 20")
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
        Mở cửa sổ tìm kiếm nhỏ để người dùng tìm theo bất kỳ cột nào ngay trên cửa sổ Treeview chính.
        """
        def perform_search():
            column = column_combobox.get()  # Cột người dùng chọn
            value = value_entry.get().strip()  # Giá trị người dùng nhập
            if not value:
                messagebox.showerror("Lỗi", "Vui lòng nhập giá trị cần tìm.")
                return

            if not column:  # Nếu không chọn cột, tìm kiếm trong tất cả các cột
                # Tìm kiếm trong tất cả các cột
                results = self.data[self.data.apply(lambda row: row.astype(str).str.contains(value, case=False, na=False).any(), axis=1)]
            else:  # Nếu chọn cột, tìm kiếm trong cột đó
                results = self.data[self.data[column].astype(str).str.contains(value, case=False, na=False)]

            if results.empty:
                messagebox.showinfo("Thông báo", "Không có kết quả tìm kiếm.")
                return

            # Xóa các kết quả cũ trong Treeview chính
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Chèn các kết quả tìm kiếm vào Treeview chính
            for idx, row in results.iterrows():
                self.tree.insert("", tk.END, values=list(row), tags=(idx,))

        # Tạo một khung tìm kiếm nhỏ gọn trên cửa sổ chính
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10, padx=10, fill=tk.X)

        # Label và combobox chọn cột
        ttk.Label(search_frame, text="Chọn cột để tìm kiếm:").pack(side=tk.LEFT, padx=5)
        column_combobox = ttk.Combobox(search_frame, values=[""] + list(self.data.columns), state="readonly")  # Thêm lựa chọn trống cho tìm kiếm trong tất cả cột
        column_combobox.pack(side=tk.LEFT, padx=5)

        # Label và ô nhập giá trị cần tìm
        ttk.Label(search_frame, text="Nhập giá trị cần tìm:").pack(side=tk.LEFT, padx=5)
        value_entry = ttk.Entry(search_frame, width=30)
        value_entry.pack(side=tk.LEFT, padx=5)

        # Nút tìm kiếm
        ttk.Button(search_frame, text="Tìm kiếm", command=perform_search).pack(side=tk.LEFT, padx=10)
       
        
    def open_filter_window(self):
        """Mở cửa sổ lọc dữ liệu."""
        def perform_filter():
            """
            Lọc dữ liệu trong Treeview dựa trên cột và giá trị người dùng nhập.
            """
            column = column_combobox.get()
            value = value_entry.get().strip()
            if not column or not value:
                messagebox.showerror("Lỗi", "Vui lòng chọn cột và nhập giá trị cần lọc.")
                return
            try:
                # Sử dụng hàm filter_data để lọc
                self.data = filter_data(self.data, column, value)
                self.current_page = 1
                self.update_treeview()  # Cập nhật Treeview với dữ liệu mới
            except ValueError as e:
                messagebox.showerror("Lỗi", str(e))


        filter_window = tk.Toplevel(self.root)
        filter_window.title("Lọc dữ liệu")
        filter_window.geometry("300x200")

        ttk.Label(filter_window, text="Chọn cột:").pack(pady=5)
        column_combobox = ttk.Combobox(filter_window, values=list(self.data.columns), state="readonly")
        column_combobox.pack(pady=5)

        ttk.Label(filter_window, text="Nhập giá trị:").pack(pady=5)
        value_entry = ttk.Entry(filter_window)
        value_entry.pack(pady=5)

        ttk.Button(filter_window, text="Lọc", command=perform_filter).pack(pady=10)

    def open_sort_window(self):
        """Mở cửa sổ sắp xếp dữ liệu."""
        def perform_sort():
            column = column_combobox.get()
            order = order_combobox.get()
            ascending = True if order == "Tăng dần" else False

            if not column:
                messagebox.showerror("Lỗi", "Vui lòng chọn cột để sắp xếp.")
                return
            
            self.data = sort_data(self.data, column, ascending)
            self.update_treeview()
            sort_window.destroy()
            messagebox.showinfo("Thành công", f"Dữ liệu đã được sắp xếp theo '{column}' ({order}).")

        sort_window = tk.Toplevel(self.root)
        sort_window.title("Sắp xếp dữ liệu")
        sort_window.geometry("300x200")

        ttk.Label(sort_window, text="Chọn cột:").pack(pady=5)
        column_combobox = ttk.Combobox(sort_window, values=list(self.data.columns), state="readonly")
        column_combobox.pack(pady=5)

        ttk.Label(sort_window, text="Thứ tự:").pack(pady=5)
        order_combobox = ttk.Combobox(sort_window, values=["Tăng dần", "Giảm dần"], state="readonly")
        order_combobox.pack(pady=5)

        ttk.Button(sort_window, text="Sắp xếp", command=perform_sort).pack(pady=10)

    # def clear(self):
    #     """
    #     Khôi phục dữ liệu về trạng thái ban đầu (xóa bộ lọc) và cập nhật lại file CSV.
    #     """
    #     self.data = self.original_data.copy()  # Khôi phục dữ liệu gốc
    #     self.update_treeview()  # Cập nhật Treeview với dữ liệu gốc
    #     self.data.to_csv(CSV_FILE, index=False)  # Cập nhật lại file CSV với dữ liệu gốc
    #     messagebox.showinfo("Thông báo", "Dữ liệu đã được khôi phục về trạng thái ban đầu.")

    

    def view_chart(self):
        """
        Mở cửa sổ để hiển thị biểu đồ, bao gồm cả biểu đồ từ 'visualization.py'.
        """
        def plot_chart():
            """
            Vẽ biểu đồ cho cột đã chọn từ dữ liệu trong DataFrame hoặc từ các hàm trong visualization.py.
            """
            selected_chart = chart_combobox.get()
            file_path_age_education = 'dataset\\filtered_depression_data.csv'
            file_path_employment = 'dataset\\cleaned_and_predicted_data.csv'
            self.data_age_education = pd.read_csv(file_path_age_education)
            self.data_employment = pd.read_csv(file_path_employment)
            if selected_chart == "Biểu đồ phân bố tuổi":
                plot_age_distribution(self.data_age_education)
            elif selected_chart == "Biểu đồ học vấn và trầm cảm":
                plot_education_vs_depression(self.data_age_education)
            elif selected_chart == "Biểu đồ việc làm và trầm cảm":
                plot_employment_vs_depression(self.data_employment)
            elif selected_chart == "Biểu đồ giấc ngủ và trầm cảm":
                plot_sleep_vs_depression(self.data_age_education)
            elif selected_chart == "Biểu đồ tình trạng hôn nhân và trầm cảm":
                plot_marital_vs_depression(self.data_employment)
            else:
                return

            # # Tạo figure cho biểu đồ
            # fig, ax = plt.subplots(figsize=(8, 6))

            #     # Kiểm tra kiểu dữ liệu của cột
            # if self.data[column].dtype == 'object':  # Dữ liệu phân loại (categorical)
            #     value_counts = self.data[column].value_counts()
            #     value_counts.plot(kind='bar', ax=ax, color='skyblue')
            #     ax.set_title(f"Biểu đồ cột của '{column}'")
            #     ax.set_xlabel(column)
            #     ax.set_ylabel('Số lượng')
            # else:  # Dữ liệu số (numerical)
            #     self.data[column].plot(kind='hist', ax=ax, color='skyblue', edgecolor='black', bins=20)
            #     ax.set_title(f"Biểu đồ phân bố của '{column}'")
            #     ax.set_xlabel(column)
            #     ax.set_ylabel('Tần suất')

            # # Tạo canvas cho biểu đồ
            # canvas = FigureCanvasTkAgg(fig, master=chart_window)  
            # canvas.draw()
            # canvas.get_tk_widget().pack()

        # Cửa sổ hiển thị biểu đồ
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Xem Biểu đồ")
        chart_window.geometry("500x600")

        ttk.Label(chart_window, text="Chọn biểu đồ:").pack(pady=10)
        chart_combobox = ttk.Combobox(chart_window, values=[
            "Biểu đồ phân bố tuổi", 
            "Biểu đồ học vấn và trầm cảm", 
            "Biểu đồ việc làm và trầm cảm",
            "Biểu đồ giấc ngủ và trầm cảm",
            "Biểu đồ tình trạng hôn nhân và trầm cảm"
        ], )
        chart_combobox.pack(pady=5)

        # ttk.Label(chart_window, text="Chọn cột để vẽ biểu đồ:").pack(pady=10)
        # column_combobox = ttk.Combobox(chart_window, values=list(self.data.columns), state="readonly")
        # column_combobox.pack(pady=5)

        ttk.Button(chart_window, text="Vẽ biểu đồ", command=plot_chart).pack(pady=10)
    
    # def clean_data(self):
    #     """
    #     Hàm xử lý khi nhấn nút "Làm sạch dữ liệu"
    #     """
    #     try:
    #         file_path = 'dataset\\depression_data.csv'  # Đường dẫn đến file CSV gốc
    #         output_path = 'dataset\\cleaned_and_predicted_data.csv'  # Đường dẫn đến file kết quả
    #         cleaned_data = clean_data(file_path, output_path)  # Gọi hàm clean_data
    #         messagebox.showinfo("Thành công", "Dữ liệu đã được làm sạch và lưu vào file mới.")
    #     except Exception as e:
    #         messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def save_changes(self):
        """
        Lưu các thay đổi từ self.data vào self.original_data.
        Điều này sẽ cập nhật dữ liệu gốc với tất cả các thay đổi (thêm, xóa, cập nhật).
        """
        self.original_data = self.data.copy()  # Sao chép dữ liệu hiện tại vào dữ liệu gốc
        messagebox.showinfo("Thông báo", "Thay đổi đã được lưu!")
        
    def restore_data(self):
        """
        Khôi phục dữ liệu về trạng thái ban đầu (không bao gồm các thay đổi về tìm kiếm, lọc, sắp xếp).
        Các thay đổi về thêm, xóa, cập nhật vẫn được lưu giữ.
        """
        # Khôi phục dữ liệu về trạng thái ban đầu
        self.data = self.original_data.copy()
    
        # Cập nhật lại Treeview để hiển thị dữ liệu đã khôi phục
        self.update_treeview()
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


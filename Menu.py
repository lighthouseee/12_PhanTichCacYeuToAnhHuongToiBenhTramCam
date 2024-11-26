import tkinter as tk
from tkinter import ttk
import pandas as pd
from crud.CRUD import read_csv_data

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Xem Dữ Liệu CSV")
        self.root.geometry("800x600")
        
        # Đọc dữ liệu từ file CSV
        self.data = pd.DataFrame(read_csv_data())  # Đảm bảo hàm trả về dữ liệu đúng dạng
        
        # Làm sạch tên cột để đảm bảo chúng hợp lệ
        self.data.columns = [col.strip().replace(" ", "_") for col in self.data.columns]
        
        # In ra tên cột để kiểm tra
        print("Tên các cột:", self.data.columns)
        
        # Tạo frame để chứa Treeview và thanh cuộn
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tạo Treeview để hiển thị dữ liệu
        self.tree = ttk.Treeview(frame, columns=self.data.columns, show="headings")
        for col in self.data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Tạo thanh cuộn dọc (vertical scrollbar)
        vsb = tk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Tạo thanh cuộn ngang (horizontal scrollbar)
        hsb = tk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=hsb.set)
        
        # Đặt Treeview vào frame
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Tải dữ liệu từ CSV vào Treeview
        self.load_data()
    
    def load_data(self):
        # Xóa hết các dữ liệu cũ trong Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Thêm dữ liệu từ DataFrame vào Treeview
        for index, row in self.data.iterrows():
            self.tree.insert("", "end", values=list(row))
    
    def auto_adjust_treeview_columns(self):
        # Tự động điều chỉnh chiều rộng cột Treeview
        for col in self.tree['columns']:
            max_width = max(len(str(item)) for item in self.data[col])
            self.tree.column(col, width=max_width * 10)


# Khởi tạo cửa sổ Tkinter
root = tk.Tk()

# Tạo ứng dụng và chạy
app = DataApp(root)
root.mainloop()

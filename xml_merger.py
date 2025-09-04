import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
import os
import re
from pathlib import Path


class XMLMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML File Merger - Ghép File XML")
        self.root.geometry("800x600")
        
        # Danh sách các file XML sẽ ghép
        self.xml_files = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="XML File Merger", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame nhập đường dẫn
        input_frame = ttk.LabelFrame(main_frame, text="Thêm File XML", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Đường dẫn file
        ttk.Label(input_frame, text="Đường dẫn:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(input_frame, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Nút Browse
        ttk.Button(input_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, padx=(5, 0))
        
        # Frame nút thao tác
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        # Nút thêm file
        ttk.Button(button_frame, text="Thêm File", command=self.add_file).pack(side=tk.LEFT, padx=(0, 5))
        
        # Nút dán từ clipboard
        ttk.Button(button_frame, text="Dán từ Clipboard", command=self.paste_from_clipboard).pack(side=tk.LEFT, padx=5)
        
        # Nút xóa hết
        ttk.Button(button_frame, text="Xóa Hết", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Frame danh sách file
        list_frame = ttk.LabelFrame(main_frame, text="Danh Sách File XML", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Listbox với scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(listbox_frame, height=10)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar cho listbox
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Nút xóa file được chọn
        ttk.Button(list_frame, text="Xóa File Được Chọn", command=self.remove_selected).grid(row=1, column=0, pady=(10, 0))
        
        # Frame output
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        # Tên file output
        ttk.Label(output_frame, text="Tên file output:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.output_var = tk.StringVar(value="merged_output.xml")
        ttk.Entry(output_frame, textvariable=self.output_var, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Nút ghép file
        merge_button = ttk.Button(main_frame, text="GHÉP FILE XML", command=self.merge_files, style="Accent.TButton")
        merge_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Cấu hình trọng số cho grid
        main_frame.rowconfigure(2, weight=1)
        
        # Bind Enter key cho entry
        self.path_entry.bind('<Return>', lambda e: self.add_file())
        
    def browse_file(self):
        """Mở dialog chọn file"""
        filename = filedialog.askopenfilename(
            title="Chọn file XML",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.path_var.set(filename)
            
    def paste_from_clipboard(self):
        """Dán đường dẫn từ clipboard"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.path_var.set(clipboard_content.strip())
        except tk.TclError:
            messagebox.showwarning("Cảnh báo", "Clipboard trống hoặc không thể đọc")
            
    def add_file(self):
        """Thêm file vào danh sách"""
        file_path = self.path_var.get().strip()
        
        if not file_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đường dẫn file")
            return
            
        # Kiểm tra file tồn tại
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"File không tồn tại: {file_path}")
            return
            
        # Kiểm tra extension
        if not file_path.lower().endswith('.xml'):
            messagebox.showwarning("Cảnh báo", "File phải có extension .xml")
            return
            
        # Kiểm tra duplicate
        if file_path in self.xml_files:
            messagebox.showwarning("Cảnh báo", "File đã có trong danh sách")
            return
            
        # Thêm vào danh sách
        self.xml_files.append(file_path)
        self.file_listbox.insert(tk.END, os.path.basename(file_path))
        
        # Xóa nội dung entry
        self.path_var.set("")
        
        messagebox.showinfo("Thành công", f"Đã thêm file: {os.path.basename(file_path)}")
        
    def remove_selected(self):
        """Xóa file được chọn trong listbox"""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn file để xóa")
            return
            
        index = selection[0]
        file_path = self.xml_files[index]
        
        # Xóa khỏi danh sách
        del self.xml_files[index]
        self.file_listbox.delete(index)
        
        messagebox.showinfo("Thành công", f"Đã xóa file: {os.path.basename(file_path)}")
        
    def clear_all(self):
        """Xóa tất cả file trong danh sách"""
        if not self.xml_files:
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả file?"):
            self.xml_files.clear()
            self.file_listbox.delete(0, tk.END)
            messagebox.showinfo("Thành công", "Đã xóa tất cả file")
            
    def extract_content_elements(self, xml_content):
        """Trích xuất tất cả các thẻ content từ XML"""
        try:
            # Loại bỏ comment trước khi parse
            comment_pattern = r'<!--.*?-->'
            cleaned_content = re.sub(comment_pattern, '', xml_content, flags=re.DOTALL)
            
            # Parse XML
            root = ET.fromstring(cleaned_content)
            
            # Tìm tất cả các thẻ content
            content_elements = []
            for content in root.findall('.//content'):
                content_elements.append(content)
            
            return content_elements
        except ET.ParseError as e:
            raise Exception(f"Lỗi parse XML: {str(e)}")
        except Exception as e:
            raise Exception(f"Lỗi xử lý XML: {str(e)}")
        
    def merge_files(self):
        """Ghép các file XML thành một file"""
        if not self.xml_files:
            messagebox.showwarning("Cảnh báo", "Chưa có file nào để ghép")
            return
            
        output_filename = self.output_var.get().strip()
        if not output_filename:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên file output")
            return
            
        try:
            # Tạo thư mục output nếu chưa có
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
            os.makedirs(output_dir, exist_ok=True)
            
            output_path = os.path.join(output_dir, output_filename)
            
            # Tạo root element mới
            merged_root = ET.Element("contentList")
            
            total_content_count = 0
            
            # Đọc và ghép content từ từng file
            for file_path in self.xml_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Trích xuất các thẻ content
                    content_elements = self.extract_content_elements(content)
                    
                    # Thêm tất cả content vào merged_root
                    for content_elem in content_elements:
                        merged_root.append(content_elem)
                        total_content_count += 1
                    
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể xử lý file {file_path}:\n{str(e)}")
                    return
            
            # Tạo tree và ghi file
            merged_tree = ET.ElementTree(merged_root)
            
            # Ghi file với header XML
            with open(output_path, 'wb') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
                merged_tree.write(f, encoding='utf-8', xml_declaration=False)
            
            messagebox.showinfo(
                "Thành công", 
                f"Đã ghép {len(self.xml_files)} file thành công!\n"
                f"Tổng số content: {total_content_count}\n"
                f"File output: {output_path}\n"
                f"Kích thước: {os.path.getsize(output_path)} bytes"
            )
            
            # Mở thư mục output
            if messagebox.askyesno("Mở thư mục", "Bạn có muốn mở thư mục output?"):
                os.startfile(output_dir)
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi ghép file:\n{str(e)}")


def main():
    root = tk.Tk()
    app = XMLMergerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

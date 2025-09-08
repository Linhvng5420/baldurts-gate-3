import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import re
import pyperclip

class XMLSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Content Sorter - Sắp xếp nội dung XML")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), background='#f0f0f0')
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10), background='#f0f0f0')
        style.configure('Modern.TButton', font=('Segoe UI', 10))
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="XML Content Sorter", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Sắp xếp nội dung XML theo contentuid hoặc nội dung", style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # Left frame for input
        left_frame = ttk.LabelFrame(main_frame, text="Nội dung đầu vào", padding="10")
        left_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        # Input buttons frame
        input_buttons_frame = ttk.Frame(left_frame)
        input_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_buttons_frame.columnconfigure(3, weight=1)
        
        paste_btn = ttk.Button(input_buttons_frame, text="📋 Dán từ Clipboard", 
                              command=self.paste_from_clipboard, style='Modern.TButton')
        paste_btn.grid(row=0, column=0, padx=(0, 10))
        
        load_file_btn = ttk.Button(input_buttons_frame, text="📁 Mở file", 
                                  command=self.load_file, style='Modern.TButton')
        load_file_btn.grid(row=0, column=1, padx=(0, 10))
        
        clear_input_btn = ttk.Button(input_buttons_frame, text="🗑️ Xóa", 
                                    command=self.clear_input, style='Modern.TButton')
        clear_input_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Instructions label
        instructions_label = ttk.Label(input_buttons_frame, text="💡 Dán nội dung hoặc mở file XML", 
                             style='Subtitle.TLabel')
        instructions_label.grid(row=0, column=3, sticky=tk.E)
        
        # Input text area
        self.input_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, font=('Consolas', 10),
                                                   height=20, width=50)
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Middle frame for controls
        middle_frame = ttk.Frame(main_frame, width=200)
        middle_frame.grid(row=2, column=1, sticky=(tk.N, tk.S), padx=10)
        middle_frame.grid_propagate(False)
        
        # Sort options
        sort_frame = ttk.LabelFrame(middle_frame, text="Tùy chọn sắp xếp", padding="10")
        sort_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.sort_by = tk.StringVar(value="contentuid")
        
        sort_by_uid_rb = ttk.Radiobutton(sort_frame, text="Theo ContentUID (Text)", 
                                        variable=self.sort_by, value="contentuid")
        sort_by_uid_rb.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        sort_by_uid_num_rb = ttk.Radiobutton(sort_frame, text="Theo ContentUID (Số)", 
                                           variable=self.sort_by, value="contentuid_numeric")
        sort_by_uid_num_rb.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        sort_by_content_rb = ttk.Radiobutton(sort_frame, text="Theo Nội dung", 
                                           variable=self.sort_by, value="content")
        sort_by_content_rb.grid(row=2, column=0, sticky=tk.W, pady=2)
        
        # Order options
        self.sort_order = tk.StringVar(value="asc")
        
        sort_asc_rb = ttk.Radiobutton(sort_frame, text="Tăng dần (A-Z)", 
                                     variable=self.sort_order, value="asc")
        sort_asc_rb.grid(row=3, column=0, sticky=tk.W, pady=2)
        
        sort_desc_rb = ttk.Radiobutton(sort_frame, text="Giảm dần (Z-A)", 
                                      variable=self.sort_order, value="desc")
        sort_desc_rb.grid(row=4, column=0, sticky=tk.W, pady=2)
        
        # Action buttons
        action_frame = ttk.Frame(middle_frame)
        action_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        sort_btn = ttk.Button(action_frame, text="🔄 Sắp xếp", 
                             command=self.sort_content, style='Modern.TButton')
        sort_btn.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=2)
        
        check_duplicate_btn = ttk.Button(action_frame, text="🔍 Kiểm tra trùng lặp", 
                                       command=self.check_duplicates, style='Modern.TButton')
        check_duplicate_btn.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=2)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(middle_frame, text="Thống kê", padding="10")
        stats_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="Chưa có dữ liệu", 
                                   style='Subtitle.TLabel', wraplength=180)
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # Right frame for output
        right_frame = ttk.LabelFrame(main_frame, text="Kết quả", padding="10")
        right_frame.grid(row=2, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Output buttons frame
        output_buttons_frame = ttk.Frame(right_frame)
        output_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_buttons_frame.columnconfigure(2, weight=1)
        
        copy_btn = ttk.Button(output_buttons_frame, text="📋 Copy kết quả", 
                             command=self.copy_result, style='Modern.TButton')
        copy_btn.grid(row=0, column=0, padx=(0, 10))
        
        clear_output_btn = ttk.Button(output_buttons_frame, text="🗑️ Xóa", 
                                     command=self.clear_output, style='Modern.TButton')
        clear_output_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(output_buttons_frame, text="Sẵn sàng", 
                                     style='Subtitle.TLabel')
        self.status_label.grid(row=0, column=2, sticky=tk.E)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=('Consolas', 10),
                                                    height=20, width=50, state=tk.DISABLED)
        self.output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def load_file(self):
        """Load content from file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file XML",
            filetypes=[("XML files", "*.xml"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                self.update_status(f"Đã tải file: {file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def on_drop(self, event):
        """Handle drag and drop files - DEPRECATED"""
        # This function is kept for compatibility but not used
        pass
    
    def paste_from_clipboard(self):
        """Paste content from clipboard"""
        try:
            content = pyperclip.paste()
            if content:
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                self.update_status("Đã dán nội dung từ clipboard")
            else:
                messagebox.showwarning("Cảnh báo", "Clipboard trống")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể dán từ clipboard: {str(e)}")
    
    def clear_input(self):
        """Clear input text area"""
        self.input_text.delete(1.0, tk.END)
        self.update_status("Đã xóa nội dung đầu vào")
    
    def clear_output(self):
        """Clear output text area"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.update_status("Đã xóa kết quả")
    
    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text="Sẵn sàng"))
    
    def check_duplicates(self):
        """Check for duplicate contentuid and display results"""
        input_content = self.input_text.get(1.0, tk.END).strip()
        
        if not input_content:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung cần kiểm tra")
            return
        
        try:
            content_lines = self.extract_content_lines(input_content)
            xml_content_lines = [line for line in content_lines if line['contentuid'] is not None]
            
            if not xml_content_lines:
                messagebox.showinfo("Thông báo", "Không tìm thấy dòng content XML nào để kiểm tra")
                return
            
            # Check for duplicates
            contentuid_count = {}
            duplicate_details = {}
            
            for line in xml_content_lines:
                contentuid = line['contentuid']
                content = line['content']
                
                if contentuid in contentuid_count:
                    contentuid_count[contentuid] += 1
                    if contentuid not in duplicate_details:
                        duplicate_details[contentuid] = []
                    duplicate_details[contentuid].append(content)
                else:
                    contentuid_count[contentuid] = 1
                    duplicate_details[contentuid] = [content]
            
            # Find duplicates
            duplicates = {uid: count for uid, count in contentuid_count.items() if count > 1}
            
            if duplicates:
                # Create compact report
                report_lines = ["=== PHÁT HIỆN CONTENTUID TRÙNG LẶP ==="]
                report_lines.append(f"Tổng số ContentUID trùng lặp: {len(duplicates)}")
                report_lines.append("")
                
                # Show duplicates in compact format
                for uid, count in duplicates.items():
                    short_uid = uid[-32:] if len(uid) > 32 else uid  # Show last 32 chars
                    report_lines.append(f"{count} lần - {short_uid}")
                
                report_lines.append("")
                report_lines.append("=" * 50)
                report_lines.append(f"Tổng số dòng content: {len(xml_content_lines)}")
                report_lines.append(f"Số ContentUID duy nhất: {len(contentuid_count)}")
                report_lines.append(f"Số ContentUID bị trùng: {len(duplicates)}")
                
                report_text = "\n".join(report_lines)
                
                # Display in output area
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, report_text)
                self.output_text.config(state=tk.DISABLED)
                
                # Auto copy to clipboard
                pyperclip.copy(report_text)
                
                # Update statistics
                self.update_statistics(len(xml_content_lines), len(contentuid_count), len(duplicates))
                
                self.update_status(f"Phát hiện {len(duplicates)} ContentUID trùng lặp và copy báo cáo vào clipboard")
                
            else:
                success_message = f"✅ KHÔNG CÓ TRÙNG LẶP\n\n"
                success_message += f"Tổng số dòng content: {len(xml_content_lines)}\n"
                success_message += f"Tất cả {len(contentuid_count)} ContentUID đều duy nhất!"
                
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(1.0, success_message)
                self.output_text.config(state=tk.DISABLED)
                
                pyperclip.copy(success_message)
                
                # Update statistics
                self.update_statistics(len(xml_content_lines), len(contentuid_count), 0)
                
                self.update_status("Không phát hiện ContentUID trùng lặp")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi kiểm tra: {str(e)}")
    
    def update_statistics(self, total_lines, unique_count, duplicate_count):
        """Update statistics display"""
        stats_text = f"📊 Thống kê:\n"
        stats_text += f"• Tổng dòng: {total_lines}\n"
        stats_text += f"• ContentUID duy nhất: {unique_count}\n"
        stats_text += f"• ContentUID trùng: {duplicate_count}\n"
        if total_lines > 0:
            duplicate_percentage = (duplicate_count / unique_count) * 100 if unique_count > 0 else 0
            stats_text += f"• Tỷ lệ trùng: {duplicate_percentage:.1f}%"
        
        self.stats_label.config(text=stats_text)
    
    def extract_numeric_suffix(self, contentuid):
        """Extract numeric suffix from contentuid for smart sorting"""
        import re
        # Find the last number in the contentuid (e.g., "_1", "_10", "_11", "_2")
        match = re.search(r'_(\d+)$', contentuid)
        if match:
            return int(match.group(1))
        return 0
    
    def extract_content_lines(self, text):
        """Extract content lines from XML text"""
        content_pattern = r'<content\s+contentuid="([^"]+)"\s+version="[^"]+">([^<]*)</content>'
        lines = text.split('\n')
        content_lines = []
        
        for line in lines:
            match = re.search(content_pattern, line.strip())
            if match:
                contentuid = match.group(1)
                content = match.group(2)
                # Preserve the original line with all whitespace and formatting
                content_lines.append({
                    'original_line': line,
                    'contentuid': contentuid,
                    'content': content
                })
            else:
                # Keep non-content lines as is
                content_lines.append({
                    'original_line': line,
                    'contentuid': None,
                    'content': None
                })
        
        return content_lines
    
    def sort_content(self):
        """Sort the content based on selected criteria"""
        input_content = self.input_text.get(1.0, tk.END).strip()
        
        if not input_content:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập nội dung cần sắp xếp")
            return
        
        try:
            content_lines = self.extract_content_lines(input_content)
            
            # Separate content lines from non-content lines
            xml_content_lines = [line for line in content_lines if line['contentuid'] is not None]
            other_lines = [line for line in content_lines if line['contentuid'] is None]
            
            if not xml_content_lines:
                messagebox.showwarning("Cảnh báo", "Không tìm thấy dòng content XML nào để sắp xếp")
                return
            
            # Sort based on selected criteria
            sort_key = self.sort_by.get()
            reverse = self.sort_order.get() == "desc"
            
            if sort_key == "contentuid":
                xml_content_lines.sort(key=lambda x: x['contentuid'], reverse=reverse)
            elif sort_key == "contentuid_numeric":
                # Smart numeric sorting for contentuid
                xml_content_lines.sort(key=lambda x: (x['contentuid'].rsplit('_', 1)[0] if '_' in x['contentuid'] else x['contentuid'], 
                                                     self.extract_numeric_suffix(x['contentuid'])), 
                                     reverse=reverse)
            else:  # sort by content
                xml_content_lines.sort(key=lambda x: x['content'], reverse=reverse)
            
            # Reconstruct the text while preserving structure
            result_lines = []
            content_index = 0
            
            for line in content_lines:
                if line['contentuid'] is not None:
                    # Replace with sorted content line
                    if content_index < len(xml_content_lines):
                        result_lines.append(xml_content_lines[content_index]['original_line'])
                        content_index += 1
                else:
                    # Keep non-content lines in their original position
                    result_lines.append(line['original_line'])
            
            result_text = '\n'.join(result_lines)
            
            # Display result
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, result_text)
            self.output_text.config(state=tk.DISABLED)
            
            # Auto copy to clipboard
            pyperclip.copy(result_text)
            
            # Update statistics
            content_lines_for_stats = self.extract_content_lines(input_content)
            xml_content_lines_for_stats = [line for line in content_lines_for_stats if line['contentuid'] is not None]
            contentuid_count_for_stats = {}
            for line in xml_content_lines_for_stats:
                contentuid = line['contentuid']
                contentuid_count_for_stats[contentuid] = contentuid_count_for_stats.get(contentuid, 0) + 1
            duplicates_for_stats = sum(1 for count in contentuid_count_for_stats.values() if count > 1)
            self.update_statistics(len(xml_content_lines_for_stats), len(contentuid_count_for_stats), duplicates_for_stats)
            
            sort_type = "ContentUID (Text)" if sort_key == "contentuid" else "ContentUID (Số)" if sort_key == "contentuid_numeric" else "Nội dung"
            order_type = "tăng dần" if not reverse else "giảm dần"
            self.update_status(f"Đã sắp xếp theo {sort_type} ({order_type}) và copy vào clipboard")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi sắp xếp: {str(e)}")
    
    def copy_result(self):
        """Copy result to clipboard"""
        result_content = self.output_text.get(1.0, tk.END).strip()
        
        if not result_content:
            messagebox.showwarning("Cảnh báo", "Không có kết quả để copy")
            return
        
        try:
            pyperclip.copy(result_content)
            self.update_status("Đã copy kết quả vào clipboard")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể copy: {str(e)}")

def main():
    # Check if required packages are installed
    try:
        import pyperclip
    except ImportError as e:
        print(f"Thiếu thư viện: {e}")
        print("Vui lòng cài đặt:")
        print("pip install pyperclip")
        return
    
    root = tk.Tk()
    app = XMLSorterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

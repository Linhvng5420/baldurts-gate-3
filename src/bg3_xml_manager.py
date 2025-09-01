#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baldur's Gate 3 XML Manager - Simplified Version without backup/temp/logs
"""

import xml.etree.ElementTree as ET
import os
import re
import html
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
from datetime import datetime

class BG3XMLManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Baldur's Gate 3 XML Manager v2.0")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2b2b2b")
        
        # Setup variables
        self.setup_variables()
        
        # Create interface
        self.create_interface()
        
        # Load config
        self.load_config()
        
    def setup_variables(self):
        """Setup all tkinter variables"""
        self.eng_file_path = tk.StringVar()
        self.vie_file_path = tk.StringVar()
        
        # Default output directory to conflict folder
        self.output_dir = tk.StringVar(value="output/conflict")
        
        self.search_file_path = tk.StringVar()
        self.check_eng_path = tk.StringVar()
        self.check_merged_path = tk.StringVar()
        self.stats_file_path = tk.StringVar()
        self.keywords_entry = tk.StringVar()
        
        # Content version setting
        self.content_version = tk.StringVar(value="50")
        
        # Custom folder name for merge output
        self.custom_folder_name = tk.StringVar(value="")
        
        # Options
        self.preserve_version = tk.BooleanVar(value=False)
        self.merge_duplicates = tk.BooleanVar(value=True)
        self.show_notifications = tk.BooleanVar(value=True)
        self.theme_var = tk.StringVar(value="dark")
        self.case_sensitive = tk.BooleanVar()
        self.regex_search = tk.BooleanVar()
        self.search_in_uid = tk.BooleanVar()
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Sẵn sàng")
        
        # Config path
        self.config_path = "src/config.json"
        
    def create_interface(self):
        """Create main interface"""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(title_frame, text="🎮 Baldur's Gate 3 XML Manager v2.0", 
                 font=('Arial', 16, 'bold')).pack()
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_merge_tab()
        self.create_search_tab()
        self.create_check_tab()
        self.create_stats_tab()
        self.create_settings_tab()
        
        # Status bar
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        ttk.Label(self.status_bar, textvariable=self.status_text).pack(side=tk.LEFT)
        
        self.time_label = ttk.Label(self.status_bar, text="")
        self.time_label.pack(side=tk.RIGHT)
        self.update_clock()
        
    def create_merge_tab(self):
        """Tab gộp file XML"""
        merge_frame = ttk.Frame(self.notebook)
        self.notebook.add(merge_frame, text="🔄 Gộp File XML")
        
        # Header with help button
        header_frame = ttk.Frame(merge_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(header_frame, text="Gộp File XML", font=('Arial', 12, 'bold')).pack(side=tk.LEFT)
        ttk.Button(header_frame, text="❓ Hướng Dẫn", 
                  command=self.show_merge_help).pack(side=tk.RIGHT)
        
        # File selection
        file_section = ttk.LabelFrame(merge_frame, text="Chọn File", padding=10)
        file_section.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(file_section, text="File Bị Kiểm Tra:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_section, textvariable=self.eng_file_path, width=60).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(file_section, text="Chọn", command=self.select_eng_file).grid(row=0, column=2, pady=2)
        
        ttk.Label(file_section, text="File Lấy Mẫu KT:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_section, textvariable=self.vie_file_path, width=60).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(file_section, text="Chọn", command=self.select_vie_file).grid(row=1, column=2, pady=2)
        
        ttk.Label(file_section, text="Thư mục output:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_section, textvariable=self.output_dir, width=60).grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(file_section, text="Chọn", command=self.select_output_dir).grid(row=2, column=2, pady=2)
        
        ttk.Label(file_section, text="Tên thư mục con:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(file_section, textvariable=self.custom_folder_name, width=60, 
                 ).grid(row=3, column=1, padx=5, pady=2)
        ttk.Label(file_section, text="(tùy chọn)").grid(row=3, column=2, sticky=tk.W, pady=2)
        
        # Options
        options_section = ttk.LabelFrame(merge_frame, text="Tùy Chọn", padding=10)
        options_section.pack(fill=tk.X, padx=10, pady=5)
        ttk.Checkbutton(options_section, text="Gộp các mục trùng lặp", 
                   variable=self.merge_duplicates).grid(row=0, column=0, columnspan=2, sticky=tk.W)
        ttk.Checkbutton(options_section, text="Giữ Version ContenUI từ English.xml Gốc (Không chọn mặc định là giá trị bên dưới)", 
                   variable=self.preserve_version).grid(row=1, column=0, columnspan=2, sticky=tk.W)
        
        # Content version setting
        ttk.Label(options_section, text="Content Version mặc định:").grid(row=2, column=0, sticky=tk.W, pady=2)
        version_entry = ttk.Entry(options_section, textvariable=self.content_version, width=10)
        version_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        ttk.Label(options_section, text="(mặc định: 50)").grid(row=2, column=2, sticky=tk.W, pady=2)
        
        # Actions
        action_frame = ttk.Frame(merge_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(action_frame, text="🚀 Bắt Đầu Gộp", 
                  command=self.start_merge).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="📊 Xem Trước", 
                  command=self.preview_merge).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🔄 Reset", 
                  command=self.reset_merge).pack(side=tk.LEFT, padx=5)
        
        # Progress
        progress_section = ttk.LabelFrame(merge_frame, text="Tiến Trình", padding=10)
        progress_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_section, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        self.log_text = scrolledtext.ScrolledText(progress_section, height=10, 
                                                 bg="#1e1e1e", fg="#ffffff")
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def create_search_tab(self):
        """Tab tìm kiếm"""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="🔍 Tìm Kiếm")
        
        # Input section
        input_section = ttk.LabelFrame(search_frame, text="Tìm Kiếm", padding=10)
        input_section.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_section, text="File XML:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_section, textvariable=self.search_file_path, width=50).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(input_section, text="Chọn", command=self.select_search_file).grid(row=0, column=2, pady=2)
        
        ttk.Label(input_section, text="Từ khóa:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_section, textvariable=self.keywords_entry, width=50).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(input_section, text="🔍 Tìm", command=self.search_keywords).grid(row=1, column=2, pady=2)
        
        # Options
        search_options = ttk.LabelFrame(search_frame, text="Tùy Chọn", padding=10)
        search_options.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(search_options, text="Phân biệt chữ hoa/thường", 
                       variable=self.case_sensitive).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(search_options, text="Sử dụng Regex", 
                       variable=self.regex_search).grid(row=0, column=1, sticky=tk.W)
        ttk.Checkbutton(search_options, text="Tìm trong UID", 
                       variable=self.search_in_uid).grid(row=0, column=2, sticky=tk.W)
        
        # Results
        results_section = ttk.LabelFrame(search_frame, text="Kết Quả", padding=10)
        results_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("UID", "Version", "Text")
        self.search_tree = ttk.Treeview(results_section, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=200)
            
        scrollbar = ttk.Scrollbar(results_section, orient=tk.VERTICAL, command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar.set)
        
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_check_tab(self):
        """Tab kiểm tra dữ liệu"""
        check_frame = ttk.Frame(self.notebook)
        self.notebook.add(check_frame, text="🔍 Kiểm Tra")
        
        # Input
        input_section = ttk.LabelFrame(check_frame, text="File Kiểm Tra", padding=10)
        input_section.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(input_section, text="File gốc (ENG):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_section, textvariable=self.check_eng_path, width=50).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(input_section, text="Chọn", command=self.select_check_eng_file).grid(row=0, column=2, pady=2)
        
        ttk.Label(input_section, text="File đã gộp:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(input_section, textvariable=self.check_merged_path, width=50).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(input_section, text="Chọn", command=self.select_check_merged_file).grid(row=1, column=2, pady=2)
        
        ttk.Button(input_section, text="🔍 Kiểm Tra", 
                  command=self.check_lost_data).grid(row=2, column=1, pady=10)
        
        # Results
        results_section = ttk.LabelFrame(check_frame, text="Kết Quả", padding=10)
        results_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.check_results = scrolledtext.ScrolledText(results_section, height=20, 
                                                      bg="#1e1e1e", fg="#ffffff")
        self.check_results.pack(fill=tk.BOTH, expand=True, pady=5)
        
    def create_stats_tab(self):
        """Tab thống kê"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 Thống Kê")
        
        # Input
        info_section = ttk.LabelFrame(stats_frame, text="File Phân Tích", padding=10)
        info_section.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_section, text="File XML:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(info_section, textvariable=self.stats_file_path, width=50).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(info_section, text="Chọn", command=self.select_stats_file).grid(row=0, column=2, pady=2)
        ttk.Button(info_section, text="📊 Phân Tích", command=self.analyze_file).grid(row=0, column=3, padx=5, pady=2)        # Results
        stats_display = ttk.LabelFrame(stats_frame, text="Kết Quả", padding=10)
        stats_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.stats_text = scrolledtext.ScrolledText(stats_display, height=15, 
                                                   bg="#1e1e1e", fg="#ffffff")
        self.stats_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Tools
        tools_section = ttk.LabelFrame(stats_frame, text="Công Cụ", padding=10)
        tools_section.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(tools_section, text="📁 Mở Thư Mục Output", 
                  command=self.open_output_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(tools_section, text="🧹 BG3 Filter Tool", 
                  command=self.open_filter_tool).pack(side=tk.LEFT, padx=5)
    
    def open_filter_tool(self):
        """Mở BG3 Enhanced Filter Tool"""
        import subprocess
        try:
            # Try to run the enhanced filter tool
            subprocess.Popen([sys.executable, "src/bg3_filter_enhanced.py", "--help"], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở Filter Tool: {e}")
        
    def create_settings_tab(self):
        """Tab cài đặt"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="⚙️ Cài Đặt")
        
        # General
        general_section = ttk.LabelFrame(settings_frame, text="Cài Đặt", padding=10)
        general_section.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(general_section, text="Hiển thị thông báo", 
                       variable=self.show_notifications).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(general_section, text="Giao diện:").grid(row=1, column=0, sticky=tk.W, pady=2)
        theme_combo = ttk.Combobox(general_section, textvariable=self.theme_var, 
                                  values=["dark", "light"], state="readonly")
        theme_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Config buttons
        config_frame = ttk.Frame(settings_frame)
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(config_frame, text="💾 Lưu", 
                  command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_frame, text="🔄 Tải", 
                  command=self.load_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_frame, text="🗑️ Reset", 
                  command=self.reset_config).pack(side=tk.LEFT, padx=5)
    
    def update_clock(self):
        """Update clock"""
        current_time = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
        
    def log_message(self, message):
        """Log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_status(self, message):
        """Update status"""
        self.status_text.set(message)
    
    # File selection methods
    def select_eng_file(self):
        filename = filedialog.askopenfilename(
            title="Chọn file tiếng Anh",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.eng_file_path.set(filename)
            
    def select_vie_file(self):
        filename = filedialog.askopenfilename(
            title="Chọn file tiếng Việt",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.vie_file_path.set(filename)
            
    def select_output_dir(self):
        dirname = filedialog.askdirectory(title="Chọn thư mục output")
        if dirname:
            self.output_dir.set(dirname)
            
    def select_search_file(self):
        filename = filedialog.askopenfilename(
            title="Chọn file XML",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.search_file_path.set(filename)
            
    def select_check_eng_file(self):
        filename = filedialog.askopenfilename(
            title="Chọn file gốc",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.check_eng_path.set(filename)
            
    def select_check_merged_file(self):
        filename = filedialog.askopenfilename(
            title="Chọn file đã gộp",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.check_merged_path.set(filename)
            
    def select_stats_file(self):
        filename = filedialog.askopenfilename(
            title="Chọn file XML",
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filename:
            self.stats_file_path.set(filename)

    # Main functionality methods
    def start_merge(self):
        """Start merge process"""
        if not self.eng_file_path.get() or not self.vie_file_path.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn đủ file!")
            return
            
        # Run in thread
        thread = threading.Thread(target=self._merge_files)
        thread.daemon = True
        thread.start()
        
    def _merge_files(self):
        """Merge files in thread"""
        try:
            self.log_message("Bắt đầu gộp file...")
            self.progress_var.set(10)
            
            # Read files
            tree_eng = ET.parse(self.eng_file_path.get())
            tree_vie = ET.parse(self.vie_file_path.get())
            root_eng = tree_eng.getroot()
            root_vie = tree_vie.getroot()
            
            self.progress_var.set(30)
            
            # Create dictionaries
            vie_dict = {}
            for c in root_vie.findall("content"):
                uid = c.attrib["contentuid"]
                vie_dict[uid] = c
                
            self.progress_var.set(50)
            
            # Create output
            vh_root = ET.Element("contentList")
            vh_eng_root = ET.Element("contentList")
            
            matched = 0
            unmatched = 0
            
            for eng_content in root_eng.findall("content"):
                uid = eng_content.attrib["contentuid"]
                
                if uid in vie_dict:
                    # Use Vietnamese content
                    vie_content = vie_dict[uid]
                    # Use version from English if preserve_version is True, otherwise use custom version
                    version = eng_content.attrib["version"] if self.preserve_version.get() else self.content_version.get()
                    new_content = ET.Element("content", {
                        "contentuid": uid,
                        "version": str(version)  # Ensure version is string
                    })
                    # Properly handle text content with encoding
                    if vie_content.text:
                        new_content.text = str(vie_content.text).strip()
                    else:
                        new_content.text = ""
                    vh_root.append(new_content)
                    matched += 1
                else:
                    # Use English content
                    new_content = ET.Element("content")
                    # Copy all attributes properly
                    for attr_name, attr_value in eng_content.attrib.items():
                        new_content.set(attr_name, str(attr_value))
                    
                    # Properly handle text content with encoding
                    if eng_content.text:
                        new_content.text = str(eng_content.text).strip()
                    else:
                        new_content.text = ""
                    vh_eng_root.append(new_content)
                    unmatched += 1
                    
            self.progress_var.set(80)
            
            # Save files to output directory with custom folder
            output_dir = self.output_dir.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Create final output directory
            custom_folder = self.custom_folder_name.get().strip()
            if custom_folder:
                # Use custom folder name
                final_dir = os.path.join(output_dir, custom_folder)
            else:
                # Use timestamp as folder name if no custom name provided
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                final_dir = os.path.join(output_dir, f"merge_{timestamp}")
            
            if not os.path.exists(final_dir):
                os.makedirs(final_dir)
                
            vh_path = os.path.join(final_dir, "english_VH.xml")
            vh_eng_path = os.path.join(final_dir, "english_Not-VH.xml")
            
            # Write XML files with proper formatting
            def write_xml_file(root_element, file_path):
                """Write XML with proper formatting and encoding"""
                # Add proper indentation
                ET.indent(root_element, space="  ", level=0)
                
                # Create ElementTree and write
                tree = ET.ElementTree(root_element)
                tree.write(file_path, encoding="utf-8", xml_declaration=True, method="xml")
                
                # Verify the file was written correctly
                if os.path.exists(file_path):
                    self.log_message(f"✅ Đã lưu: {os.path.basename(file_path)}")
                else:
                    self.log_message(f"❌ Lỗi lưu: {os.path.basename(file_path)}")
            
            # Write both files
            write_xml_file(vh_root, vh_path)
            write_xml_file(vh_eng_root, vh_eng_path)
            
            self.progress_var.set(100)
            
            # Summary with file paths
            summary = f"✅ Hoàn thành!\n- Đã dịch: {matched:,}\n- Chưa dịch: {unmatched:,}\n- Lưu tại: {final_dir}"
            self.log_message(summary)
            
            if self.show_notifications.get():
                messagebox.showinfo("Hoàn thành", summary)
                
        except Exception as e:
            error_msg = f"❌ Lỗi: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Lỗi", error_msg)
        finally:
            self.progress_var.set(0)

    def preview_merge(self):
        """Preview merge results"""
        # Implementation for preview
        messagebox.showinfo("Xem trước", "Tính năng xem trước sẽ được triển khai sau")

    def reset_merge(self):
        """Reset merge form"""
        self.eng_file_path.set("")
        self.vie_file_path.set("")
        
        # Reset to default output directory
        self.output_dir.set("output/conflict")
        
        # Clear custom folder name
        self.custom_folder_name.set("")
        
        self.content_version.set("50")  # Reset content version to default
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set(0)

    def show_merge_help(self):
        """Show merge functionality help dialog"""
        help_window = tk.Toplevel(self.root)
        help_window.title("📖 Hướng Dẫn Sử Dụng - Gộp File XML")
        help_window.geometry("700x600")
        help_window.configure(bg="#2b2b2b")
        help_window.resizable(True, True)
        
        # Make it modal
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center the window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (help_window.winfo_width() // 2)
        y = (help_window.winfo_screenheight() // 2) - (help_window.winfo_height() // 2)
        help_window.geometry(f"+{x}+{y}")
        
        # Title
        title_frame = ttk.Frame(help_window)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(title_frame, text="📖 Hướng Dẫn Sử Dụng - Chức Năng Gộp File XML", 
                 font=('Arial', 14, 'bold')).pack()
        
        # Help content
        help_frame = ttk.Frame(help_window)
        help_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        help_text = scrolledtext.ScrolledText(help_frame, 
                                            wrap=tk.WORD,
                                            bg="#1e1e1e", 
                                            fg="#ffffff",
                                            font=('Consolas', 10))
        help_text.pack(fill=tk.BOTH, expand=True)
        
        help_content = """🔄 QUY TRÌNH GỘP FILE XML BALDUR'S GATE 3

═══════════════════════════════════════════════════════════════════

1️⃣ ĐỌCVÀ PHÂN TÍCH FILE

📂 Đọc file tiếng Anh bằng XML parser
   • Phân tích cấu trúc XML và trích xuất các phần tử <content>
   • Mỗi phần tử có 2 thuộc tính quan trọng: contentuid và version

📂 Đọc file tiếng Việt bằng XML parser  
   • Tương tự file tiếng Anh, phân tích và trích xuất các phần tử
   • Tạo dictionary từ file tiếng Việt với key là contentuid để tra cứu nhanh
   • Dictionary giúp tối ưu tốc độ so khớp từ O(n²) xuống O(n)

═══════════════════════════════════════════════════════════════════

2️⃣ QUÁ TRÌNH GỘP CHÍNH

🔄 Duyệt qua từng phần tử content trong file tiếng Anh
   • Với mỗi phần tử:
     
   🔑 Lấy contentuid làm khóa tra cứu
      Example: contentuid="h123abc456def789"
      
   🔍 Kiểm tra xem có bản dịch tiếng Việt tương ứng không
      • Tra cứu trong dictionary tiếng Việt bằng contentuid
      
   ✅ Nếu có bản dịch:
      • Sử dụng text tiếng Việt từ dictionary
      • Tạo phần tử mới với contentuid và version
      • Thêm vào file english_VH.xml (đã có bản dịch)
      • Tăng biến đếm "matched"
      
   ❌ Nếu không có bản dịch:
      • Giữ nguyên text tiếng Anh gốc
      • Thêm vào file english_Not-VH.xml (chưa có bản dịch)
      • Tăng biến đếm "unmatched"

═══════════════════════════════════════════════════════════════════

3️⃣ XỬ LÝ VERSION

⚙️ Có 2 chế độ xử lý version:

🔒 Nếu chọn "Giữ Version ContenUI từ English.xml Gốc":
   • Sử dụng version từ file tiếng Anh gốc
   • Đảm bảo tính tương thích với game gốc
   
🎯 Nếu không chọn (mặc định):
   • Đặt version theo giá trị tùy chỉnh (mặc định: "50")
   • Cho phép linh hoạt trong việc quản lý version

═══════════════════════════════════════════════════════════════════

4️⃣ LƯU KẾT QUẢ

📁 Tạo thư mục output nếu chưa tồn tại
   • Format: output/merge_YYYYMMDD_HHMM/
   • Example: output/merge_20250901_1430/

💾 Lưu 2 file kết quả:

📄 english_VH.xml:
   • Chứa các phần tử đã có bản dịch tiếng Việt
   • Ready để import vào game
   
📄 english_Not-VH.xml:
   • Chứa các phần tử chưa có bản dịch (vẫn là tiếng Anh)
   • Dùng để tham khảo hoặc dịch thêm

═══════════════════════════════════════════════════════════════════

📊 THỐNG KÊ KẾT QUẢ

✅ Đã dịch: {số lượng} phần tử
❌ Chưa dịch: {số lượng} phần tử
⏱️ Thời gian xử lý: tùy thuộc vào kích thước file

═══════════════════════════════════════════════════════════════════

💡 TIPS & LƯU Ý

🎯 Đảm bảo 2 file XML có cùng cấu trúc contentuid
🔄 Sử dụng backup trước khi thực hiện merge
⚡ File lớn có thể mất vài phút để xử lý
🎮 Test file kết quả trong game trước khi phát hành

═══════════════════════════════════════════════════════════════════"""

        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  # Make it read-only
        
        # Close button
        button_frame = ttk.Frame(help_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="✅ Đóng", 
                  command=help_window.destroy).pack(side=tk.RIGHT)
        
        # Focus on help window
        help_text.focus_set()

    def search_keywords(self):
        """Search keywords"""
        # Implementation for search
        messagebox.showinfo("Tìm kiếm", "Tính năng tìm kiếm sẽ được triển khai sau")

    def check_lost_data(self):
        """Check lost data"""
        # Implementation for check
        messagebox.showinfo("Kiểm tra", "Tính năng kiểm tra sẽ được triển khai sau")

    def analyze_file(self):
        """Analyze file"""
        # Implementation for analysis
        messagebox.showinfo("Phân tích", "Tính năng phân tích sẽ được triển khai sau")

    def open_output_folder(self):
        """Open output folder"""
        output_dir = self.output_dir.get()
        if os.path.exists(output_dir):
            os.startfile(output_dir)
        else:
            messagebox.showwarning("Cảnh báo", "Thư mục output không tồn tại!")

    # Config methods
    def save_config(self):
        """Save configuration"""
        try:
            config = {
                'output_dir': self.output_dir.get(),
                'show_notifications': self.show_notifications.get(),
                'theme': self.theme_var.get(),
                'preserve_version': self.preserve_version.get(),
                'merge_duplicates': self.merge_duplicates.get(),
                'content_version': self.content_version.get(),
                'custom_folder_name': self.custom_folder_name.get()
            }
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
            messagebox.showinfo("Thành công", "Đã lưu cấu hình!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu: {str(e)}")

    def load_config(self):
        """Load configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                self.output_dir.set(config.get('output_dir', "output/conflict"))
                self.show_notifications.set(config.get('show_notifications', True))
                self.theme_var.set(config.get('theme', 'dark'))
                self.preserve_version.set(config.get('preserve_version', False))
                self.merge_duplicates.set(config.get('merge_duplicates', True))
                self.content_version.set(config.get('content_version', '50'))
                self.custom_folder_name.set(config.get('custom_folder_name', ''))
                
        except Exception:
            # Use defaults if config doesn't exist or is corrupted
            pass

    def reset_config(self):
        """Reset configuration"""
        if messagebox.askyesno("Xác nhận", "Reset về cài đặt mặc định?"):
            try:
                if os.path.exists(self.config_path):
                    os.remove(self.config_path)
                    
                # Reset variables to default values
                self.output_dir.set("output/conflict")
                self.show_notifications.set(True)
                self.theme_var.set("dark")
                self.preserve_version.set(False)
                self.merge_duplicates.set(True)
                self.content_version.set("50")
                self.custom_folder_name.set("")
                
                messagebox.showinfo("Hoàn thành", "Đã reset!")
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi reset: {str(e)}")


def main():
    """Main function"""
    root = tk.Tk()
    app = BG3XMLManager(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
System Requirements Checker for BG3 XML Manager
Kiểm tra yêu cầu hệ thống cho BG3 XML Manager
"""

import sys
import os
import platform
import tkinter as tk
from tkinter import messagebox

def check_python_version():
    """Kiểm tra phiên bản Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        return False, f"Python {version.major}.{version.minor}.{version.micro}"
    return True, f"Python {version.major}.{version.minor}.{version.micro}"

def check_tkinter():
    """Kiểm tra Tkinter"""
    try:
        import tkinter
        import tkinter.ttk
        return True, "Tkinter có sẵn"
    except ImportError:
        return False, "Tkinter không được cài đặt"

def check_xml_support():
    """Kiểm tra hỗ trợ XML"""
    try:
        import xml.etree.ElementTree as ET
        return True, "XML ElementTree có sẵn"
    except ImportError:
        return False, "XML ElementTree không có sẵn"

def check_threading():
    """Kiểm tra hỗ trợ threading"""
    try:
        import threading
        return True, "Threading có sẵn"
    except ImportError:
        return False, "Threading không có sẵn"

def check_json_support():
    """Kiểm tra hỗ trợ JSON"""
    try:
        import json
        return True, "JSON có sẵn"
    except ImportError:
        return False, "JSON không có sẵn"

def check_file_permissions():
    """Kiểm tra quyền ghi file"""
    try:
        test_file = "test_permissions.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        return True, "Có quyền ghi file"
    except:
        return False, "Không có quyền ghi file"

def check_disk_space():
    """Kiểm tra dung lượng ổ cứng"""
    try:
        if platform.system() == "Windows":
            import shutil
            total, used, free = shutil.disk_usage(".")
            free_mb = free // (1024*1024)
            if free_mb < 100:  # Cần ít nhất 100MB
                return False, f"Dung lượng trống: {free_mb}MB (cần ít nhất 100MB)"
            return True, f"Dung lượng trống: {free_mb}MB"
        else:
            return True, "Không thể kiểm tra trên hệ điều hành này"
    except:
        return False, "Không thể kiểm tra dung lượng"

def get_system_info():
    """Lấy thông tin hệ thống"""
    return {
        "OS": f"{platform.system()} {platform.release()}",
        "Architecture": platform.machine(),
        "Processor": platform.processor() or "Unknown",
        "Python Path": sys.executable,
        "Working Directory": os.getcwd()
    }

def run_checks():
    """Chạy tất cả kiểm tra"""
    checks = [
        ("Python Version", check_python_version),
        ("Tkinter", check_tkinter),
        ("XML Support", check_xml_support),
        ("Threading", check_threading),
        ("JSON Support", check_json_support),
        ("File Permissions", check_file_permissions),
        ("Disk Space", check_disk_space)
    ]
    
    results = []
    all_passed = True
    
    print("🔍 KIỂM TRA YÊU CẦU HỆ THỐNG")
    print("=" * 50)
    
    for name, check_func in checks:
        try:
            passed, message = check_func()
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{name:<20}: {status} - {message}")
            results.append((name, passed, message))
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"{name:<20}: ❌ ERROR - {str(e)}")
            results.append((name, False, str(e)))
            all_passed = False
    
    print("\n📊 THÔNG TIN HỆ THỐNG")
    print("=" * 50)
    
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key:<20}: {value}")
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 TẤT CẢ KIỂM TRA THÀNH CÔNG!")
        print("Hệ thống của bạn sẵn sàng chạy BG3 XML Manager.")
    else:
        print("⚠️ MỘT SỐ KIỂM TRA THẤT BẠI!")
        print("Vui lòng khắc phục các vấn đề trước khi chạy ứng dụng.")
    
    return all_passed, results

def show_gui_report(all_passed, results):
    """Hiển thị báo cáo qua GUI"""
    try:
        root = tk.Tk()
        root.title("System Requirements Check")
        root.geometry("600x500")
        root.configure(bg="#2b2b2b")
        
        # Title
        title_label = tk.Label(root, text="🔍 Kiểm Tra Yêu Cầu Hệ Thống", 
                              font=("Arial", 16, "bold"), 
                              bg="#2b2b2b", fg="#ffffff")
        title_label.pack(pady=10)
        
        # Results frame
        results_frame = tk.Frame(root, bg="#2b2b2b")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Results text
        for name, passed, message in results:
            status_color = "#00ff00" if passed else "#ff0000"
            status_text = "✅ PASS" if passed else "❌ FAIL"
            
            result_label = tk.Label(results_frame, 
                                   text=f"{name}: {status_text} - {message}",
                                   font=("Consolas", 10),
                                   bg="#2b2b2b", fg=status_color,
                                   anchor="w")
            result_label.pack(fill=tk.X, pady=2)
        
        # Summary
        summary_color = "#00ff00" if all_passed else "#ff6600"
        summary_text = "🎉 Hệ thống sẵn sàng!" if all_passed else "⚠️ Cần khắc phục một số vấn đề"
        
        summary_label = tk.Label(root, text=summary_text,
                                font=("Arial", 12, "bold"),
                                bg="#2b2b2b", fg=summary_color)
        summary_label.pack(pady=10)
        
        # Buttons
        button_frame = tk.Frame(root, bg="#2b2b2b")
        button_frame.pack(pady=10)
        
        if all_passed:
            run_button = tk.Button(button_frame, text="🚀 Chạy BG3 XML Manager",
                                  command=lambda: run_main_app(root),
                                  font=("Arial", 12), bg="#4CAF50", fg="white")
            run_button.pack(side=tk.LEFT, padx=5)
        
        close_button = tk.Button(button_frame, text="Đóng",
                                command=root.quit,
                                font=("Arial", 12), bg="#f44336", fg="white")
        close_button.pack(side=tk.LEFT, padx=5)
        
        root.mainloop()
        
    except Exception as e:
        print(f"Không thể hiển thị GUI: {e}")

def run_main_app(root):
    """Chạy ứng dụng chính"""
    try:
        root.quit()
        root.destroy()
        import bg3_xml_manager
        bg3_xml_manager.main()
    except ImportError:
        messagebox.showerror("Lỗi", "Không tìm thấy file bg3_xml_manager.py!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chạy ứng dụng: {str(e)}")

def main():
    """Hàm main"""
    print("Baldur's Gate 3 XML Manager - System Requirements Checker")
    print("Đang kiểm tra yêu cầu hệ thống...\n")
    
    all_passed, results = run_checks()
    
    # Hỏi xem có muốn hiển thị GUI report không
    if '--gui' in sys.argv or (all_passed and '--no-gui' not in sys.argv):
        try:
            show_gui_report(all_passed, results)
        except:
            pass  # Fallback to console only
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

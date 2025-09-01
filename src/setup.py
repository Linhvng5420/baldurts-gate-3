#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Setup and Structure Manager for BG3 XML Manager
Quản lý cấu trúc dự án cho BG3 XML Manager
"""

import os
import json
from datetime import datetime

class ProjectSetup:
    def __init__(self):
        self.project_structure = {
            "directories": [
                "output",
                "data/input",
                "data/filtered",
                "data/wip"
            ],
            "files": {
                "src/config.json": self.create_default_config(),
                "src/project_info.json": self.create_project_info()
            }
        }
    
    def create_default_config(self):
        """Tạo file config mặc định"""
        return {
            "version": "2.0",
            "created": datetime.now().isoformat(),
            "settings": {
                "output_dir": "output",
                "auto_backup": False,
                "show_notifications": True,
                "theme": "dark",
                "create_backup": False,
                "preserve_version": False,
                "merge_duplicates": True
            },
            "paths": {
                "eng_file": "data/input/eng.xml",
                "vie_file": "data/input/vie.xml",
                "output_dir": "output"
            },
            "advanced": {
                "max_backup_files": 10,
                "auto_cleanup_temp": True,
                "log_level": "INFO",
                "chunk_size": 1000
            }
        }
    
    def create_project_info(self):
        """Tạo thông tin dự án"""
        return {
            "name": "Baldur's Gate 3 XML Manager",
            "version": "2.0",
            "description": "Công cụ quản lý và xử lý file XML cho dự án Việt hóa Baldur's Gate 3",
            "author": "BG3 Vietnam Team",
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "python_version": "3.6+",
            "dependencies": [
                "tkinter",
                "xml.etree.ElementTree",
                "threading",
                "json",
                "os",
                "shutil",
                "datetime"
            ],
            "features": [
                "Gộp file XML",
                "Tìm kiếm và lọc",
                "Kiểm tra dữ liệu bị mất",
                "Thống kê và phân tích",
                "Backup tự động",
                "Giao diện GUI"
            ]
        }
    
    def setup_project(self):
        """Thiết lập cấu trúc dự án"""
        print("🚀 THIẾT LẬP DỰ ÁN BG3 XML MANAGER")
        print("=" * 50)
        
        # Tạo thư mục
        for directory in self.project_structure["directories"]:
            try:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    print(f"✅ Đã tạo thư mục: {directory}")
                else:
                    print(f"📁 Thư mục đã tồn tại: {directory}")
            except Exception as e:
                print(f"❌ Lỗi tạo thư mục {directory}: {e}")
        
        # Tạo file
        for filename, content in self.project_structure["files"].items():
            try:
                if not os.path.exists(filename):
                    if filename.endswith('.json'):
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(content, f, indent=2, ensure_ascii=False)
                    else:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(content)
                    print(f"✅ Đã tạo file: {filename}")
                else:
                    print(f"📄 File đã tồn tại: {filename}")
            except Exception as e:
                print(f"❌ Lỗi tạo file {filename}: {e}")
        
        # Tạo file README trong thư mục con
        self.create_subdirectory_readme()
        
        print("\n🎉 THIẾT LẬP HOÀN TẤT!")
        print("Cấu trúc dự án đã được tạo thành công.")
    
    def create_subdirectory_readme(self):
        """Tạo file README cho các thư mục con"""
        readme_contents = {
            "data/input": """# 📁 Thư mục Input

Đặt các file XML gốc vào đây:

## 📄 File cần thiết:
- `eng.xml` - File tiếng Anh từ game (bản mới nhất)
- `vie.xml` - File tiếng Việt đã dịch (bản cũ)

## 📋 Lưu ý:
- File phải có định dạng XML hợp lệ
- Encoding: UTF-8
- Cấu trúc: `<contentList><content contentuid="..." version="...">text</content></contentList>`

## 🔧 Cách sử dụng:
1. Copy file từ game vào đây
2. Đảm bảo tên file đúng (eng.xml, vie.xml)
3. Chạy merge từ menu chính
""",
            "output": """# 📁 Thư mục Output

Chứa các file kết quả sau khi xử lý:

## 📄 File được tạo:
- `vh.xml` - Các mục đã được dịch
- `vh-eng.xml` - Các mục chưa được dịch
- `lost-eng.xml` - Dữ liệu bị mất (nếu có)
- `vh_merge.xml` - File gộp tổng

## 🎯 Sử dụng:
- File `vh.xml` dùng để import vào game
- File `lost-eng.xml` cần được xử lý thêm
- Tự động tạo bởi ứng dụng
""",
            "backup": """# 📁 Thư mục Backup

Chứa các file backup tự động:

## 📄 Format file:
- `{filename}_{timestamp}.xml`
- Tự động tạo trước khi merge
- Giới hạn: 10 file backup gần nhất

## 🔧 Quản lý:
- Tự động dọn dẹp file cũ
- Có thể xóa thủ công khi cần
""",
            "data/filtered": """# 📁 Thư mục Filtered

Chứa kết quả tìm kiếm và lọc XML:

## 📄 File được tạo:
- `{keyword}.xml` - File chứa entries có từ khóa
- `search_results_{timestamp}.xml` - Kết quả có timestamp

## 🔧 Cách tạo:
1. Sử dụng công cụ Search & Filter
2. Nhập từ khóa cần tìm
3. File kết quả sẽ được lưu tự động
""",
            "temp": """# 📁 Thư mục Temp

Chứa các file tạm thời:

## 📄 Nội dung:
- File xử lý trung gian
- Cache dữ liệu
- File log tạm thời

## 🧹 Dọn dẹp:
- Tự động xóa khi đóng ứng dụng
- Có thể dọn dẹp thủ công
"""
        }
        
        for directory, content in readme_contents.items():
            readme_path = os.path.join(directory, "README.md")
            try:
                if not os.path.exists(readme_path):
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Đã tạo README: {readme_path}")
            except Exception as e:
                print(f"❌ Lỗi tạo README {readme_path}: {e}")
    
    def check_project_structure(self):
        """Kiểm tra cấu trúc dự án"""
        print("🔍 KIỂM TRA CẤU TRÚC DỰ ÁN")
        print("=" * 50)
        
        missing_items = []
        
        # Kiểm tra thư mục
        for directory in self.project_structure["directories"]:
            if os.path.exists(directory):
                print(f"✅ Thư mục: {directory}")
            else:
                print(f"❌ Thiếu thư mục: {directory}")
                missing_items.append(directory)
        
        # Kiểm tra file
        required_files = ["src/bg3_xml_manager.py", "README.md", "run_bg3_manager.bat"]
        for filename in required_files:
            if os.path.exists(filename):
                print(f"✅ File: {filename}")
            else:
                print(f"❌ Thiếu file: {filename}")
                missing_items.append(filename)
        
        if missing_items:
            print(f"\n⚠️ Thiếu {len(missing_items)} mục. Chạy setup để tạo.")
            return False
        else:
            print("\n🎉 Cấu trúc dự án hoàn chỉnh!")
            return True
    
    def create_sample_files(self):
        """Tạo file mẫu"""
        print("📄 TẠO FILE MẪU")
        print("=" * 30)
        
        sample_xml = """<?xml version="1.0" encoding="utf-8"?>
<contentList>
    <content contentuid="h123456789" version="1">Sample English Text</content>
    <content contentuid="h987654321" version="1">Another Sample Text</content>
    <content contentuid="h555666777" version="1">Third Sample Entry</content>
</contentList>"""
        
        sample_vie_xml = """<?xml version="1.0" encoding="utf-8"?>
<contentList>
    <content contentuid="h123456789" version="50">Văn bản tiếng Việt mẫu</content>
    <content contentuid="h987654321" version="50">Văn bản mẫu khác</content>
</contentList>"""
        
        # Tạo file mẫu
        samples = {
            "file_goc/sample_eng.xml": sample_xml,
            "file_goc/sample_vie.xml": sample_vie_xml
        }
        
        for filepath, content in samples.items():
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Đã tạo: {filepath}")
            except Exception as e:
                print(f"❌ Lỗi tạo {filepath}: {e}")

def main():
    """Hàm main"""
    import sys
    
    setup = ProjectSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "setup":
            setup.setup_project()
        elif command == "check":
            setup.check_project_structure()
        elif command == "sample":
            setup.create_sample_files()
        elif command == "all":
            setup.setup_project()
            setup.create_sample_files()
            setup.check_project_structure()
        else:
            print("Sử dụng: python project_setup.py [setup|check|sample|all]")
    else:
        # Menu tương tác
        print("🎮 BG3 XML MANAGER - PROJECT SETUP")
        print("=" * 40)
        print("1. Thiết lập dự án (setup)")
        print("2. Kiểm tra cấu trúc (check)")
        print("3. Tạo file mẫu (sample)")
        print("4. Thực hiện tất cả (all)")
        print("0. Thoát")
        
        choice = input("\nChọn tùy chọn (0-4): ").strip()
        
        if choice == "1":
            setup.setup_project()
        elif choice == "2":
            setup.check_project_structure()
        elif choice == "3":
            setup.create_sample_files()
        elif choice == "4":
            setup.setup_project()
            setup.create_sample_files()
            setup.check_project_structure()
        elif choice == "0":
            print("Thoát.")
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()

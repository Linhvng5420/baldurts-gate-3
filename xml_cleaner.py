#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XML Cleaner - Xóa comment và dòng trống trong file XML
Giữ nguyên format XML và không thay đổi cấu trúc
"""

import re
import os
import sys
from pathlib import Path

def clean_xml_file(input_path, output_path=None):
    """
    Xóa comment và dòng trống từ file XML
    
    Args:
        input_path (str): Đường dẫn file XML đầu vào
        output_path (str, optional): Đường dẫn file XML đầu ra. Nếu None, sẽ ghi đè file gốc
    
    Returns:
        bool: True nếu thành công, False nếu có lỗi
    """
    try:
        # Kiểm tra file đầu vào có tồn tại không
        if not os.path.exists(input_path):
            print(f"❌ File không tồn tại: {input_path}")
            return False
        
        print(f"🔄 Đang xử lý file: {input_path}")
        
        # Đọc nội dung file
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Đếm số dòng ban đầu
        original_lines = len(content.splitlines())
        
        # Xóa comment XML (<!-- ... -->)
        # Sử dụng regex để tìm và xóa comment, bao gồm cả comment nhiều dòng
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Chia thành các dòng để xử lý
        lines = content.splitlines()
        
        # Xóa dòng trống hoàn toàn và dòng chỉ có khoảng trắng
        cleaned_lines = []
        for line in lines:
            # Giữ lại dòng nếu không phải là dòng trống hoàn toàn
            if line.strip():
                cleaned_lines.append(line)
        
        # Ghép lại thành nội dung hoàn chỉnh
        cleaned_content = '\n'.join(cleaned_lines)
        
        # Đảm bảo file kết thúc bằng newline
        if cleaned_content and not cleaned_content.endswith('\n'):
            cleaned_content += '\n'
        
        # Xác định đường dẫn output
        if output_path is None:
            output_path = input_path
        
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Ghi file đã làm sạch
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
        
        # Thống kê
        final_lines = len(cleaned_lines)
        removed_lines = original_lines - final_lines
        
        print(f"✅ Hoàn thành!")
        print(f"📊 Thống kê:")
        print(f"   - Dòng ban đầu: {original_lines:,}")
        print(f"   - Dòng sau khi làm sạch: {final_lines:,}")
        print(f"   - Dòng đã xóa: {removed_lines:,}")
        print(f"💾 File đã lưu tại: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi xử lý file: {str(e)}")
        return False

def clean_xml_batch(input_dir, output_dir=None, file_pattern="*.xml"):
    """
    Xử lý hàng loạt file XML trong thư mục
    
    Args:
        input_dir (str): Thư mục chứa file XML đầu vào
        output_dir (str, optional): Thư mục đầu ra. Nếu None, sẽ ghi đè file gốc
        file_pattern (str): Pattern để tìm file (mặc định: "*.xml")
    
    Returns:
        int: Số file đã xử lý thành công
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"❌ Thư mục không tồn tại: {input_dir}")
        return 0
    
    # Tìm tất cả file XML
    xml_files = list(input_path.glob(file_pattern))
    
    if not xml_files:
        print(f"❌ Không tìm thấy file XML nào trong: {input_dir}")
        return 0
    
    print(f"🔍 Tìm thấy {len(xml_files)} file XML")
    
    success_count = 0
    
    for xml_file in xml_files:
        print(f"\n{'='*60}")
        
        # Xác định đường dẫn output
        if output_dir:
            output_path = Path(output_dir) / xml_file.name
        else:
            output_path = xml_file
        
        # Xử lý file
        if clean_xml_file(str(xml_file), str(output_path)):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"🎉 Hoàn thành! Đã xử lý thành công {success_count}/{len(xml_files)} file")
    
    return success_count

def main():
    """Hàm main với giao diện command line"""
    
    print("🧹 XML Cleaner - Công cụ làm sạch file XML")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("💡 Cách sử dụng:")
        print("   python xml_cleaner.py <file_xml>")
        print("   python xml_cleaner.py <file_xml> <file_output>")
        print("   python xml_cleaner.py --batch <thư_mục>")
        print("   python xml_cleaner.py --batch <thư_mục_input> <thư_mục_output>")
        print("\n📝 Ví dụ:")
        print("   python xml_cleaner.py English.xml")
        print("   python xml_cleaner.py English.xml English_clean.xml")
        print("   python xml_cleaner.py --batch ./data/")
        print("   python xml_cleaner.py --batch ./input/ ./output/")
        return
    
    # Xử lý batch
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("❌ Thiếu đường dẫn thư mục input")
            return
        
        input_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        
        clean_xml_batch(input_dir, output_dir)
        
    # Xử lý file đơn lẻ
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        clean_xml_file(input_file, output_file)

if __name__ == "__main__":
    main()

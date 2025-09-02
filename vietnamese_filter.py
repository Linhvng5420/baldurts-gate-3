#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để lọc các dòng có tiếng Việt từ file XML
Tạo file mới chứa các dòng tiếng Việt và xóa chúng khỏi file gốc
"""

import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime

def has_vietnamese_chars(text, additional_keywords=None):
    """
    Kiểm tra xem text có chứa ký tự tiếng Việt hoặc từ khóa bổ sung không
    
    Args:
        text: Chuỗi cần kiểm tra
        additional_keywords: Danh sách các từ khóa bổ sung cần lọc
    """
    # Kiểm tra ký tự tiếng Việt
    vietnamese_pattern = r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]'
    has_viet_chars = bool(re.search(vietnamese_pattern, text))
    
    # Kiểm tra từ khóa bổ sung
    has_additional_keywords = False
    if additional_keywords:
        text_lower = text.lower()
        for keyword in additional_keywords:
            if keyword.lower() in text_lower:
                has_additional_keywords = True
                break
    
    return has_viet_chars or has_additional_keywords

def filter_vietnamese_content(input_file, vietnamese_output_file, remaining_output_file, additional_keywords=None):
    """
    Lọc nội dung tiếng Việt từ file XML
    
    Args:
        input_file: Đường dẫn file XML đầu vào
        vietnamese_output_file: File output chứa các dòng tiếng Việt
        remaining_output_file: File output chứa các dòng còn lại (không phải tiếng Việt)
        additional_keywords: Danh sách các từ khóa bổ sung cần lọc
    """
    try:
        # Parse XML file
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Tạo cấu trúc XML mới cho file tiếng Việt
        vietnamese_root = ET.Element("contentList")
        remaining_root = ET.Element("contentList")
        
        vietnamese_count = 0
        remaining_count = 0
        
        print(f"Đang xử lý file: {input_file}")
        print("Đang phân tích các content elements...")
        
        # Duyệt qua tất cả content elements
        for content in root.findall('content'):
            text = content.text if content.text else ""
            
            if has_vietnamese_chars(text, additional_keywords):
                # Có tiếng Việt hoặc từ khóa bổ sung - thêm vào file Vietnamese
                vietnamese_root.append(content)
                vietnamese_count += 1
            else:
                # Không có tiếng Việt - thêm vào file còn lại
                remaining_root.append(content)
                remaining_count += 1
        
        # Tạo file XML cho nội dung tiếng Việt
        vietnamese_tree = ET.ElementTree(vietnamese_root)
        vietnamese_tree.write(vietnamese_output_file, encoding='utf-8', xml_declaration=True)
        
        # Tạo file XML cho nội dung còn lại
        remaining_tree = ET.ElementTree(remaining_root)
        remaining_tree.write(remaining_output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"\n✅ Hoàn thành!")
        print(f"📊 Thống kê:")
        print(f"   - Tổng số entries: {vietnamese_count + remaining_count}")
        print(f"   - Entries có tiếng Việt: {vietnamese_count}")
        print(f"   - Entries không có tiếng Việt: {remaining_count}")
        print(f"\n📁 Files đã tạo:")
        print(f"   - File tiếng Việt: {vietnamese_output_file}")
        print(f"   - File còn lại: {remaining_output_file}")
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ Lỗi parse XML: {e}")
        return False
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    """
    Hàm main để thực thi script
    """
    # Nhập đường dẫn file từ người dùng
    print("🔍 Nhập đường dẫn file XML cần lọc:")
    input_file = input("Đường dẫn file: ").strip().strip('"')
    
    if not input_file:
        print("❌ Đường dẫn file không được để trống!")
        return
    
    # Nhập các từ khóa bổ sung cần lọc
    print("\n📝 Nhập các từ/câu bổ sung cần lọc (không chứa ký tự tiếng Việt):")
    print("   - Các từ/câu cách nhau bằng dấu phẩy (,)")
    print("   - Bỏ trống nếu không cần thêm từ khóa")
    print("   - Ví dụ: từ1, từ2, câu dài hơn")
    
    additional_input = input("Từ khóa bổ sung: ").strip()
    additional_keywords = []
    
    if additional_input:
        # Tách các từ khóa và làm sạch
        keywords = [keyword.strip() for keyword in additional_input.split(',')]
        additional_keywords = [keyword for keyword in keywords if keyword]
        
        if additional_keywords:
            print(f"✅ Đã thêm {len(additional_keywords)} từ khóa bổ sung:")
            for i, keyword in enumerate(additional_keywords, 1):
                print(f"   {i}. '{keyword}'")
        else:
            print("ℹ️  Không có từ khóa bổ sung nào được thêm")
    else:
        print("ℹ️  Không sử dụng từ khóa bổ sung")
    
    # Tạo tên file output với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Lấy tên file và thư mục từ đường dẫn input
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    base_name = os.path.splitext(input_filename)[0]
    
    vietnamese_output = os.path.join(input_dir, f"{base_name}_Vietnamese_{timestamp}.xml")
    remaining_output = os.path.join(input_dir, f"{base_name}_NonVietnamese_{timestamp}.xml")
    
    # Kiểm tra file đầu vào có tồn tại không
    if not os.path.exists(input_file):
        print(f"❌ File không tồn tại: {input_file}")
        return
    
    print("🚀 Bắt đầu lọc nội dung tiếng Việt...")
    print(f"📂 Input file: {input_file}")
    if additional_keywords:
        print(f"🔍 Từ khóa bổ sung: {', '.join(additional_keywords)}")
    
    # Thực hiện lọc
    success = filter_vietnamese_content(input_file, vietnamese_output, remaining_output, additional_keywords)
    
    if success:
        print("✅ Quá trình lọc hoàn tất! Hai file đã được tạo thành công.")

if __name__ == "__main__":
    main()

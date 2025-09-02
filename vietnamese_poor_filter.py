#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để lọc các dòng xml có cả tiếng việt và tiếng anh
Tạo file mới chứa các dòng tiếng Việt và tiếng Anh riêng biệt
Các dòng có dưới 5 từ tiếng Việt sẽ được tính là tiếng Anh
"""

import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime

def count_vietnamese_words(text):
    """
    Đếm số lượng từ tiếng Việt trong đoạn văn bản
    
    Args:
        text: Chuỗi cần kiểm tra
    
    Returns:
        Số lượng từ tiếng Việt
    """
    # Mẫu nhận dạng từ có ký tự tiếng Việt
    vietnamese_pattern = r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]'
    
    # Tách văn bản thành các từ (đơn giản hóa bằng cách tách theo khoảng trắng)
    words = text.split()
    
    # Đếm số từ có ký tự tiếng Việt
    vietnamese_words = 0
    for word in words:
        if re.search(vietnamese_pattern, word):
            vietnamese_words += 1
    
    return vietnamese_words

def has_vietnamese_chars(text):
    """
    Kiểm tra xem text có chứa ký tự tiếng Việt không
    
    Args:
        text: Chuỗi cần kiểm tra
    """
    vietnamese_pattern = r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]'
    return bool(re.search(vietnamese_pattern, text))

def filter_mixed_content(input_file, vietnamese_output_file, english_output_file, vietnamese_threshold=5):
    """
    Lọc nội dung XML thành file tiếng Việt và tiếng Anh
    
    Args:
        input_file: Đường dẫn file XML đầu vào
        vietnamese_output_file: File output chứa các dòng tiếng Việt
        english_output_file: File output chứa các dòng tiếng Anh
        vietnamese_threshold: Ngưỡng số từ tiếng Việt để xác định là nội dung tiếng Việt
    """
    try:
        # Parse XML file
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Tạo cấu trúc XML mới cho file tiếng Việt và tiếng Anh
        vietnamese_root = ET.Element("contentList")
        english_root = ET.Element("contentList")
        
        vietnamese_count = 0
        english_count = 0
        
        print(f"Đang xử lý file: {input_file}")
        print("Đang phân tích các content elements...")
        
        # Duyệt qua tất cả content elements
        for content in root.findall('content'):
            text = content.text if content.text else ""
            
            # Kiểm tra nếu có ký tự tiếng Việt
            if has_vietnamese_chars(text):
                # Đếm số từ tiếng Việt
                viet_word_count = count_vietnamese_words(text)
                
                # Nếu số từ tiếng Việt >= ngưỡng, xem là nội dung tiếng Việt
                if viet_word_count >= vietnamese_threshold:
                    vietnamese_root.append(content)
                    vietnamese_count += 1
                else:
                    english_root.append(content)
                    english_count += 1
            else:
                # Không có ký tự tiếng Việt - thêm vào file tiếng Anh
                english_root.append(content)
                english_count += 1
        
        # Tạo file XML cho nội dung tiếng Việt
        vietnamese_tree = ET.ElementTree(vietnamese_root)
        vietnamese_tree.write(vietnamese_output_file, encoding='utf-8', xml_declaration=True)
        
        # Tạo file XML cho nội dung tiếng Anh
        english_tree = ET.ElementTree(english_root)
        english_tree.write(english_output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"\n✅ Hoàn thành!")
        print(f"📊 Thống kê:")
        print(f"   - Tổng số entries: {vietnamese_count + english_count}")
        print(f"   - Entries tiếng Việt (>= {vietnamese_threshold} từ): {vietnamese_count}")
        print(f"   - Entries tiếng Anh (< {vietnamese_threshold} từ tiếng Việt): {english_count}")
        print(f"\n📁 Files đã tạo:")
        print(f"   - File tiếng Việt: {vietnamese_output_file}")
        print(f"   - File tiếng Anh: {english_output_file}")
        
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
    
    # Nhập ngưỡng từ tiếng Việt
    print("\n🔢 Nhập số lượng từ tiếng Việt tối thiểu để phân loại là nội dung tiếng Việt:")
    print("   - Mặc định: 5 từ")
    threshold_input = input("Số lượng từ (Enter để dùng mặc định): ").strip()
    
    vietnamese_threshold = 5  # Mặc định
    if threshold_input:
        try:
            vietnamese_threshold = int(threshold_input)
            print(f"✅ Đã đặt ngưỡng từ tiếng Việt là: {vietnamese_threshold}")
        except ValueError:
            print(f"⚠️ Giá trị không hợp lệ, dùng ngưỡng mặc định: {vietnamese_threshold}")
    else:
        print(f"ℹ️ Dùng ngưỡng mặc định: {vietnamese_threshold}")
    
    # Tạo tên file output với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Lấy tên file và thư mục từ đường dẫn input
    input_dir = os.path.dirname(input_file)
    input_filename = os.path.basename(input_file)
    base_name = os.path.splitext(input_filename)[0]
    
    vietnamese_output = os.path.join(input_dir, f"{base_name}_Vietnamese_{timestamp}.xml")
    english_output = os.path.join(input_dir, f"{base_name}_English_{timestamp}.xml")
    
    # Kiểm tra file đầu vào có tồn tại không
    if not os.path.exists(input_file):
        print(f"❌ File không tồn tại: {input_file}")
        return
    
    print("🚀 Bắt đầu lọc nội dung...")
    print(f"📂 Input file: {input_file}")
    print(f"🔍 Ngưỡng phân loại: >= {vietnamese_threshold} từ tiếng Việt = nội dung tiếng Việt")
    
    # Thực hiện lọc
    success = filter_mixed_content(input_file, vietnamese_output, english_output, vietnamese_threshold)
    
    if success:
        print("✅ Quá trình lọc hoàn tất! Hai file đã được tạo thành công.")
        print("   - Các dòng có >= {vietnamese_threshold} từ tiếng Việt được xếp vào file Vietnamese.")
        print("   - Các dòng còn lại được xếp vào file English.")

if __name__ == "__main__":
    main()

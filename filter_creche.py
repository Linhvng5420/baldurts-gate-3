#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để lọc các dòng chứa "Crèche" từ file XML
"""

import xml.etree.ElementTree as ET
import re
from datetime import datetime

def filter_creche_lines(input_file, output_file):
    """
    Lọc các dòng chứa từ "Crèche" từ file XML input và lưu vào file output
    """
    print(f"Đang đọc file: {input_file}")
    
    try:
        # Đọc file XML
        tree = ET.parse(input_file)
        root = tree.getroot()
        
        # Tạo XML mới
        new_root = ET.Element("contentList")
        
        # Đếm số dòng tìm thấy
        count = 0
        
        # Duyệt qua tất cả các thẻ content
        for content in root.findall('content'):
            text = content.text if content.text else ""
            
            # Kiểm tra xem có chứa "Crèche" không (không phân biệt hoa thường)
            if "crèche" in text.lower():
                # Thêm vào XML mới
                new_content = ET.SubElement(new_root, "content")
                new_content.set("contentuid", content.get("contentuid", ""))
                new_content.set("version", content.get("version", ""))
                new_content.text = content.text
                count += 1
                print(f"Tìm thấy: {text[:100]}...")
        
        # Tạo tree mới và ghi file
        new_tree = ET.ElementTree(new_root)
        
        # Ghi file với encoding UTF-8
        ET.indent(new_tree, space="\t", level=0)
        with open(output_file, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
            new_tree.write(f, encoding='utf-8', xml_declaration=False)
        
        print(f"\n✅ Hoàn thành! Đã lọc {count} dòng chứa 'Crèche'")
        print(f"📁 File output: {output_file}")
        
        return count
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return 0

def main():
    # Đường dẫn file input và output
    input_file = r"d:\Games\Baldurt's Gate VH\baldurts-gate-3\output\filtered\english_Vietnamese_20250902_094615.xml"
    
    # Tạo tên file output với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = rf"d:\Games\Baldurt's Gate VH\baldurts-gate-3\output\filtered\creche_lines_{timestamp}.xml"
    
    print("🔍 Bắt đầu lọc các dòng chứa 'Crèche'...")
    print("=" * 50)
    
    # Thực hiện lọc
    count = filter_creche_lines(input_file, output_file)
    
    if count > 0:
        print("=" * 50)
        print(f"📊 Tổng kết: {count} dòng đã được lọc thành công!")
    else:
        print("❌ Không tìm thấy dòng nào hoặc có lỗi xảy ra")

if __name__ == "__main__":
    main()

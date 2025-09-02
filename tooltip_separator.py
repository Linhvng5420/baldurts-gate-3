#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phân chia file XML theo từng vùng Tooltip
"""

import os
import re
import sys
import argparse
from collections import defaultdict
from datetime import datetime

def extract_tooltips_from_line(line):
    """Trích xuất tất cả tooltips từ một dòng XML"""
    tooltip_pattern = r'Tooltip="([^"]+)"'
    tooltips = re.findall(tooltip_pattern, line)
    return tooltips

def extract_text_content(line):
    """Trích xuất nội dung text từ dòng XML"""
    text_match = re.search(r'>([^<]*)', line)
    return text_match.group(1) if text_match else ""

def categorize_content_by_tooltips(input_file):
    """Phân loại nội dung theo tooltips"""
    tooltip_contents = defaultdict(list)
    
    print(f"Đang đọc file: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Tổng số dòng: {len(lines)}")
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if line.startswith('<content contentuid='):
            tooltips = extract_tooltips_from_line(line)
            
            if tooltips:
                # Nếu có nhiều tooltip trong một dòng, sử dụng tooltip đầu tiên làm chính
                primary_tooltip = tooltips[0]
                tooltip_contents[primary_tooltip].append({
                    'line': line,
                    'line_number': line_num,
                    'all_tooltips': tooltips
                })
            else:
                # Nội dung không có tooltip
                tooltip_contents['NO_TOOLTIP'].append({
                    'line': line,
                    'line_number': line_num,
                    'all_tooltips': []
                })
    
    return tooltip_contents

def save_tooltip_report(tooltip_contents, output_dir, sort_content=False):
    """Lưu file báo cáo thống kê tooltip và file XML phân nhóm theo tooltip"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Tạo file báo cáo duy nhất
    report_file = os.path.join(output_dir, f"tooltip_report_{timestamp}.txt")
    xml_file = os.path.join(output_dir, f"tooltip_separated_{timestamp}.xml")
    
    with open(report_file, 'w', encoding='utf-8') as report:
        report.write("=== BÁO CÁO PHÂN LOẠI TOOLTIP ===\n")
        report.write(f"Thời gian tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Tổng số tooltip khác nhau: {len(tooltip_contents)}\n")
        if sort_content:
            report.write("Nội dung được sắp xếp theo thứ tự a-z trong mỗi nhóm tooltip\n")
        report.write("\n")
        
        # Tính tổng số entries
        total_entries = sum(len(contents) for contents in tooltip_contents.values())
        report.write(f"Tổng số entries: {total_entries}\n\n")
        
        # Phân chia tooltip theo số lượng entries
        large_tooltips = []  # >= 5 entries
        small_tooltips = []  # < 5 entries
        small_tooltip_contents = []  # Gộp tất cả contents của small tooltips
        
        for tooltip, contents in tooltip_contents.items():
            if len(contents) >= 5:
                large_tooltips.append((tooltip, contents))
            else:
                small_tooltips.append((tooltip, contents))
                small_tooltip_contents.extend(contents)
        
        # Sắp xếp large tooltips theo số lượng từ ít đến nhiều
        large_tooltips.sort(key=lambda x: len(x[1]))
        
        # Sắp xếp small tooltips theo số lượng từ ít đến nhiều
        small_tooltips.sort(key=lambda x: len(x[1]))
        
        report.write("=== THỐNG KÊ THEO TOOLTIP ===\n")
        
        # Hiển thị tooltips lớn (>= 5 entries)
        if large_tooltips:
            report.write("--- Tooltips có từ 5 entries trở lên ---\n")
            for i, (tooltip, contents) in enumerate(large_tooltips, 1):
                count = len(contents)
                percentage = (count / total_entries * 100) if total_entries > 0 else 0
                report.write(f"{i:2d}. {tooltip:<25} | {count:4d} entries ({percentage:5.1f}%)\n")
        
        # Hiển thị nhóm tooltips nhỏ (< 5 entries) - gộp chung cho gọn
        if small_tooltips:
            small_total = len(small_tooltip_contents)
            small_percentage = (small_total / total_entries * 100) if total_entries > 0 else 0
            report.write("\n--- Tooltips có ít hơn 5 entries (gộp chung) ---\n")
            report.write(f"    NHÓM_TOOLTIP_NHỎ         | {small_total:4d} entries ({small_percentage:5.1f}%)\n")
            
            # Chỉ hiển thị tổng số và một vài ví dụ đầu tiên cho gọn
            report.write("    Bao gồm:\n")
            # Hiển thị tối đa 10 tooltip đầu tiên
            for tooltip, contents in small_tooltips[:10]:
                count = len(contents)
                report.write(f"      - {tooltip:<30} | {count:2d} entries\n")
            
            if len(small_tooltips) > 10:
                report.write(f"      ... và {len(small_tooltips) - 10} tooltips khác\n")
        
        report.write("\n" + "="*70 + "\n")
        report.write("=== CHI TIẾT TỪNG TOOLTIP ===\n\n")
        
        # Chi tiết cho large tooltips
        if large_tooltips:
            report.write("--- CHI TIẾT TOOLTIPS LỚN (>= 5 entries) ---\n\n")
            for tooltip, contents in large_tooltips:
                count = len(contents)
                report.write(f"[{tooltip}] - {count} entries:\n")
                report.write("-" * 50 + "\n")
                
                # Hiển thị tối đa 10 ví dụ đầu tiên
                # Sắp xếp dữ liệu nếu cần
                contents_to_show = contents
                if sort_content:
                    contents_to_show = sorted(contents, key=lambda x: extract_text_content(x['line']).lower())
                
                for i, content in enumerate(contents_to_show[:10]):
                    uid = re.search(r'contentuid="([^"]+)"', content['line'])
                    uid_text = uid.group(1) if uid else "N/A"
                    
                    # Lấy text content (phần sau >)
                    text_content = extract_text_content(content['line'])
                    text_display = text_content[:50] + "..." if len(text_content) > 50 else text_content
                    
                    report.write(f"  {i+1:2d}. UID: {uid_text:<30} | Text: {text_display}\n")
                
                if len(contents) > 10:
                    report.write(f"  ... và {len(contents) - 10} entries khác\n")
                
                report.write("\n")
        
        # Chi tiết cho small tooltips (gộp chung) - rút gọn
        if small_tooltips:
            report.write("--- CHI TIẾT TOOLTIPS NHỎ (< 5 entries) ---\n\n")
            report.write(f"[NHÓM_TOOLTIP_NHỎ] - {len(small_tooltip_contents)} entries tổng cộng:\n")
            report.write("-" * 50 + "\n")
            
            # Chỉ hiển thị 20 tooltip đầu tiên với 1 ví dụ mỗi tooltip
            for tooltip, contents in small_tooltips[:20]:
                count = len(contents)
                report.write(f"\n  >>> {tooltip} ({count} entries):\n")
                
                # Chỉ hiển thị 1 ví dụ đầu tiên
                # Sắp xếp nếu cần
                if sort_content:
                    content = sorted(contents, key=lambda x: extract_text_content(x['line']).lower())[0]
                else:
                    content = contents[0]
                
                uid = re.search(r'contentuid="([^"]+)"', content['line'])
                uid_text = uid.group(1) if uid else "N/A"
                
                # Lấy text content (phần sau >)
                text_content = extract_text_content(content['line'])
                text_display = text_content[:40] + "..." if len(text_content) > 40 else text_content
                
                report.write(f"    1. UID: {uid_text:<25} | Text: {text_display}\n")
                if count > 1:
                    report.write(f"       ... và {count - 1} entries khác\n")
            
            if len(small_tooltips) > 20:
                report.write(f"\n  ... và {len(small_tooltips) - 20} tooltips khác\n")
            
            report.write("\n")
    
    # Tạo file XML với các tooltip được nhóm theo comment
    with open(xml_file, 'w', encoding='utf-8') as xml_out:
        xml_out.write('<?xml version="1.0" encoding="utf-8"?>\n')
        xml_out.write('<contentList>\n')
        
        # Xuất large tooltips trước
        for tooltip, contents in large_tooltips:
            count = len(contents)
            xml_out.write(f'    <!-- Pattern: {tooltip} - {count} entries -->\n')
            
            # Sắp xếp nội dung theo thứ tự alphabet nếu được yêu cầu
            if sort_content:
                # Tạo bản sao nội dung để sắp xếp
                contents_to_write = sorted(contents, key=lambda x: extract_text_content(x['line']).lower())
                for content in contents_to_write:
                    xml_out.write(f'\t{content["line"]}\n')
            else:
                for content in contents:
                    xml_out.write(f'\t{content["line"]}\n')
        
        # Xuất small tooltips theo nhóm
        if small_tooltips:
            # Gộp tất cả small tooltips vào một comment
            total_small = len(small_tooltip_contents)
            xml_out.write(f'    <!-- Pattern: TOOLTIP_NHỎ - {total_small} entries -->\n')
            
            # Sắp xếp nội dung nhỏ nếu được yêu cầu
            if sort_content:
                # Tạo bản sao nội dung để sắp xếp
                small_contents_to_write = sorted(small_tooltip_contents, key=lambda x: extract_text_content(x['line']).lower())
                for content in small_contents_to_write:
                    xml_out.write(f'\t{content["line"]}\n')
            else:
                for content in small_tooltip_contents:
                    xml_out.write(f'\t{content["line"]}\n')
        
        xml_out.write('</contentList>\n')
    
    sort_status = "đã sắp xếp theo thứ tự a-z" if sort_content else "theo thứ tự gốc"
    print(f"Đã tạo file báo cáo: {report_file}")
    print(f"Đã tạo file XML ({sort_status}): {xml_file}")
    return report_file, xml_file

def main():
    # Thiết lập argument parser
    parser = argparse.ArgumentParser(description='Phân chia file XML theo từng vùng Tooltip')
    parser.add_argument('input_file', nargs='?', 
                       help='Đường dẫn file XML đầu vào')
    parser.add_argument('-o', '--output', 
                       help='Thư mục output (mặc định: output/tooltip_separated)')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Chế độ tương tác (nhập đường dẫn thủ công)')
    parser.add_argument('--sort', '-s', action='store_true',
                       help='Sắp xếp nội dung theo thứ tự a-z trong mỗi nhóm tooltip')
    
    args = parser.parse_args()
    
    # Xác định file input
    if args.input_file:
        input_file = args.input_file
    elif args.interactive:
        # Chế độ tương tác
        print("=== TOOLTIP SEPARATOR ===")
        print("Nhập đường dẫn file XML cần phân tích:")
        input_file = input().strip()
        
        # Xử lý đường dẫn có dấu ngoặc kép
        if input_file.startswith('"') and input_file.endswith('"'):
            input_file = input_file[1:-1]
    else:
        # Đường dẫn mặc định (để tương thích ngược)
        input_file = r"d:\Games\Baldurt's Gate VH\baldurts-gate-3\output\filtered\temp.xml"
    
    # Xác định thư mục output
    if args.output:
        output_dir = args.output
    elif args.interactive:
        print("Nhập thư mục output (Enter để dùng mặc định):")
        user_output = input().strip()
        if user_output:
            # Xử lý đường dẫn có dấu ngoặc kép
            if user_output.startswith('"') and user_output.endswith('"'):
                user_output = user_output[1:-1]
            output_dir = user_output
        else:
            output_dir = r"d:\Games\Baldurt's Gate VH\baldurts-gate-3\output\tooltip_separated"
    else:
        output_dir = r"d:\Games\Baldurt's Gate VH\baldurts-gate-3\output\tooltip_separated"
    
    # Kiểm tra file tồn tại
    # Chuyển đổi đường dẫn tương đối thành đường dẫn tuyệt đối
    input_file = os.path.abspath(input_file)
    
    if not os.path.exists(input_file):
        print(f"Lỗi: Không tìm thấy file {input_file}")
        if args.interactive:
            input("Nhấn Enter để thoát...")
        return 1
    
    # Xác định tùy chọn sắp xếp
    should_sort = args.sort
    if args.interactive and not should_sort:
        print("Sắp xếp nội dung theo thứ tự a-z trong mỗi nhóm tooltip? (y/n, mặc định: n):")
        sort_response = input().strip().lower()
        should_sort = sort_response in ('y', 'yes', 'có', 'co')
    
    print(f"File input: {input_file}")
    print(f"Thư mục output: {output_dir}")
    print(f"Sắp xếp nội dung: {'Có' if should_sort else 'Không'}")
    print("Bắt đầu phân tích tooltip...")
    
    try:
        # Phân loại nội dung theo tooltip
        tooltip_contents = categorize_content_by_tooltips(input_file)
        
        print(f"\nĐã tìm thấy {len(tooltip_contents)} tooltip khác nhau")
        
        # Lưu file báo cáo
        report_file, xml_file = save_tooltip_report(tooltip_contents, output_dir, should_sort)
        
        print("\n=== HOÀN THÀNH ===")
        print(f"File báo cáo đã được tạo: {report_file}")
        print(f"File XML đã được tạo: {xml_file}")
        
        if args.interactive:
            input("Nhấn Enter để thoát...")
        
        return 0
        
    except Exception as e:
        print(f"Lỗi: {str(e)}")
        if args.interactive:
            input("Nhấn Enter để thoát...")
        return 1

if __name__ == "__main__":
    sys.exit(main())

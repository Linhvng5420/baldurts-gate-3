#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search-Tool-UI.py - Giao diện người dùng cho công cụ tìm kiếm và xử lý file XML
"""

import os
import re
import time
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import sys
import json
from io import StringIO
# Define functions
def tim_kiem_noi_dung(file_path, search_pattern):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Phân tách từ khóa tìm kiếm bằng dấu phẩy (giữ nguyên khoảng trắng)
        search_keywords = [keyword for keyword in search_pattern.split(',')]
        
        print(f"🔍 Đang tìm kiếm với {len(search_keywords)} từ khóa:")
        for i, keyword in enumerate(search_keywords, 1):
            print(f"   {i}. '{keyword}'")
        print()
        
        # Tìm tất cả các phần tử content trong file XML với format chính xác
        # Pattern để tìm content với cấu trúc chính xác, bao gồm tab và xuống dòng
        pattern = r'(\t<content[^>]*>.*?</content>)'
        content_elements = re.finditer(pattern, content, re.DOTALL)
        matches = []
        matches_by_keyword = {keyword: [] for keyword in search_keywords}
        
        for element in content_elements:
            full_element = element.group(1)  # Lấy toàn bộ phần tử bao gồm tab
            # Kiểm tra từng từ khóa trong toàn bộ dòng XML
            for keyword in search_keywords:
                if keyword.lower() in full_element.lower():
                    if full_element not in matches:  # Tránh trùng lặp
                        matches.append(full_element)
                    matches_by_keyword[keyword].append(full_element)
        
        if matches:
            print(f"✅ Đã tìm thấy {len(matches)} kết quả tổng cộng trong toàn bộ dòng XML:")
            
            # Hiển thị thống kê theo từng từ khóa
            print("\n📊 Thống kê theo từng từ khóa:")
            for keyword in search_keywords:
                count = len(matches_by_keyword[keyword])
                print(f"   '{keyword}': {count} kết quả")
            print()
            
            for i, match in enumerate(matches, 1):
                # Hiển thị contentuid để dễ nhận biết
                uid_match = re.search(r'contentuid="([^"]+)"', match)
                if uid_match:
                    print(f"\n📄 Kết quả {i} (UID: {uid_match.group(1)}):")
                else:
                    print(f"\n📄 Kết quả {i}:")
                
                # Tìm từ khóa nào khớp với kết quả này
                matched_keywords = []
                for keyword in search_keywords:
                    if keyword.lower() in match.lower():
                        matched_keywords.append(keyword)
                
                if matched_keywords:
                    keywords_str = ', '.join([f"'{kw}'" for kw in matched_keywords])
                    print(f"🎯 Khớp với từ khóa: {keywords_str}")
                
                # Highlight từ khóa tìm thấy trong preview
                preview = match.strip()
                preview_lower = preview.lower()
                
                # Highlight tất cả từ khóa tìm thấy
                highlighted_preview = preview
                for keyword in matched_keywords:
                    keyword_lower = keyword.lower()
                    if keyword_lower in preview_lower:
                        # Tìm vị trí chính xác của từ khóa (giữ nguyên case)
                        start_idx = preview_lower.find(keyword_lower)
                        if start_idx != -1:
                            end_idx = start_idx + len(keyword)
                            found_text = preview[start_idx:end_idx]
                            highlighted_preview = highlighted_preview.replace(found_text, f"🔍[{found_text}]🔍", 1)
                
                # Rút gọn nếu quá dài
                if len(highlighted_preview) > 200:
                    highlighted_preview = highlighted_preview[:200] + "..."
                
                print(highlighted_preview)
        else:
            print("❌ Không tìm thấy kết quả nào.")
        
        return matches
    except Exception as e:
        print(f"❌ Lỗi khi tìm kiếm: {str(e)}")
        return []

def xuat_ket_qua_ra_xml(ket_qua, file_path, search_content):
    try:
        # Tạo thư mục output trong thư mục gốc của project
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))  # Lên 2 cấp từ src/Search Tool
        output_dir = os.path.join(project_root, "output")
        
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Tạo timestamp để tránh trùng tên
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Tạo tên file output với từ khóa tìm kiếm (loại bỏ ký tự đặc biệt)
        search_safe = re.sub(r'[^\w\s-]', '', search_content).strip()
        search_safe = re.sub(r'[-\s]+', '_', search_safe)[:10]
        
        output_filename = f"{base_name}_search_{search_safe}_{timestamp}.xml"
        output_path = os.path.join(output_dir, output_filename)
        
        # Xuất file XML với cấu trúc đúng và nội dung đầy đủ
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n')
            file.write('<contentList>\n')
            
            for item in ket_qua:
                # Đảm bảo item có tab đầu dòng đúng format
                if item.strip().startswith('<content'):
                    # Thêm tab đầu dòng nếu chưa có
                    if not item.startswith('\t'):
                        file.write(f'\t{item.strip()}\n')
                    else:
                        file.write(f'{item.rstrip()}\n')
                else:
                    # Nếu không phải content tag thì thêm tab
                    file.write(f'\t{item.strip()}\n')
                    
            file.write('</contentList>')
        
        print(f"💾 Đã xuất {len(ket_qua)} kết quả ra file XML:")
        print(f"📁 {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Lỗi khi xuất file: {str(e)}")
        return None

def xoa_noi_dung(file_path, contents_to_remove):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Lấy contentuid của các phần tử cần xóa
        content_uids_to_remove = set()
        for item in contents_to_remove:
            match = re.search(r'contentuid="([^"]+)"', item)
            if match:
                content_uids_to_remove.add(match.group(1))

        print(f"🎯 Sẽ xóa {len(content_uids_to_remove)} ContentUID:")
        for uid in content_uids_to_remove:
            print(f"   - {uid}")

        # Đếm số phần tử trước khi xóa
        before_count = len(re.findall(r'<content[^>]*>', content))

        # Tìm và xóa các phần tử content có UID trong danh sách
        def replace_content(match):
            full_match = match.group(0)
            uid_search = re.search(r'contentuid="([^"]+)"', full_match)
            if uid_search and uid_search.group(1) in content_uids_to_remove:
                return ""  # Xóa phần tử này
            return full_match  # Giữ nguyên phần tử này

        # Pattern để match toàn bộ dòng content (bao gồm tab và xuống dòng)
        pattern = r'(\s*<content[^>]*>.*?</content>\s*)'
        new_content = re.sub(pattern, replace_content, content, flags=re.DOTALL)

        # Đếm số phần tử sau khi xóa
        after_count = len(re.findall(r'<content[^>]*>', new_content))
        deleted_count = before_count - after_count

        # Ghi lại file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print(f"✅ Đã xóa {deleted_count} phần tử khỏi file.")
        print(f"📊 Thống kê: {before_count} → {after_count} phần tử")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi xóa nội dung: {str(e)}")
        return False

def phan_tich_file_xml(file_path):
    try:
        # Lấy thông tin file
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size
        file_name = os.path.basename(file_path)
        
        # Chuyển đổi timestamp thành ngày tháng dễ đọc
        file_created = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(file_stat.st_ctime))
        file_modified = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(file_stat.st_mtime))
        
        print(f"📁 Tên file: {file_name}")
        print(f"📅 Ngày tạo: {file_created}")
        print(f"📅 Ngày sửa đổi: {file_modified}")
        print(f"📊 Kích thước: {file_size:,} bytes ({file_size/1024:.2f} KB)")
        print()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Phân tích nội dung file
        lines = content.split('\n')
        total_lines = len(lines)
        
        # Đếm số dòng content
        content_elements = re.findall(r'<content.*?</content>', content, re.DOTALL)
        content_lines = len(content_elements)
        
        # Đếm số dòng có comment (<!-- ... -->)
        comment_lines = 0
        for line in lines:
            if '<!--' in line or '-->' in line:
                comment_lines += 1
        
        # Đếm số dòng trống
        empty_lines = 0
        for line in lines:
            if line.strip() == '':
                empty_lines += 1
        
        # Đếm các dòng có nội dung thực (không trống, không phải comment)
        content_real_lines = total_lines - empty_lines - comment_lines
        
        print(f"📋 Thống kê nội dung file:")
        print(f"   • Tổng số dòng: {total_lines:,}")
        print(f"   • Số dòng content: {content_lines:,}")
        print(f"   • Số dòng có comment: {comment_lines:,}")
        print(f"   • Số dòng trống: {empty_lines:,}")
        print(f"   • Số dòng có nội dung thực: {content_real_lines:,}")
        print()
        
        # Phân tích thêm về cấu trúc XML
        contentlist_count = content.count('<contentList>')
        if contentlist_count > 0:
            print(f"📦 Cấu trúc XML:")
            print(f"   • Số thẻ <contentList>: {contentlist_count}")
            
            # Tìm các contentuid duy nhất
            contentuid_list = re.findall(r'contentuid="([^"]*)"', content)
            unique_uids = set(contentuid_list)
            duplicate_uids = len(contentuid_list) - len(unique_uids)
            
            print(f"   • Tổng ContentUID: {len(contentuid_list):,}")
            print(f"   • ContentUID duy nhất: {len(unique_uids):,}")
            if duplicate_uids > 0:
                print(f"   • ContentUID trùng lặp: {duplicate_uids:,}")
        
        return {
            'total_lines': total_lines,
            'content_lines': content_lines,
            'comment_lines': comment_lines,
            'empty_lines': empty_lines,
            'content_real_lines': content_real_lines,
            'file_size': file_size,
            'content_elements': content_elements
        }
    except Exception as e:
        print(f"❌ Lỗi khi phân tích file: {str(e)}")
        return None

def chia_file_xml(file_path, content_per_file):
    """
    Chia file XML thành nhiều file nhỏ với số lượng content elements được chỉ định
    
    Args:
        file_path (str): Đường dẫn đến file XML gốc
        content_per_file (int): Số lượng content elements mỗi file
        
    Returns:
        list: Danh sách đường dẫn các file đã tạo
    """
    try:
        print(f"📂 Đang đọc file: {os.path.basename(file_path)}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Tìm tất cả content elements với format chính xác
        pattern = r'(\t<content[^>]*>.*?</content>)'
        content_elements = re.findall(pattern, content, re.DOTALL)
        
        if not content_elements:
            print("❌ Không tìm thấy content elements nào trong file!")
            return []
        
        total_elements = len(content_elements)
        print(f"📊 Tổng số content elements: {total_elements:,}")
        print(f"📋 Chia mỗi file: {content_per_file:,} elements")
        
        # Tính số file cần tạo
        total_files = (total_elements + content_per_file - 1) // content_per_file
        print(f"📁 Số file sẽ tạo: {total_files}")
        
        # Tạo thư mục output
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        output_dir = os.path.join(project_root, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Tạo timestamp để tránh trùng tên
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        created_files = []
        
        # Lấy header và footer của file gốc
        header_match = re.search(r'^(.*?<contentList>\s*)', content, re.DOTALL)
        footer_match = re.search(r'(\s*</contentList>.*?)$', content, re.DOTALL)
        
        header = header_match.group(1) if header_match else '<?xml version="1.0" encoding="utf-8"?>\n<contentList>\n'
        footer = footer_match.group(1) if footer_match else '\n</contentList>'
        
        print("\n🔄 Đang tạo các file...")
        
        for i in range(total_files):
            start_idx = i * content_per_file
            end_idx = min(start_idx + content_per_file, total_elements)
            
            # Lấy content elements cho file này
            file_elements = content_elements[start_idx:end_idx]
            
            # Tạo tên file
            file_number = i + 1
            output_filename = f"{base_name}_part_{file_number:03d}_of_{total_files:03d}_{timestamp}.xml"
            output_path = os.path.join(output_dir, output_filename)
            
            # Tạo nội dung file
            file_content = header
            for element in file_elements:
                file_content += element + '\n'
            file_content += footer
            
            # Ghi file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(file_content)
            
            created_files.append(output_path)
            
            print(f"✅ File {file_number:3d}/{total_files}: {output_filename} ({len(file_elements):,} elements)")
        
        print(f"\n🎉 Chia file hoàn tất!")
        print(f"📁 Tạo thành công {len(created_files)} file trong thư mục output")
        print(f"📊 Tổng {total_elements:,} elements được chia đều")
        
        return created_files
        
    except Exception as e:
        print(f"❌ Lỗi khi chia file: {str(e)}")
        return []

def tim_contentuid_trung_lap_trong_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            contentuid_list = re.findall(r'contentuid="([^"]*)"', content)
            duplicates = {x for x in contentuid_list if contentuid_list.count(x) > 1}
            return list(duplicates)
    except Exception as e:
        print(f"Lỗi khi tìm ContentUID trùng lặp: {str(e)}")
        return []

def so_sanh_hai_file_xml(file1_path, file2_path):
    try:
        print(f"📖 Đang đọc File A: {os.path.basename(file1_path)}")
        with open(file1_path, 'r', encoding='utf-8') as file1:
            content1 = file1.read()
            
        print(f"📖 Đang đọc File B: {os.path.basename(file2_path)}")
        with open(file2_path, 'r', encoding='utf-8') as file2:
            content2 = file2.read()
        
        print("🔍 Đang trích xuất ContentUID...")
        # Trích xuất tất cả ContentUID từ hai file
        uids1 = set(re.findall(r'contentuid="([^"]*)"', content1))
        uids2 = set(re.findall(r'contentuid="([^"]*)"', content2))
        
        print(f"📊 File A có {len(uids1)} ContentUID")
        print(f"📊 File B có {len(uids2)} ContentUID")
        
        # So sánh và phân loại
        only_in_file1 = uids1 - uids2
        only_in_file2 = uids2 - uids1
        in_both_files = uids1 & uids2
        
        print(f"🔍 Phân tích hoàn tất:")
        print(f"   - Chỉ có trong File A: {len(only_in_file1)}")
        print(f"   - Chỉ có trong File B: {len(only_in_file2)}")
        print(f"   - Số Dòng Trùng Nhau: {len(in_both_files)}")
        
        return {
            'chi_co_trong_file1': only_in_file1,
            'chi_co_trong_file2': only_in_file2,
            'trung_nhau': in_both_files
        }
    except Exception as e:
        print(f"❌ Lỗi khi so sánh file: {str(e)}")
        return None

def xuat_contentuid_trung_ra_file(file_path, output_path):
    duplicates = tim_contentuid_trung_lap_trong_file(file_path)
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            for uid in duplicates:
                file.write(f"{uid}\n")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất ContentUID trùng: {str(e)}")
        return False

def xoa_contentuid_trung_trong_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        seen_uids = set()
        new_content = []
        
        for match in re.finditer(r'(<content.*?</content>)', content, re.DOTALL):
            element = match.group(1)
            uid_match = re.search(r'contentuid="([^"]*)"', element)
            
            if uid_match:
                uid = uid_match.group(1)
                if uid not in seen_uids:
                    seen_uids.add(uid)
                    new_content.append(element)
            else:
                new_content.append(element)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('<?xml version="1.0" encoding="utf-8"?>\n<contentList>\n')
            file.write('\n'.join(new_content))
            file.write('\n</contentList>')
            
        return True
    except Exception as e:
        print(f"Lỗi khi xóa ContentUID trùng: {str(e)}")
        return False

def lay_noi_dung_theo_contentuid_list(file_path, uid_list):
    """
    Lấy nội dung đầy đủ của các content theo danh sách ContentUID
    
    Args:
        file_path (str): Đường dẫn đến file XML
        uid_list (set): Danh sách ContentUID cần lấy
        
    Returns:
        list: Danh sách các content element đầy đủ
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Tìm tất cả content elements
        pattern = r'(\t<content[^>]*>.*?</content>)'
        content_elements = re.finditer(pattern, content, re.DOTALL)
        matches = []
        
        for element in content_elements:
            full_element = element.group(1)
            # Tìm contentuid trong element
            uid_match = re.search(r'contentuid="([^"]+)"', full_element)
            if uid_match and uid_match.group(1) in uid_list:
                matches.append(full_element)
                
        return matches
    except Exception as e:
        print(f"❌ Lỗi khi lấy nội dung theo ContentUID: {str(e)}")
        return []

def lay_noi_dung_theo_contentuid(file_path, uid):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            pattern = rf'<content.*?contentuid="{uid}".*?</content>'
            match = re.search(pattern, content, re.DOTALL)
            return match.group(0) if match else None
    except Exception as e:
        print(f"Lỗi khi lấy nội dung theo ContentUID: {str(e)}")
        return None

def xuat_contentuid_khong_trung_ra_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
            contentuid_list = re.findall(r'contentuid="([^"]*)"', content)
            unique_uids = set(contentuid_list)
            
        with open(output_path, 'w', encoding='utf-8') as file:
            for uid in unique_uids:
                file.write(f"{uid}\n")
        return True
    except Exception as e:
        print(f"Lỗi khi xuất ContentUID không trùng: {str(e)}")
        return False

class RedirectText:
    """
    Lớp chuyển hướng đầu ra để hiển thị trong UI
    """
    def __init__(self, text_widget):
        self.output = text_widget
        self.stdout = sys.stdout

    def write(self, string):
        self.output.configure(state="normal")
        self.output.insert(tk.END, string)
        self.output.see(tk.END)
        self.output.configure(state="disabled")
        self.stdout.write(string)

    def flush(self):
        pass

class SearchToolUI:
    """
    Giao diện người dùng cho công cụ tìm kiếm và xử lý file XML
    """
    def __init__(self, master):
        self.master = master
        master.title("Công cụ xử lý file XML")
        master.geometry("900x700")
        
        # Đường dẫn file lưu lịch sử
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "path_history.json")
        
        # Tải lịch sử đường dẫn
        self.path_history = self.load_path_history()
        
        # Tab Control
        self.tab_control = ttk.Notebook(master)
        
        # Tab 1: Tìm kiếm và xóa nội dung
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Tìm kiếm và xóa')
        
        # Tab 2: Phân tích file
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Phân tích file')
        
        # Tab 3: So sánh hai file
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab3, text='So sánh hai file')
        
        # Tab 4: Chia file XML
        self.tab4 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab4, text='Chia file XML')
        
        self.tab_control.pack(expand=1, fill="both")
        
        # Thiết lập các tab
        self.setup_search_tab()
        self.setup_analyze_tab()
        self.setup_compare_tab()
        self.setup_split_tab()
        
        # Thiết lập khu vực hiển thị kết quả
        self.setup_output_area()
        
        # Thêm một số đường dẫn test vào lịch sử nếu lịch sử trống (chỉ để test)
        if len(self.path_history) == 0:
            print("Lịch sử trống, thêm một số đường dẫn test...")
            # Thử tìm một vài file XML trong workspace để làm ví dụ
            test_paths = [
                r"d:\Games\Baldurt's Gate VH\baldurts-gate-3\data\A-VIET-HOA\english.xml",
                r"d:\Games\Baldurt's Gate VH\baldurts-gate-3\data\A-VIET-HOA\Item.xml",
            ]
            for path in test_paths:
                if os.path.exists(path):
                    self.path_history.append(path)
                    print(f"Thêm đường dẫn test: {path}")
            
            if self.path_history:
                self.save_path_history()
                self.update_combobox_values()
        
        # Chuyển hướng đầu ra để hiển thị trong UI
        self.redirect = RedirectText(self.output_text)
        sys.stdout = self.redirect

    def load_path_history(self):
        """Tải lịch sử đường dẫn từ file JSON"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Giới hạn số lượng lịch sử (tối đa 20 đường dẫn)
                    history = data[:20] if isinstance(data, list) else []
                    print(f"Đã tải {len(history)} đường dẫn từ lịch sử")
                    return history
            else:
                print("File lịch sử chưa tồn tại, tạo lịch sử mới")
                return []
        except Exception as e:
            print(f"Lỗi khi tải lịch sử: {e}")
            return []
    
    def save_path_history(self):
        """Lưu lịch sử đường dẫn vào file JSON"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.path_history, f, ensure_ascii=False, indent=2)
            print(f"Đã lưu {len(self.path_history)} đường dẫn vào lịch sử")
        except Exception as e:
            print(f"Lỗi khi lưu lịch sử: {e}")
    
    def add_to_history(self, path):
        """Thêm đường dẫn vào lịch sử"""
        if path and os.path.exists(path):
            # Xóa đường dẫn cũ nếu đã tồn tại
            if path in self.path_history:
                self.path_history.remove(path)
            # Thêm vào đầu danh sách
            self.path_history.insert(0, path)
            # Giới hạn số lượng lịch sử
            self.path_history = self.path_history[:20]
            # Lưu vào file
            self.save_path_history()
            # Cập nhật các combobox
            self.update_combobox_values()
            print(f"Đã thêm vào lịch sử: {os.path.basename(path)}")
        else:
            if path:
                print(f"Không thể thêm vào lịch sử - File không tồn tại: {path}")
    
    def remove_from_history(self, path):
        """Xóa đường dẫn khỏi lịch sử"""
        if path in self.path_history:
            self.path_history.remove(path)
            self.save_path_history()
            self.update_combobox_values()
            print(f"Đã xóa khỏi lịch sử: {os.path.basename(path)}")
            return True
        return False
    
    def update_combobox_values(self):
        """Cập nhật giá trị cho tất cả các combobox"""
        print(f"Cập nhật combobox với {len(self.path_history)} đường dẫn")
        # Cập nhật combobox trong tab tìm kiếm
        if hasattr(self, 'search_path_entry'):
            self.search_path_entry['values'] = self.path_history
            print("Đã cập nhật search_path_entry")
        
        # Cập nhật combobox trong tab phân tích
        if hasattr(self, 'analyze_path_entry'):
            self.analyze_path_entry['values'] = self.path_history
            print("Đã cập nhật analyze_path_entry")
        
        # Cập nhật combobox trong tab so sánh
        if hasattr(self, 'file_a_path_entry'):
            self.file_a_path_entry['values'] = self.path_history
            print("Đã cập nhật file_a_path_entry")
        if hasattr(self, 'file_b_path_entry'):
            self.file_b_path_entry['values'] = self.path_history
            print("Đã cập nhật file_b_path_entry")
        
        # Cập nhật combobox trong tab chia file
        if hasattr(self, 'split_path_entry'):
            self.split_path_entry['values'] = self.path_history
            print("Đã cập nhật split_path_entry")

    def setup_search_tab(self):
        """Thiết lập tab tìm kiếm và xóa nội dung"""
        frame = ttk.LabelFrame(self.tab1, text="Tìm kiếm nội dung")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Thông báo hướng dẫn
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill="x", padx=5, pady=5)
        
        info_text = "💡 Sử dụng nút 'Duyệt...' để chọn file XML hoặc 'Lấy từ clipboard' để lấy đường dẫn"
        
        ttk.Label(info_frame, text=info_text, font=("Arial", 9), foreground="blue").pack(side=tk.LEFT)
        
        # Thông báo về lịch sử đường dẫn
        history_info_frame = ttk.Frame(frame)
        history_info_frame.pack(fill="x", padx=5, pady=2)
        
        history_info_text = "📚 Lịch sử đường dẫn: Nhấn vào dropdown để chọn từ lịch sử | Nút 🗑️ để xóa đường dẫn hiện tại khỏi lịch sử"
        ttk.Label(history_info_frame, text=history_info_text, font=("Arial", 9), foreground="darkblue").pack(side=tk.LEFT)
        
        # Thông báo về khả năng tìm kiếm mới
        search_info_frame = ttk.Frame(frame)
        search_info_frame.pack(fill="x", padx=5, pady=2)
        
        search_info_text = "🔍 Tìm kiếm trong toàn bộ dòng XML: contentuid, version, content text... | Nhiều từ khóa: cách nhau bởi dấu phẩy (,)"
        ttk.Label(search_info_frame, text=search_info_text, font=("Arial", 9), foreground="darkgreen").pack(side=tk.LEFT)
        
        # Frame cho đường dẫn file
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(path_frame, text="Đường dẫn file XML:").pack(side=tk.LEFT)
        
        self.search_path_var = tk.StringVar()
        # Sử dụng Combobox thay vì Entry để có dropdown
        self.search_path_entry = ttk.Combobox(path_frame, textvariable=self.search_path_var, width=50)
        self.search_path_entry['values'] = self.path_history
        self.search_path_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Debug: In số lượng items trong combobox
        print(f"Khởi tạo search combobox với {len(self.path_history)} items")
        
        # Nút duyệt file
        ttk.Button(path_frame, text="Duyệt...", command=lambda: self.browse_file(self.search_path_var)).pack(side=tk.LEFT, padx=5)
        
        # Nút lấy đường dẫn từ clipboard
        ttk.Button(path_frame, text="Lấy từ clipboard", command=lambda: self.parse_clipboard(self.search_path_var)).pack(side=tk.LEFT)
        
        # Nút xóa đường dẫn hiện tại khỏi lịch sử
        ttk.Button(path_frame, text="🗑️", command=lambda: self.remove_current_path(self.search_path_var)).pack(side=tk.LEFT, padx=2)
        
        # Frame cho nội dung tìm kiếm
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(search_frame, text="Nội dung tìm kiếm:").pack(side=tk.LEFT)
        
        self.search_content_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_content_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Thêm placeholder cho ô tìm kiếm
        search_entry.insert(0, "Từ khóa 1, từ khóa 2, ... (cách nhau bởi dấu phẩy)")
        search_entry.configure(foreground="gray")
        search_entry.bind("<FocusIn>", lambda e: self.clear_search_placeholder(e))
        search_entry.bind("<FocusOut>", lambda e: self.add_search_placeholder(e))
        
        # Frame cho các nút chức năng
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="🔍 Tìm kiếm", command=self.run_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Lưu kết quả", command=self.save_search_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Xóa nội dung", command=self.delete_content).pack(side=tk.LEFT, padx=5)
        
        # Biến để lưu kết quả tìm kiếm
        self.search_results = []

    def setup_analyze_tab(self):
        """Thiết lập tab phân tích file"""
        frame = ttk.LabelFrame(self.tab2, text="Phân tích file XML")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame cho đường dẫn file
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(path_frame, text="Đường dẫn file XML:").pack(side=tk.LEFT)
        
        self.analyze_path_var = tk.StringVar()
        # Sử dụng Combobox thay vì Entry để có dropdown
        self.analyze_path_entry = ttk.Combobox(path_frame, textvariable=self.analyze_path_var, width=50)
        self.analyze_path_entry['values'] = self.path_history
        self.analyze_path_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Debug: In số lượng items trong combobox
        print(f"Khởi tạo analyze combobox với {len(self.path_history)} items")
        
        # Nút duyệt file
        ttk.Button(path_frame, text="Duyệt...", command=lambda: self.browse_file(self.analyze_path_var)).pack(side=tk.LEFT, padx=5)
        
        # Nút lấy đường dẫn từ clipboard
        ttk.Button(path_frame, text="Lấy từ clipboard", command=lambda: self.parse_clipboard(self.analyze_path_var)).pack(side=tk.LEFT)
        
        # Nút xóa đường dẫn hiện tại khỏi lịch sử
        ttk.Button(path_frame, text="🗑️", command=lambda: self.remove_current_path(self.analyze_path_var)).pack(side=tk.LEFT, padx=2)
        
        # Frame cho các nút chức năng
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Phân tích file", command=self.run_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tìm contentUID trùng lặp", command=self.find_duplicate_uids).pack(side=tk.LEFT, padx=5)

    def setup_compare_tab(self):
        """Thiết lập tab so sánh hai file"""
        frame = ttk.LabelFrame(self.tab3, text="So sánh hai file XML")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame cho file A
        file_a_frame = ttk.Frame(frame)
        file_a_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(file_a_frame, text="File A:").pack(side=tk.LEFT)
        
        self.file_a_path_var = tk.StringVar()
        # Sử dụng Combobox thay vì Entry để có dropdown
        self.file_a_path_entry = ttk.Combobox(file_a_frame, textvariable=self.file_a_path_var, width=50)
        self.file_a_path_entry['values'] = self.path_history
        self.file_a_path_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Debug: In số lượng items trong combobox
        print(f"Khởi tạo file_a combobox với {len(self.path_history)} items")
        
        # Nút duyệt file A
        ttk.Button(file_a_frame, text="Duyệt...", command=lambda: self.browse_file(self.file_a_path_var)).pack(side=tk.LEFT, padx=5)
        
        # Nút lấy đường dẫn từ clipboard cho file A
        ttk.Button(file_a_frame, text="Lấy từ clipboard", command=lambda: self.parse_clipboard(self.file_a_path_var)).pack(side=tk.LEFT)
        
        # Nút xóa đường dẫn hiện tại khỏi lịch sử
        ttk.Button(file_a_frame, text="🗑️", command=lambda: self.remove_current_path(self.file_a_path_var)).pack(side=tk.LEFT, padx=2)
        
        # Frame cho file B
        file_b_frame = ttk.Frame(frame)
        file_b_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(file_b_frame, text="File B:").pack(side=tk.LEFT)
        
        self.file_b_path_var = tk.StringVar()
        # Sử dụng Combobox thay vì Entry để có dropdown
        self.file_b_path_entry = ttk.Combobox(file_b_frame, textvariable=self.file_b_path_var, width=50)
        self.file_b_path_entry['values'] = self.path_history
        self.file_b_path_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Debug: In số lượng items trong combobox
        print(f"Khởi tạo file_b combobox với {len(self.path_history)} items")
        
        # Nút duyệt file B
        ttk.Button(file_b_frame, text="Duyệt...", command=lambda: self.browse_file(self.file_b_path_var)).pack(side=tk.LEFT, padx=5)
        
        # Nút lấy đường dẫn từ clipboard cho file B
        ttk.Button(file_b_frame, text="Lấy từ clipboard", command=lambda: self.parse_clipboard(self.file_b_path_var)).pack(side=tk.LEFT)
        
        # Nút xóa đường dẫn hiện tại khỏi lịch sử
        ttk.Button(file_b_frame, text="🗑️", command=lambda: self.remove_current_path(self.file_b_path_var)).pack(side=tk.LEFT, padx=2)
        
        # Frame cho các nút chức năng
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="So sánh hai file", command=self.run_comparison).pack(side=tk.LEFT, padx=5)
        
        # Frame cho các tùy chọn sau so sánh
        self.compare_options_frame = ttk.LabelFrame(frame, text="Tùy chọn sau so sánh")
        
        # Các biến lưu kết quả so sánh
        self.comparison_results = None
        self.contentuid_only_in_a = None
        self.contentuid_only_in_b = None

    def setup_compare_options(self):
        """Thiết lập các tùy chọn sau khi so sánh hai file"""
        # Xóa các widget cũ nếu có
        for widget in self.compare_options_frame.winfo_children():
            widget.destroy()
        
        # Hiển thị frame tùy chọn
        self.compare_options_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Các nút chức năng cho contentUID trùng nhau
        trung_frame = ttk.LabelFrame(self.compare_options_frame, text="Xử lý các contentUID trùng nhau")
        trung_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(trung_frame, text="Lọc contentUID trùng nhau ra file", 
                  command=self.export_duplicate_uids).pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(trung_frame, text="Xóa contentUID trùng nhau ở file A", 
                  command=lambda: self.delete_duplicate_uids('A')).pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(trung_frame, text="Xóa contentUID trùng nhau ở file B", 
                  command=lambda: self.delete_duplicate_uids('B')).pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(trung_frame, text="Xóa contentUID trùng nhau ở cả hai file", 
                  command=lambda: self.delete_duplicate_uids('AB')).pack(side=tk.LEFT, padx=5, pady=2)
        
        # Các nút chức năng cho contentUID không trùng nhau
        khong_trung_frame = ttk.LabelFrame(self.compare_options_frame, text="Xử lý các contentUID không trùng nhau")
        khong_trung_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(khong_trung_frame, text="Lọc contentUID chỉ có trong file A", 
                  command=lambda: self.export_unique_uids('A')).pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(khong_trung_frame, text="Lọc contentUID chỉ có trong file B", 
                  command=lambda: self.export_unique_uids('B')).pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(khong_trung_frame, text="Lọc tất cả contentUID không trùng nhau", 
                  command=lambda: self.export_unique_uids('AB')).pack(side=tk.LEFT, padx=5, pady=2)

    def setup_split_tab(self):
        """Thiết lập tab chia file XML"""
        frame = ttk.LabelFrame(self.tab4, text="Chia file XML thành nhiều file nhỏ")
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Thông báo hướng dẫn
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill="x", padx=5, pady=5)
        
        info_text = "💡 Chia file XML lớn thành nhiều file nhỏ để dễ quản lý và xử lý"
        ttk.Label(info_frame, text=info_text, font=("Arial", 9), foreground="blue").pack(side=tk.LEFT)
        
        # Frame cho đường dẫn file
        path_frame = ttk.Frame(frame)
        path_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(path_frame, text="Đường dẫn file XML:").pack(side=tk.LEFT)
        
        self.split_path_var = tk.StringVar()
        # Sử dụng Combobox để có dropdown lịch sử
        self.split_path_entry = ttk.Combobox(path_frame, textvariable=self.split_path_var, width=50)
        self.split_path_entry['values'] = self.path_history
        self.split_path_entry.pack(side=tk.LEFT, padx=5, fill="x", expand=True)
        
        # Nút duyệt file
        ttk.Button(path_frame, text="Duyệt...", command=lambda: self.browse_file(self.split_path_var)).pack(side=tk.LEFT, padx=5)
        
        # Nút lấy đường dẫn từ clipboard
        ttk.Button(path_frame, text="Lấy từ clipboard", command=lambda: self.parse_clipboard(self.split_path_var)).pack(side=tk.LEFT)
        
        # Nút xóa đường dẫn hiện tại khỏi lịch sử
        ttk.Button(path_frame, text="🗑️", command=lambda: self.remove_current_path(self.split_path_var)).pack(side=tk.LEFT, padx=2)
        
        # Frame cho cài đặt chia file
        settings_frame = ttk.Frame(frame)
        settings_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Label(settings_frame, text="Số content elements mỗi file:").pack(side=tk.LEFT)
        
        self.content_per_file_var = tk.StringVar(value="1000")
        content_entry = ttk.Entry(settings_frame, textvariable=self.content_per_file_var, width=10)
        content_entry.pack(side=tk.LEFT, padx=5)
        
        # Thêm các gợi ý số lượng
        suggestion_frame = ttk.Frame(frame)
        suggestion_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(suggestion_frame, text="Gợi ý:").pack(side=tk.LEFT)
        
        ttk.Button(suggestion_frame, text="500", 
                  command=lambda: self.content_per_file_var.set("500")).pack(side=tk.LEFT, padx=2)
        ttk.Button(suggestion_frame, text="1000", 
                  command=lambda: self.content_per_file_var.set("1000")).pack(side=tk.LEFT, padx=2)
        ttk.Button(suggestion_frame, text="2000", 
                  command=lambda: self.content_per_file_var.set("2000")).pack(side=tk.LEFT, padx=2)
        ttk.Button(suggestion_frame, text="5000", 
                  command=lambda: self.content_per_file_var.set("5000")).pack(side=tk.LEFT, padx=2)
        
        # Frame cho các nút chức năng
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=5, pady=10)
        
        ttk.Button(button_frame, text="📊 Phân tích file trước", command=self.analyze_before_split).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✂️ Chia file", command=self.run_split_file).pack(side=tk.LEFT, padx=5)
        
        # Frame cho thông tin phân tích
        self.split_info_frame = ttk.LabelFrame(frame, text="Thông tin phân tích")
        
        # Biến lưu thông tin phân tích
        self.split_analysis_result = None

    def setup_output_area(self):
        """Thiết lập khu vực hiển thị kết quả"""
        output_frame = ttk.LabelFrame(self.master, text="Kết quả")
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Thêm thanh cuộn
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=80, height=15)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.output_text.config(state="disabled")
        
        # Nút xóa kết quả
        ttk.Button(output_frame, text="Xóa kết quả", command=self.clear_output).pack(padx=5, pady=5)

    def parse_clipboard(self, string_var):
        """
        Phân tích nội dung clipboard để tìm đường dẫn file
        
        Args:
            string_var: StringVar để lưu đường dẫn tìm thấy
        """
        try:
            # Lấy nội dung clipboard
            clipboard_content = self.master.clipboard_get()
            
            # Tìm đường dẫn trong nội dung clipboard
            file_path = self.find_file_path_in_text(clipboard_content)
            
            if file_path:
                string_var.set(file_path)
                # Thêm vào lịch sử
                self.add_to_history(file_path)
                self.print_to_output(f"Đã tìm thấy đường dẫn: {file_path}")
            else:
                self.print_to_output("Không tìm thấy đường dẫn file trong clipboard.")
        except:
            self.print_to_output("Không thể đọc nội dung từ clipboard.")

    def find_file_path_in_text(self, text):
        """
        Tìm đường dẫn file trong văn bản
        
        Args:
            text (str): Văn bản cần tìm đường dẫn
            
        Returns:
            str: Đường dẫn file tìm thấy hoặc None
        """
        # Mẫu regex cho đường dẫn Windows
        win_pattern = r'([a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*\.xml)'
        
        # Mẫu regex cho đường dẫn Unix
        unix_pattern = r'(/(?:[^/\r\n]+/)*[^/\r\n]*\.xml)'
        
        # Tìm đường dẫn
        if os.name == 'nt':
            match = re.search(win_pattern, text, re.IGNORECASE)
        else:
            match = re.search(unix_pattern, text)
        
        if match:
            return match.group(1)
        return None

    def browse_file(self, string_var):
        """
        Mở hộp thoại duyệt file và lưu đường dẫn
        
        Args:
            string_var: StringVar để lưu đường dẫn file đã chọn
        """
        filepath = filedialog.askopenfilename(
            filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
        )
        if filepath:
            string_var.set(filepath)
            # Thêm vào lịch sử
            self.add_to_history(filepath)
    
    def parse_clipboard(self, string_var):
        """
        Phân tích nội dung clipboard để tìm đường dẫn file
        
        Args:
            string_var: StringVar để lưu đường dẫn tìm thấy
        """
        try:
            # Lấy nội dung clipboard
            clipboard_content = self.master.clipboard_get()
            print(f"Nội dung clipboard: {clipboard_content[:100]}...")  # Debug
            
            # Tìm đường dẫn trong nội dung clipboard
            file_path = self.find_file_path_in_text(clipboard_content)
            
            if file_path:
                print(f"Tìm thấy đường dẫn: {file_path}")  # Debug
                string_var.set(file_path)
                # Thêm vào lịch sử
                self.add_to_history(file_path)
                self.print_to_output(f"Đã tìm thấy đường dẫn: {file_path}")
            else:
                print("Không tìm thấy đường dẫn file trong clipboard")  # Debug
                self.print_to_output("Không tìm thấy đường dẫn file trong clipboard.")
        except Exception as e:
            print(f"Lỗi clipboard: {e}")  # Debug
            self.print_to_output("Không thể đọc nội dung từ clipboard.")
    
    def remove_current_path(self, string_var):
        """
        Xóa đường dẫn hiện tại khỏi lịch sử
        
        Args:
            string_var: StringVar chứa đường dẫn cần xóa
        """
        current_path = string_var.get()
        if current_path:
            if self.remove_from_history(current_path):
                self.print_to_output(f"Đã xóa đường dẫn khỏi lịch sử: {os.path.basename(current_path)}")
                # Xóa nội dung hiện tại trong combobox
                string_var.set("")
            else:
                self.print_to_output("Đường dẫn không có trong lịch sử.")
        else:
            messagebox.showinfo("Thông báo", "Không có đường dẫn nào để xóa.")

    def clear_search_placeholder(self, event):
        """Xóa placeholder text cho ô tìm kiếm"""
        if event.widget.get() == "Từ khóa 1, từ khóa 2, ... (cách nhau bởi dấu phẩy)":
            event.widget.delete(0, tk.END)
            event.widget.configure(foreground="black")

    def add_search_placeholder(self, event):
        """Thêm placeholder text cho ô tìm kiếm"""
        if not event.widget.get():
            event.widget.insert(0, "Từ khóa 1, từ khóa 2, ... (cách nhau bởi dấu phẩy)")
            event.widget.configure(foreground="gray")

    def clear_output(self):
        """Xóa nội dung khu vực hiển thị kết quả"""
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")

    def print_to_output(self, text):
        """
        Hiển thị văn bản trong khu vực kết quả
        
        Args:
            text (str): Văn bản cần hiển thị
        """
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state="disabled")

    def run_search(self):
        """Thực hiện tìm kiếm nội dung"""
        file_path = self.search_path_var.get()
        search_content = self.search_content_var.get()
        
        # Kiểm tra placeholder text
        if file_path in ["", ""]:
            messagebox.showerror("Lỗi", "Vui lòng chọn file XML để tìm kiếm")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"File {file_path} không tồn tại")
            return
            
        if search_content in ["", "Từ khóa 1, từ khóa 2, ... (cách nhau bởi dấu phẩy)"]:
            messagebox.showerror("Lỗi", "Vui lòng nhập nội dung cần tìm kiếm")
            return
        
        # Thực hiện tìm kiếm trong luồng riêng
        self.clear_output()
        threading.Thread(target=self._search_thread, args=(file_path, search_content)).start()

    def _search_thread(self, file_path, search_content):
        """
        Luồng tìm kiếm để không làm treo UI
        
        Args:
            file_path (str): Đường dẫn đến file XML
            search_content (str): Nội dung cần tìm kiếm
        """
        try:
            # Phân tách từ khóa để hiển thị
            search_keywords = [keyword for keyword in search_content.split(',')]
            
            # Thông báo bắt đầu tìm kiếm
            if len(search_keywords) == 1:
                self.print_to_output(f"🔍 Đang tìm kiếm '{search_content}' trong file:")
            else:
                self.print_to_output(f"🔍 Đang tìm kiếm {len(search_keywords)} từ khóa trong file:")
                for i, keyword in enumerate(search_keywords, 1):
                    self.print_to_output(f"   {i}. '{keyword}'")
            
            self.print_to_output(f"📁 {file_path}")
            
            # Kiểm tra kích thước file
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            self.print_to_output(f"📊 Kích thước file: {file_size:.2f} MB")
            
            # Thực hiện tìm kiếm
            self.search_results = tim_kiem_noi_dung(file_path, search_content)
            
            # Hiển thị kết quả
            if self.search_results:
                self.print_to_output(f"\n✅ Tìm kiếm hoàn tất! Đã tìm thấy {len(self.search_results)} kết quả.")
                self.print_to_output("📋 Chi tiết kết quả:")
                
                for i, result in enumerate(self.search_results, 1):
                    # Tìm contentuid
                    uid_match = re.search(r'contentuid="([^"]+)"', result)
                    if uid_match:
                        uid = uid_match.group(1)
                        # Lấy phần text bên trong
                        text_match = re.search(r'>([^<]+)</content>', result)
                        if text_match:
                            text = text_match.group(1)[:100]  # Chỉ lấy 100 ký tự đầu
                            if len(text_match.group(1)) > 100:
                                text += "..."
                            self.print_to_output(f"   {i}. UID: {uid}")
                            self.print_to_output(f"      Text: {text}")
                        else:
                            self.print_to_output(f"   {i}. UID: {uid}")
                    else:
                        self.print_to_output(f"   {i}. Không tìm thấy UID")
                
                self.print_to_output("\n💡 Bạn có thể nhấn '🗑️ Xóa nội dung' để xóa các kết quả này.")
            else:
                self.print_to_output("\n❌ Không tìm thấy kết quả nào phù hợp với từ khóa tìm kiếm.")
                self.print_to_output("💡 Thử lại với từ khóa khác hoặc kiểm tra đường dẫn file.")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi tìm kiếm: {str(e)}")
            self.print_to_output("💡 Kiểm tra lại đường dẫn file và quyền truy cập.")

    def save_search_results(self):
        """Lưu kết quả tìm kiếm ra file XML tự động"""
        if not self.search_results:
            messagebox.showinfo("Thông báo", "Không có kết quả tìm kiếm để lưu")
            return
            
        file_path = self.search_path_var.get()
        search_content = self.search_content_var.get()
        
        # Thực hiện lưu kết quả trong luồng riêng
        threading.Thread(target=self._save_results_thread, args=(file_path, search_content,)).start()

    def _save_results_thread(self, file_path, search_content):
        """
        Luồng lưu kết quả để không làm treo UI
        
        Args:
            file_path (str): Đường dẫn file gốc
            search_content (str): Nội dung đã tìm kiếm
        """
        try:
            self.print_to_output("💾 Đang lưu kết quả tìm kiếm...")
            
            # Xuất kết quả ra file tự động
            output_path = xuat_ket_qua_ra_xml(self.search_results, file_path, search_content)
            
            if output_path:
                self.print_to_output("✅ Lưu thành công!")
                self.print_to_output(f"📁 File đã được lưu tại: {os.path.basename(output_path)}")
            else:
                self.print_to_output("❌ Lưu không thành công!")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi lưu kết quả: {str(e)}")

    def delete_content(self):
        """Xóa nội dung đã tìm thấy"""
        if not self.search_results:
            messagebox.showinfo("Thông báo", "Không có kết quả tìm kiếm để xóa")
            return
            
        file_path = self.search_path_var.get()
        
        # Hỏi xác nhận trước khi xóa
        confirm = messagebox.askyesno(
            "Xác nhận", 
            f"Bạn có chắc chắn muốn xóa {len(self.search_results)} phần tử từ file {os.path.basename(file_path)}?"
        )
        
        if not confirm:
            return
        
        # Thực hiện xóa trong luồng riêng
        threading.Thread(target=self._delete_thread, args=(file_path,)).start()

    def _delete_thread(self, file_path):
        """
        Luồng xóa nội dung để không làm treo UI
        
        Args:
            file_path (str): Đường dẫn đến file XML
        """
        try:
            self.print_to_output("🗑️ Đang xóa nội dung...")
            
            # Thực hiện xóa
            if xoa_noi_dung(file_path, self.search_results):
                self.print_to_output("✅ Xóa thành công!")
                self.print_to_output("💡 File đã được cập nhật.")
                # Xóa kết quả tìm kiếm sau khi xóa thành công
                self.search_results = []
            else:
                self.print_to_output("❌ Xóa không thành công!")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi xóa nội dung: {str(e)}")

    def run_analysis(self):
        """Phân tích file XML"""
        file_path = self.analyze_path_var.get()
        
        if not file_path:
            messagebox.showerror("Lỗi", "Vui lòng nhập đường dẫn file XML")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"File {file_path} không tồn tại")
            return
        
        # Thực hiện phân tích trong luồng riêng
        self.clear_output()
        threading.Thread(target=self._analyze_thread, args=(file_path,)).start()

    def _analyze_thread(self, file_path):
        """
        Luồng phân tích file để không làm treo UI
        
        Args:
            file_path (str): Đường dẫn đến file XML
        """
        # Lưu đầu ra hiện tại
        old_stdout = sys.stdout
        result_output = StringIO()
        sys.stdout = result_output
        
        try:
            phan_tich_file_xml(file_path)
        except Exception as e:
            # Khôi phục đầu ra và thông báo lỗi
            sys.stdout = old_stdout
            self.print_to_output(f"Lỗi khi phân tích file: {e}")
            return
        
        # Khôi phục đầu ra và hiển thị kết quả
        sys.stdout = old_stdout
        self.print_to_output(result_output.getvalue())

    def find_duplicate_uids(self):
        """Tìm các contentUID trùng lặp trong file"""
        file_path = self.analyze_path_var.get()
        
        if not file_path:
            messagebox.showerror("Lỗi", "Vui lòng nhập đường dẫn file XML")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"File {file_path} không tồn tại")
            return
        
        # Thực hiện tìm kiếm trong luồng riêng
        self.clear_output()
        threading.Thread(target=self._find_duplicate_thread, args=(file_path,)).start()

    def _find_duplicate_thread(self, file_path):
        """
        Luồng tìm contentUID trùng lặp để không làm treo UI
        
        Args:
            file_path (str): Đường dẫn đến file XML
        """
        # Lưu đầu ra hiện tại
        old_stdout = sys.stdout
        result_output = StringIO()
        sys.stdout = result_output
        
        try:
            tim_contentuid_trung_lap_trong_file(file_path)
        except Exception as e:
            # Khôi phục đầu ra và thông báo lỗi
            sys.stdout = old_stdout
            self.print_to_output(f"Lỗi khi tìm contentUID trùng lặp: {e}")
            return
        
        # Khôi phục đầu ra và hiển thị kết quả
        sys.stdout = old_stdout
        self.print_to_output(result_output.getvalue())

    def run_comparison(self):
        """So sánh hai file XML"""
        file_a = self.file_a_path_var.get()
        file_b = self.file_b_path_var.get()
        
        # Kiểm tra placeholder text
        if file_a in ["", ""]:
            messagebox.showerror("Lỗi", "Vui lòng chọn file A để so sánh")
            return
            
        if not os.path.exists(file_a):
            messagebox.showerror("Lỗi", f"File A không tồn tại:\n{file_a}")
            return
            
        if file_b in ["", ""]:
            messagebox.showerror("Lỗi", "Vui lòng chọn file B để so sánh")
            return
            
        if not os.path.exists(file_b):
            messagebox.showerror("Lỗi", f"File B không tồn tại:\n{file_b}")
            return
        
        # Thực hiện so sánh trong luồng riêng
        self.clear_output()
        threading.Thread(target=self._compare_thread, args=(file_a, file_b)).start()

    def _compare_thread(self, file_a, file_b):
        """
        Luồng so sánh hai file để không làm treo UI
        
        Args:
            file_a (str): Đường dẫn đến file A
            file_b (str): Đường dẫn đến file B
        """
        try:
            self.print_to_output(f"🔍 Đang so sánh hai file:")
            self.print_to_output(f"📁 File A: {os.path.basename(file_a)}")
            self.print_to_output(f"📁 File B: {os.path.basename(file_b)}")
            
            # Thực hiện so sánh
            comparison_result = so_sanh_hai_file_xml(file_a, file_b)
            
            if comparison_result:
                self.comparison_results = comparison_result
                
                # Lấy kết quả so sánh
                only_in_a = comparison_result['chi_co_trong_file1']
                only_in_b = comparison_result['chi_co_trong_file2'] 
                in_both = comparison_result['trung_nhau']
                
                # Hiển thị kết quả
                self.print_to_output(f"\n✅ So sánh hoàn tất!")
                self.print_to_output(f"📊 Thống kê:")
                self.print_to_output(f"   🔵 Chỉ có trong File A: {len(only_in_a)} ContentUID")
                self.print_to_output(f"   🔴 Chỉ có trong File B: {len(only_in_b)} ContentUID")
                self.print_to_output(f"   🟢 Có trong cả hai file: {len(in_both)} ContentUID")
                
                # Hiển thị mẫu ContentUID (5 đầu tiên)
                if only_in_a:
                    self.print_to_output(f"\n🔵 Mẫu ContentUID chỉ có trong File A:")
                    for uid in list(only_in_a)[:5]:
                        self.print_to_output(f"   - {uid}")
                    if len(only_in_a) > 5:
                        self.print_to_output(f"   ... và {len(only_in_a) - 5} ContentUID khác")
                
                if only_in_b:
                    self.print_to_output(f"\n🔴 Mẫu ContentUID chỉ có trong File B:")
                    for uid in list(only_in_b)[:5]:
                        self.print_to_output(f"   - {uid}")
                    if len(only_in_b) > 5:
                        self.print_to_output(f"   ... và {len(only_in_b) - 5} ContentUID khác")
                
                # Thiết lập các tùy chọn sau so sánh
                self.master.after(0, self.setup_compare_options)
                self.print_to_output(f"\n💡 Sử dụng các nút bên dưới để xuất kết quả.")
            else:
                self.print_to_output("❌ Không thể so sánh hai file.")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi so sánh hai file: {str(e)}")
            self.print_to_output("💡 Kiểm tra lại đường dẫn file và định dạng XML.")

    def export_duplicate_uids(self):
        """Xuất danh sách contentUID trùng nhau ra file"""
        if not self.comparison_results:
            messagebox.showinfo("Thông báo", "Không có contentUID trùng nhau để xuất")
            return
        
        # Thực hiện xuất file trong luồng riêng
        threading.Thread(target=self._export_duplicate_thread).start()

    def _export_duplicate_thread(self):
        """Luồng xuất contentUID trùng nhau để không làm treo UI"""
        try:
            file_a = self.file_a_path_var.get()
            file_b = self.file_b_path_var.get()
            
            # Tạo thư mục output trong thư mục gốc của project
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(script_dir))  # Lên 2 cấp từ src/Search Tool
            output_dir = os.path.join(project_root, "output")
            
            # Tạo thư mục output nếu chưa tồn tại
            os.makedirs(output_dir, exist_ok=True)
            
            # Tạo timestamp để tránh trùng tên file
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Tạo tên file output cho contentUID trùng nhau
            base_name_a = os.path.splitext(os.path.basename(file_a))[0]
            base_name_b = os.path.splitext(os.path.basename(file_b))[0]
            output_filename = f"duplicate_uids_{base_name_a}_vs_{base_name_b}_{timestamp}.xml"
            output_path = os.path.join(output_dir, output_filename)
            
            # Lấy danh sách contentUID trùng nhau
            duplicate_uids = self.comparison_results['trung_nhau']
            
            self.print_to_output(f"💾 Đang xuất {len(duplicate_uids)} ContentUID trùng nhau...")
            
            # Lấy nội dung đầy đủ từ file A (có thể dùng file A hoặc B đều được vì trùng nhau)
            content_elements = lay_noi_dung_theo_contentuid_list(file_a, duplicate_uids)
            
            if content_elements:
                # Xuất file XML với nội dung đầy đủ
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
                    file.write('<contentList>\n')
                    
                    for element in content_elements:
                        file.write(f'{element.rstrip()}\n')
                        
                    file.write('</contentList>')
                
                self.print_to_output(f"✅ Xuất thành công!")
                self.print_to_output(f"📁 File: {output_filename}")
                self.print_to_output(f"📊 Đã xuất {len(content_elements)} content elements trùng nhau")
            else:
                self.print_to_output(f"❌ Không tìm thấy nội dung cho {len(duplicate_uids)} ContentUID trùng nhau")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi xuất contentUID trùng nhau: {str(e)}")

    def delete_duplicate_uids(self, file_option):
        """
        Xóa contentUID trùng nhau
        
        Args:
            file_option (str): 'A' để xóa từ file A, 'B' để xóa từ file B, 
                            'AB' để xóa từ cả hai file
        """
        if not self.comparison_results:
            messagebox.showinfo("Thông báo", "Không có contentUID trùng nhau để xóa")
            return
        
        file_a = self.file_a_path_var.get()
        file_b = self.file_b_path_var.get()
        
        # Lấy danh sách contentUID trùng nhau
        uid_list = list(self.comparison_results['trung_nhau'])
        
        # Hỏi xác nhận trước khi xóa
        confirm = messagebox.askyesno(
            "Xác nhận", 
            f"Bạn có chắc chắn muốn xóa {len(uid_list)} contentUID trùng nhau từ " +
            ("file A" if file_option == 'A' else ("file B" if file_option == 'B' else "cả hai file")) + "?"
        )
        
        if not confirm:
            return
        
        # Thực hiện xóa trong luồng riêng
        threading.Thread(target=self._delete_duplicate_thread, args=(file_option, file_a, file_b, uid_list)).start()

    def _delete_duplicate_thread(self, file_option, file_a, file_b, uid_list):
        """
        Luồng xóa contentUID trùng nhau để không làm treo UI
        
        Args:
            file_option (str): 'A' để xóa từ file A, 'B' để xóa từ file B, 
                            'AB' để xóa từ cả hai file
            file_a (str): Đường dẫn đến file A
            file_b (str): Đường dẫn đến file B
            uid_list (list): Danh sách các contentUID cần xóa
        """
        try:
            self.print_to_output(f"🗑️ Đang xóa {len(uid_list)} ContentUID trùng nhau...")
            
            if file_option in ['A', 'AB']:
                self.print_to_output(f"📁 Xóa từ File A: {os.path.basename(file_a)}")
                # Lấy nội dung các content cần xóa từ file A
                content_to_remove = lay_noi_dung_theo_contentuid_list(file_a, uid_list)
                if content_to_remove:
                    if xoa_noi_dung(file_a, content_to_remove):
                        self.print_to_output(f"✅ Đã xóa thành công từ File A")
                    else:
                        self.print_to_output(f"❌ Lỗi khi xóa từ File A")
                
            if file_option in ['B', 'AB']:
                self.print_to_output(f"📁 Xóa từ File B: {os.path.basename(file_b)}")
                # Lấy nội dung các content cần xóa từ file B
                content_to_remove = lay_noi_dung_theo_contentuid_list(file_b, uid_list)
                if content_to_remove:
                    if xoa_noi_dung(file_b, content_to_remove):
                        self.print_to_output(f"✅ Đã xóa thành công từ File B")
                    else:
                        self.print_to_output(f"❌ Lỗi khi xóa từ File B")
                        
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi xóa contentUID trùng nhau: {str(e)}")

    def export_unique_uids(self, export_type):
        """
        Xuất contentUID không trùng nhau ra file
        
        Args:
            export_type (str): 'A' cho file A, 'B' cho file B, 'AB' cho tất cả
        """
        if not self.comparison_results:
            messagebox.showinfo("Thông báo", "Chưa có kết quả so sánh để xuất")
            return
        
        # Thực hiện xuất file trong luồng riêng
        threading.Thread(target=self._export_unique_thread, args=(export_type,)).start()

    def _export_unique_thread(self, export_type):
        """Luồng xuất contentUID không trùng nhau để không làm treo UI"""
        try:
            file_a = self.file_a_path_var.get()
            file_b = self.file_b_path_var.get()
            
            # Tạo timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if export_type == 'A':
                uids_to_export = self.comparison_results['chi_co_trong_file1']
                source_file = file_a
                base_name = os.path.splitext(os.path.basename(file_a))[0]
                output_filename = f"{base_name}_only_in_A_{timestamp}.xml"
                description = "chỉ có trong File A"
            elif export_type == 'B':
                uids_to_export = self.comparison_results['chi_co_trong_file2']
                source_file = file_b
                base_name = os.path.splitext(os.path.basename(file_b))[0]
                output_filename = f"{base_name}_only_in_B_{timestamp}.xml"
                description = "chỉ có trong File B"
            else:  # AB
                # Xuất cả hai file riêng biệt
                self._export_combined_unique_files(file_a, file_b, timestamp)
                return
            
            # Tạo thư mục output trong thư mục gốc của project
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(script_dir))  # Lên 2 cấp từ src/Search Tool
            output_dir = os.path.join(project_root, "output")
            
            # Tạo thư mục output nếu chưa tồn tại
            os.makedirs(output_dir, exist_ok=True)
            
            # Tạo đường dẫn output trong thư mục output
            output_path = os.path.join(output_dir, output_filename)
            
            self.print_to_output(f"💾 Đang xuất {len(uids_to_export)} ContentUID {description}...")
            
            # Lấy nội dung đầy đủ từ file gốc
            content_elements = lay_noi_dung_theo_contentuid_list(source_file, uids_to_export)
            
            if content_elements:
                # Xuất file XML với nội dung đầy đủ
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
                    file.write('<contentList>\n')
                    
                    for element in content_elements:
                        file.write(f'{element.rstrip()}\n')
                        
                    file.write('</contentList>')
                
                self.print_to_output(f"✅ Xuất thành công!")
                self.print_to_output(f"📁 File: {output_filename}")
                self.print_to_output(f"📊 Đã xuất {len(content_elements)} content elements đầy đủ")
            else:
                self.print_to_output(f"❌ Không tìm thấy nội dung cho {len(uids_to_export)} ContentUID")
            
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi xuất ContentUID: {str(e)}")
            
    def _export_combined_unique_files(self, file_a, file_b, timestamp):
        """Xuất cả hai file unique riêng biệt khi chọn 'AB'"""
        try:
            # Tạo thư mục output trong thư mục gốc của project
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(script_dir))  # Lên 2 cấp từ src/Search Tool
            output_dir = os.path.join(project_root, "output")
            
            # Tạo thư mục output nếu chưa tồn tại
            os.makedirs(output_dir, exist_ok=True)
            
            # Xuất file A
            uids_a = self.comparison_results['chi_co_trong_file1']
            if uids_a:
                base_name_a = os.path.splitext(os.path.basename(file_a))[0]
                output_filename_a = f"{base_name_a}_only_in_A_{timestamp}.xml"
                output_path_a = os.path.join(output_dir, output_filename_a)
                
                content_elements_a = lay_noi_dung_theo_contentuid_list(file_a, uids_a)
                
                with open(output_path_a, 'w', encoding='utf-8') as file:
                    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
                    file.write('<contentList>\n')
                    for element in content_elements_a:
                        file.write(f'{element.rstrip()}\n')
                    file.write('</contentList>')
                
                self.print_to_output(f"✅ Đã xuất File A: {output_filename_a} ({len(content_elements_a)} elements)")
            
            # Xuất file B
            uids_b = self.comparison_results['chi_co_trong_file2']
            if uids_b:
                base_name_b = os.path.splitext(os.path.basename(file_b))[0]
                output_filename_b = f"{base_name_b}_only_in_B_{timestamp}.xml"
                output_path_b = os.path.join(output_dir, output_filename_b)
                
                content_elements_b = lay_noi_dung_theo_contentuid_list(file_b, uids_b)
                
                with open(output_path_b, 'w', encoding='utf-8') as file:
                    file.write('<?xml version="1.0" encoding="utf-8"?>\n')
                    file.write('<contentList>\n')
                    for element in content_elements_b:
                        file.write(f'{element.rstrip()}\n')
                    file.write('</contentList>')
                
                self.print_to_output(f"✅ Đã xuất File B: {output_filename_b} ({len(content_elements_b)} elements)")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi xuất file combined: {str(e)}")

    def analyze_before_split(self):
        """Phân tích file trước khi chia"""
        file_path = self.split_path_var.get()
        
        if not file_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn file XML để phân tích")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"File {file_path} không tồn tại")
            return
        
        # Thực hiện phân tích trong luồng riêng
        self.clear_output()
        threading.Thread(target=self._analyze_split_thread, args=(file_path,)).start()

    def _analyze_split_thread(self, file_path):
        """
        Luồng phân tích file cho tab chia file
        
        Args:
            file_path (str): Đường dẫn đến file XML
        """
        try:
            self.print_to_output(f"🔍 Đang phân tích file: {os.path.basename(file_path)}")
            
            # Thực hiện phân tích
            analysis_result = phan_tich_file_xml(file_path)
            
            if analysis_result:
                self.split_analysis_result = analysis_result
                content_count = analysis_result['content_lines']
                
                # Hiển thị thông tin chia file
                self.print_to_output(f"\n📋 Dự đoán chia file:")
                
                try:
                    content_per_file = int(self.content_per_file_var.get())
                    if content_per_file <= 0:
                        raise ValueError("Số lượng phải > 0")
                    
                    total_files = (content_count + content_per_file - 1) // content_per_file
                    
                    self.print_to_output(f"   • Với {content_per_file:,} content/file → Sẽ tạo {total_files} file")
                    
                    # Hiển thị bảng dự đoán cho các kích thước khác nhau
                    suggestions = [500, 1000, 2000, 5000, 10000]
                    self.print_to_output(f"\n📊 Bảng dự đoán:")
                    for suggestion in suggestions:
                        if suggestion <= content_count:
                            files_needed = (content_count + suggestion - 1) // suggestion
                            self.print_to_output(f"   • {suggestion:5,} content/file → {files_needed:3d} file{'s' if files_needed > 1 else ''}")
                    
                    # Hiển thị frame thông tin
                    self.master.after(0, self.show_split_info)
                    
                except ValueError:
                    self.print_to_output("❌ Vui lòng nhập số nguyên dương cho số content mỗi file")
            else:
                self.print_to_output("❌ Không thể phân tích file")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi phân tích: {str(e)}")

    def show_split_info(self):
        """Hiển thị thông tin phân tích trong frame"""
        if not self.split_analysis_result:
            return
        
        # Hiển thị frame thông tin
        self.split_info_frame.pack(fill="x", padx=5, pady=5)
        
        # Xóa các widget cũ
        for widget in self.split_info_frame.winfo_children():
            widget.destroy()
        
        result = self.split_analysis_result
        
        # Hiển thị thông tin tóm tắt
        info_text = f"Tổng content: {result['content_lines']:,} | Kích thước: {result['file_size']/1024:.1f} KB | Dòng: {result['total_lines']:,}"
        ttk.Label(self.split_info_frame, text=info_text, font=("Arial", 9)).pack(pady=2)

    def run_split_file(self):
        """Chạy tính năng chia file"""
        file_path = self.split_path_var.get()
        
        if not file_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn file XML để chia")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("Lỗi", f"File {file_path} không tồn tại")
            return
        
        try:
            content_per_file = int(self.content_per_file_var.get())
            if content_per_file <= 0:
                raise ValueError("Số lượng phải lớn hơn 0")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên dương cho số content mỗi file")
            return
        
        # Hỏi xác nhận
        confirm = messagebox.askyesno(
            "Xác nhận chia file", 
            f"Bạn có chắc chắn muốn chia file thành các file nhỏ với {content_per_file:,} content elements mỗi file?\n\n"
            f"File: {os.path.basename(file_path)}"
        )
        
        if not confirm:
            return
        
        # Thực hiện chia file trong luồng riêng
        self.clear_output()
        threading.Thread(target=self._split_file_thread, args=(file_path, content_per_file)).start()

    def _split_file_thread(self, file_path, content_per_file):
        """
        Luồng chia file để không làm treo UI
        
        Args:
            file_path (str): Đường dẫn đến file XML
            content_per_file (int): Số content elements mỗi file
        """
        try:
            self.print_to_output(f"✂️ Bắt đầu chia file: {os.path.basename(file_path)}")
            self.print_to_output(f"📋 Cài đặt: {content_per_file:,} content elements mỗi file")
            
            # Thực hiện chia file
            created_files = chia_file_xml(file_path, content_per_file)
            
            if created_files:
                self.print_to_output(f"\n🎉 Chia file hoàn tất!")
                self.print_to_output(f"📁 Đã tạo {len(created_files)} file trong thư mục output")
                
                # Hiển thị danh sách file đã tạo
                self.print_to_output(f"\n📋 Danh sách file đã tạo:")
                for i, file_path in enumerate(created_files, 1):
                    file_name = os.path.basename(file_path)
                    self.print_to_output(f"   {i:2d}. {file_name}")
                
                # Thêm đường dẫn vào lịch sử
                self.add_to_history(self.split_path_var.get())
                
                self.print_to_output(f"\n💡 Các file đã được lưu trong thư mục 'output' của project.")
            else:
                self.print_to_output("❌ Chia file không thành công")
                
        except Exception as e:
            self.print_to_output(f"❌ Lỗi khi chia file: {str(e)}")

def main():
    # Tạo thư mục output trong thư mục gốc của project nếu chưa tồn tại
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))  # Lên 2 cấp từ src/Search Tool
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    # Tạo cửa sổ chính
    root = tk.Tk()
    app = SearchToolUI(root)
    
    # Thiết lập style
    style = ttk.Style()
    if os.name == 'nt':  # Windows
        style.theme_use('vista')
    
    # Thiết lập tiêu đề cửa sổ và kích thước mặc định
    root.title("Công cụ xử lý XML - Baldur's Gate 3 Việt Hóa")
    root.geometry("1000x700")
    
    # Hiển thị thông báo hướng dẫn
    app.print_to_output("🎉 Chào mừng đến với Công cụ xử lý XML!")
    app.print_to_output("✨ CẬP NHẬT: Đã sửa tính năng phân tích file và thêm tính năng chia file XML!")
    app.print_to_output("📂 Sử dụng các tab để truy cập các chức năng:")
    app.print_to_output("   • Tab 1: Tìm kiếm và xóa nội dung")
    app.print_to_output("   • Tab 2: Phân tích file (đã cải thiện)")
    app.print_to_output("   • Tab 3: So sánh hai file")
    app.print_to_output("   • Tab 4: Chia file XML (MỚI)")
    app.print_to_output("📚 Lịch sử đường dẫn: Nhấn dropdown để chọn từ lịch sử | Nút 🗑️ để xóa")
    app.print_to_output("� Tip: Sử dụng 'Lấy từ clipboard' để dán đường dẫn nhanh!")
    
    root.mainloop()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tim_Loc_Xoa.py - Tool tìm kiếm, phân tích, so sánh và xóa nội dung trong file XML
"""

import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from datetime import datetime
import re

def tim_kiem_noi_dung(duong_dan_file, noi_dung_tim_kiem):
    """
    Tìm kiếm nội dung trong file XML
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML cần tìm kiếm
        noi_dung_tim_kiem (str): Nội dung cần tìm kiếm
        
    Returns:
        list: Danh sách các phần tử (contentuid, nội dung, dòng XML) tìm thấy
    """
    if not os.path.exists(duong_dan_file):
        print(f"Lỗi: File {duong_dan_file} không tồn tại")
        return []
    
    try:
        # Đọc file XML
        with open(duong_dan_file, 'r', encoding='utf-8') as file:
            xml_content = file.read()
        
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        
        # Tìm kiếm các phần tử content chứa nội dung cần tìm
        ket_qua = []
        so_luong = 0
        
        for content in root.findall('.//content'):
            noi_dung = content.text
            if noi_dung and noi_dung_tim_kiem.lower() in noi_dung.lower():
                content_uid = content.get('contentuid', 'không có uid')
                
                # Tạo dòng XML đầy đủ cho nội dung này
                xml_line = get_xml_line_for_element(xml_content, content_uid, noi_dung)
                
                ket_qua.append((content_uid, noi_dung, xml_line))
                so_luong += 1
                print(f"\n[{so_luong}] UID: {content_uid}")
                print(f"Nội dung: {noi_dung}")
                print(f"Dòng XML: {xml_line}")
        
        print(f"\nTìm thấy {so_luong} kết quả cho nội dung: '{noi_dung_tim_kiem}'")
        return ket_qua
        
    except Exception as e:
        print(f"Lỗi khi tìm kiếm: {e}")
        return []

def get_xml_line_for_element(xml_content, content_uid, noi_dung):
    """
    Tìm dòng XML đầy đủ dựa trên content_uid và nội dung
    
    Args:
        xml_content (str): Nội dung XML đầy đủ
        content_uid (str): ID của phần tử content
        noi_dung (str): Nội dung của phần tử
        
    Returns:
        str: Dòng XML đầy đủ chứa phần tử content
    """
    pattern = re.compile(rf'<content\s+contentuid="{re.escape(content_uid)}"[^>]*>.*?</content>', re.DOTALL)
    matches = pattern.findall(xml_content)
    if matches:
        return matches[0]
    
    # Nếu không tìm thấy theo content_uid, thử tìm theo nội dung
    escaped_content = re.escape(noi_dung)
    pattern = re.compile(rf'<content\s+contentuid="[^"]*"[^>]*>{escaped_content}</content>', re.DOTALL)
    matches = pattern.findall(xml_content)
    if matches:
        return matches[0]
    
    return f'<content contentuid="{content_uid}">{noi_dung}</content>'

def xuat_ket_qua_ra_xml(ket_qua, noi_dung_tim_kiem):
    """
    Xuất kết quả tìm kiếm ra file XML
    
    Args:
        ket_qua (list): Danh sách kết quả tìm thấy
        noi_dung_tim_kiem (str): Nội dung đã tìm kiếm
        
    Returns:
        str: Đường dẫn file kết quả
    """
    try:
        # Tạo thư mục output/filtered nếu chưa tồn tại
        output_dir = os.path.join("output", "filtered")
        os.makedirs(output_dir, exist_ok=True)
        
        # Tạo tên file với thời gian hiện tại
        thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
        ten_file = os.path.join(output_dir, f"Content_By_{thoi_gian}.xml")
        
        root = ET.Element("contentList")
        
        # Thêm phần tử chú thích
        comment = ET.SubElement(root, "comment")
        comment.text = f"Kết quả tìm kiếm cho nội dung: '{noi_dung_tim_kiem}' - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Thêm các kết quả tìm được
        for uid, noi_dung, xml_line in ket_qua:
            # Phân tích dòng XML để lấy các thuộc tính
            content_element = None
            try:
                # Tạo một XML tạm thời để phân tích
                temp_xml = f"<root>{xml_line}</root>"
                temp_root = ET.fromstring(temp_xml)
                original_element = temp_root.find(".//content")
                
                if original_element is not None:
                    # Tạo phần tử content mới với các thuộc tính của phần tử gốc
                    content_element = ET.SubElement(root, "content")
                    for key, value in original_element.attrib.items():
                        content_element.set(key, value)
                    content_element.text = original_element.text
            except:
                # Nếu không thể phân tích XML, tạo phần tử đơn giản
                content_element = ET.SubElement(root, "content")
                content_element.set("contentuid", uid)
                content_element.text = noi_dung
        
        # Ghi ra file với định dạng đẹp
        formatted_xml = format_xml(root)
        with open(ten_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(formatted_xml)
        
        print(f"Đã xuất kết quả ra file XML: {ten_file}")
        return ten_file
        
    except Exception as e:
        print(f"Lỗi khi xuất file XML: {e}")
        return None

def xoa_noi_dung(duong_dan_file, ket_qua):
    """
    Xóa nội dung đã tìm thấy từ file bằng cách xóa dòng, giữ nguyên format gốc
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML cần xóa nội dung
        ket_qua (list): Danh sách các phần tử cần xóa (contentuid, nội dung, dòng XML)
        
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
    """
    try:
        # Đọc toàn bộ nội dung file
        with open(duong_dan_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Tạo file backup trước khi sửa đổi
        backup_dir = os.path.dirname(duong_dan_file)
        backup_file = os.path.join(backup_dir, f"backup_{os.path.basename(duong_dan_file)}")
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            
        print(f"Đã tạo file backup: {backup_file}")
        
        # Tạo danh sách contentuid cần xóa
        uid_can_xoa = [item[0] for item in ket_qua]
        
        # Tìm và đánh dấu các dòng cần xóa
        dong_can_xoa = set()
        so_luong_xoa = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Tìm dòng bắt đầu thẻ content
            if '<content contentuid=' in line:
                # Tìm contentuid trong dòng này
                for uid in uid_can_xoa:
                    if f'contentuid="{uid}"' in line:
                        # Đánh dấu dòng bắt đầu để xóa
                        start_line = i
                        
                        # Nếu thẻ đóng trên cùng dòng
                        if '</content>' in line:
                            dong_can_xoa.add(i)
                            so_luong_xoa += 1
                        else:
                            # Tìm dòng kết thúc thẻ content
                            j = i + 1
                            while j < len(lines):
                                if '</content>' in lines[j]:
                                    # Đánh dấu tất cả dòng từ start_line đến j
                                    for k in range(start_line, j + 1):
                                        dong_can_xoa.add(k)
                                    so_luong_xoa += 1
                                    break
                                j += 1
                        break
            i += 1
        
        # Tạo nội dung mới bằng cách loại bỏ các dòng đã đánh dấu
        new_lines = []
        for i, line in enumerate(lines):
            if i not in dong_can_xoa:
                new_lines.append(line)
        
        # Ghi lại file gốc với nội dung đã xóa, giữ nguyên format
        with open(duong_dan_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"Đã xóa {so_luong_xoa} phần tử từ file: {duong_dan_file}")
        
        # Kiểm tra nếu số lượng xóa khác với số lượng yêu cầu
        if so_luong_xoa != len(uid_can_xoa):
            print(f"Cảnh báo: Chỉ tìm thấy và xóa {so_luong_xoa}/{len(uid_can_xoa)} phần tử")
        
        return True
        
    except Exception as e:
        print(f"Lỗi khi xóa nội dung: {e}")
        return False

def phan_tich_file_xml(duong_dan_file):
    """
    Phân tích thông tin từ file XML
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML cần phân tích
        
    Returns:
        dict: Thông tin phân tích về file
    """
    if not os.path.exists(duong_dan_file):
        print(f"Lỗi: File {duong_dan_file} không tồn tại")
        return None
    
    try:
        # Đọc toàn bộ nội dung file để đếm số dòng
        with open(duong_dan_file, 'r', encoding='utf-8') as file:
            noi_dung = file.readlines()
        
        # Đếm tổng số dòng
        tong_so_dong = len(noi_dung)
        
        # Đếm số dòng trống
        so_dong_trong = sum(1 for line in noi_dung if line.strip() == '')
        
        # Đếm số dòng không trống
        so_dong_khong_trong = tong_so_dong - so_dong_trong
        
        # Đọc file XML để đếm số lượng contentuid
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        
        # Đếm số lượng phần tử content và contentUID duy nhất
        so_luong_content = len(root.findall('.//content'))
        contentuid_list = [content.get('contentuid') for content in root.findall('.//content')]
        contentuid_duy_nhat = list(set(contentuid_list))
        so_luong_contentuid_duy_nhat = len(contentuid_duy_nhat)
        so_luong_contentuid_trung_lap = so_luong_content - so_luong_contentuid_duy_nhat
        
        # Lấy thông tin về kích thước file
        kich_thuoc_file = os.path.getsize(duong_dan_file)
        kich_thuoc_kb = kich_thuoc_file / 1024
        
        # Hiển thị kết quả
        print(f"\nKết quả phân tích file: {duong_dan_file}")
        print(f"- Tổng số dòng: {tong_so_dong}")
        print(f"- Số dòng trống: {so_dong_trong}")
        print(f"- Số dòng không trống: {so_dong_khong_trong}")
        print(f"- Số lượng content: {so_luong_content}")
        print(f"- Số lượng contentUID duy nhất: {so_luong_contentuid_duy_nhat}")
        if so_luong_contentuid_trung_lap > 0:
            print(f"- Số lượng contentUID trùng lặp: {so_luong_contentuid_trung_lap}")
        print(f"- Kích thước file: {kich_thuoc_kb:.2f} KB")
        
        return {
            'duong_dan': duong_dan_file,
            'tong_so_dong': tong_so_dong,
            'so_dong_trong': so_dong_trong,
            'so_dong_khong_trong': so_dong_khong_trong,
            'so_luong_content': so_luong_content,
            'so_luong_contentuid_duy_nhat': so_luong_contentuid_duy_nhat,
            'so_luong_contentuid_trung_lap': so_luong_contentuid_trung_lap,
            'kich_thuoc_kb': kich_thuoc_kb,
            'contentuid_list': contentuid_duy_nhat
        }
        
    except Exception as e:
        print(f"Lỗi khi phân tích file: {e}")
        return None

def tim_contentuid_trung_lap_trong_file(duong_dan_file):
    """
    Tìm các contentUID trùng lặp trong cùng một file
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML
        
    Returns:
        dict: Thông tin về các contentUID trùng lặp
    """
    try:
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        
        contentuid_count = {}
        contentuid_trung_lap = {}
        
        # Đếm số lần xuất hiện của mỗi contentUID
        for content in root.findall('.//content'):
            contentuid = content.get('contentuid')
            if contentuid:
                if contentuid in contentuid_count:
                    contentuid_count[contentuid] += 1
                    if contentuid not in contentuid_trung_lap:
                        contentuid_trung_lap[contentuid] = []
                    contentuid_trung_lap[contentuid].append(content.text)
                else:
                    contentuid_count[contentuid] = 1
        
        # Lọc ra những contentUID xuất hiện nhiều hơn 1 lần
        contentuid_trung_lap_filtered = {k: v for k, v in contentuid_trung_lap.items() if contentuid_count[k] > 1}
        
        if contentuid_trung_lap_filtered:
            print(f"\nTìm thấy {len(contentuid_trung_lap_filtered)} contentUID trùng lặp trong file:")
            for contentuid, noi_dung_list in contentuid_trung_lap_filtered.items():
                print(f"- {contentuid}: xuất hiện {contentuid_count[contentuid]} lần")
                for i, noi_dung in enumerate(noi_dung_list):
                    noi_dung_rut_gon = noi_dung[:50] + "..." if len(noi_dung) > 50 else noi_dung
                    print(f"  {i+1}. {noi_dung_rut_gon}")
        else:
            print("\nKhông tìm thấy contentUID trùng lặp trong file")
            
        return {
            'so_luong_trung_lap': len(contentuid_trung_lap_filtered),
            'contentuid_trung_lap': contentuid_trung_lap_filtered,
            'contentuid_count': contentuid_count
        }
        
    except Exception as e:
        print(f"Lỗi khi tìm contentUID trùng lặp: {e}")
        return None

def so_sanh_hai_file_xml(file_a, file_b):
    """
    So sánh hai file XML để tìm các contentuid trùng nhau và không trùng nhau
    
    Args:
        file_a (str): Đường dẫn đến file XML thứ nhất
        file_b (str): Đường dẫn đến file XML thứ hai
        
    Returns:
        tuple: (ket_qua_trung, contentuid_chi_co_trong_a, contentuid_chi_co_trong_b)
            - ket_qua_trung: Danh sách các content trùng nhau giữa hai file
            - contentuid_chi_co_trong_a: Set các contentuid chỉ có trong file A
            - contentuid_chi_co_trong_b: Set các contentuid chỉ có trong file B
    """
    # Phân tích cả hai file
    thong_tin_a = phan_tich_file_xml(file_a)
    thong_tin_b = phan_tich_file_xml(file_b)
    
    if not thong_tin_a or not thong_tin_b:
        return None, None, None
    
    # Tìm các contentuid trùng nhau và riêng biệt
    contentuid_a = set(thong_tin_a['contentuid_list'])
    contentuid_b = set(thong_tin_b['contentuid_list'])
    
    contentuid_trung = contentuid_a.intersection(contentuid_b)
    contentuid_chi_co_trong_a = contentuid_a - contentuid_b
    contentuid_chi_co_trong_b = contentuid_b - contentuid_a
    
    print(f"\nKết quả so sánh hai file:")
    print(f"- File A ({os.path.basename(file_a)}): {len(contentuid_a)} contentuid")
    print(f"- File B ({os.path.basename(file_b)}): {len(contentuid_b)} contentuid")
    print(f"- Số lượng contentuid trùng nhau: {len(contentuid_trung)}")
    print(f"- Số lượng contentuid chỉ có trong file A: {len(contentuid_chi_co_trong_a)}")
    print(f"- Số lượng contentuid chỉ có trong file B: {len(contentuid_chi_co_trong_b)}")
    
    # Đọc nội dung của các contentuid trùng nhau
    ket_qua_trung = []
    
    if contentuid_trung:
        # Đọc từ file A
        tree_a = ET.parse(file_a)
        root_a = tree_a.getroot()
        
        for content in root_a.findall('.//content'):
            contentuid = content.get('contentuid')
            if contentuid in contentuid_trung:
                ket_qua_trung.append((contentuid, content.text))
    
    return ket_qua_trung, contentuid_chi_co_trong_a, contentuid_chi_co_trong_b

def xuat_contentuid_trung_ra_file(ket_qua_trung):
    """
    Xuất danh sách contentuid trùng nhau ra file XML
    
    Args:
        ket_qua_trung (list): Danh sách các contentuid trùng nhau và nội dung
        
    Returns:
        str: Đường dẫn file kết quả
    """
    try:
        # Tạo thư mục output/filtered nếu chưa tồn tại
        output_dir = os.path.join("output", "filtered")
        os.makedirs(output_dir, exist_ok=True)
        
        # Tạo tên file với thời gian hiện tại
        thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
        ten_file = os.path.join(output_dir, f"trung_contentuid_{thoi_gian}.xml")
        
        with open(ten_file, 'w', encoding='utf-8') as f:
            # Viết khai báo XML
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<contentList>\n')
            
            # Thêm phần tử chú thích
            f.write(f'\t<!-- Danh sách {len(ket_qua_trung)} contentuid trùng nhau - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -->\n')
            
            # Thêm các contentuid trùng nhau
            for contentuid, noi_dung in ket_qua_trung:
                # Escape XML special characters in content
                if noi_dung:
                    noi_dung = noi_dung.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')
                else:
                    noi_dung = ""
                f.write(f'\t<content contentuid="{contentuid}">{noi_dung}</content>\n')
            
            # Kết thúc file
            f.write('</contentList>\n')
            
        print(f"Đã xuất danh sách contentuid trùng nhau ra file: {ten_file}")
        return ten_file
        
    except Exception as e:
        print(f"Lỗi khi xuất file: {e}")
        return None

def lay_noi_dung_theo_contentuid(duong_dan_file, contentuid_list):
    """
    Lấy nội dung từ file XML theo danh sách contentuid
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML
        contentuid_list (set): Tập hợp các contentuid cần lấy
        
    Returns:
        list: Danh sách các cặp (contentuid, nội dung)
    """
    try:
        # Đọc file XML
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        
        # Lấy nội dung của các contentuid
        ket_qua = []
        for content in root.findall('.//content'):
            contentuid = content.get('contentuid')
            if contentuid in contentuid_list:
                ket_qua.append((contentuid, content.text))
        
        return ket_qua
        
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return []

def xuat_contentuid_khong_trung_ra_file(ket_qua, ten_prefix="khong_trung_fileA"):
    """
    Xuất danh sách contentuid không trùng nhau ra file XML
    
    Args:
        ket_qua (list): Danh sách các cặp (contentuid, nội dung) không trùng nhau
        ten_prefix (str): Tiền tố tên file (mặc định: "khong_trung_fileA")
        
    Returns:
        str: Đường dẫn file kết quả
    """
    try:
        # Tạo thư mục output/filtered nếu chưa tồn tại
        output_dir = os.path.join("output", "filtered")
        os.makedirs(output_dir, exist_ok=True)
        
        # Tạo tên file với thời gian hiện tại
        thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
        ten_file = os.path.join(output_dir, f"{ten_prefix}_{thoi_gian}.xml")
        
        root = ET.Element("contentList")
        
        # Thêm phần tử chú thích
        comment = ET.SubElement(root, "comment")
        comment.text = f"Danh sách {len(ket_qua)} contentuid không trùng nhau - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Thêm các contentuid không trùng nhau
        for contentuid, noi_dung in ket_qua:
            content_element = ET.SubElement(root, "content")
            content_element.set("contentuid", contentuid)
            content_element.text = noi_dung
        
        # Ghi file với định dạng đẹp
        formatted_xml = format_xml(root)
        with open(ten_file, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write(formatted_xml)
            
        print(f"Đã xuất danh sách contentuid không trùng nhau ra file: {ten_file}")
        return ten_file
        
    except Exception as e:
        print(f"Lỗi khi xuất file: {e}")
        return None

def xoa_contentuid_trung_trong_file(duong_dan_file, contentuid_list):
    """
    Xóa các contentuid trùng nhau trong file, giữ nguyên cấu trúc và format của file gốc
    
    Args:
        duong_dan_file (str): Đường dẫn đến file cần xóa
        contentuid_list (list): Danh sách các contentuid cần xóa
        
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
    """
    try:
        # Đọc nội dung file theo từng dòng
        with open(duong_dan_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Tạo file backup trước khi ghi đè
        backup_dir = os.path.dirname(duong_dan_file)
        backup_file = os.path.join(backup_dir, f"backup_{os.path.basename(duong_dan_file)}")
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Đã tạo file backup: {backup_file}")
        
        # Xác định các dòng cần xóa
        dang_xoa = False
        so_luong_xoa = 0
        new_lines = []
        
        for i, line in enumerate(lines):
            # Tìm dòng bắt đầu của content với contentuid trong danh sách cần xóa
            if '<content contentuid="' in line:
                found_uid = False
                for uid in contentuid_list:
                    if f'contentuid="{uid}"' in line or f"contentuid='{uid}'" in line:
                        found_uid = True
                        dang_xoa = True
                        so_luong_xoa += 1
                        break
                
                if not found_uid:
                    dang_xoa = False
                    new_lines.append(line)
            
            # Nếu đang ở trong phần tử cần xóa, tiếp tục bỏ qua các dòng
            elif dang_xoa:
                if '</content>' in line:
                    dang_xoa = False
            
            # Nếu không phải dòng cần xóa, giữ lại dòng đó
            else:
                new_lines.append(line)
        
        # Ghi lại file với các dòng đã lọc
        with open(duong_dan_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"Đã xóa {so_luong_xoa} contentuid trùng nhau từ file: {duong_dan_file}")
        return True
        
    except Exception as e:
        print(f"Lỗi khi xóa nội dung: {e}")
        return False

def tim_loc_xoa():
    """
    Chức năng tìm kiếm, lọc và xóa nội dung
    """
    print("\nCHỨC NĂNG TÌM KIẾM VÀ XÓA NỘI DUNG")
    print("------------------------------------")
    
    while True:
        # Nhập đường dẫn file XML
        duong_dan_file = get_input_with_space_exit("\nNhập đường dẫn đến file XML (nhấn Space để quay lại): ")
        if duong_dan_file == ' ':
            break
        
        if not os.path.exists(duong_dan_file):
            print(f"Lỗi: File {duong_dan_file} không tồn tại")
            continue
        
        # Kiểm tra xem có phải là file XML không
        if not duong_dan_file.lower().endswith('.xml'):
            print(f"Lỗi: File {duong_dan_file} không phải là file XML")
            continue
        
        # Nhập nội dung tìm kiếm
        noi_dung_tim_kiem = input("Nhập nội dung cần tìm kiếm: ")
        if not noi_dung_tim_kiem:
            print("Nội dung tìm kiếm không được để trống")
            continue
        
        # Thực hiện tìm kiếm
        ket_qua = tim_kiem_noi_dung(duong_dan_file, noi_dung_tim_kiem)
        
        if not ket_qua:
            print("Không tìm thấy kết quả phù hợp")
            continue
        
        # Xuất kết quả ra file XML
        file_ket_qua = xuat_ket_qua_ra_xml(ket_qua, noi_dung_tim_kiem)
        
        # Hỏi người dùng có muốn xóa không
        lua_chon = input("\nChọn chức năng (Xóa/Tiếp tục): ").lower()
        if lua_chon == "xóa" or lua_chon == "xoa":
            xoa_noi_dung(duong_dan_file, ket_qua)

def get_input_with_space_exit(prompt):
    """
    Lấy đầu vào từ người dùng, cho phép sử dụng phím Space để quay lại
    
    Args:
        prompt (str): Thông báo hiển thị cho người dùng
        
    Returns:
        str: Chuỗi đầu vào từ người dùng, trả về ' ' nếu người dùng chỉ nhấn Space
    """
    user_input = input(prompt)
    if user_input == ' ':
        return ' '
    return user_input

def format_xml(element):
    """
    Định dạng XML để dễ đọc với thụt lề đúng
    
    Args:
        element: Phần tử XML cần định dạng
        
    Returns:
        str: Chuỗi XML đã được định dạng đẹp, không bao gồm khai báo XML
    """
    # Chuyển đổi thành chuỗi
    rough_string = ET.tostring(element, encoding='utf-8').decode('utf-8')
    
    # Sử dụng minidom để định dạng
    parsed = minidom.parseString(rough_string)
    formatted_xml = parsed.toprettyxml(indent="\t")
    
    # Loại bỏ dòng trống thừa và khai báo XML
    lines = []
    for line in formatted_xml.split('\n'):
        if line.strip() and not line.startswith('<?xml'):
            lines.append(line)
    
    formatted_xml = '\n'.join(lines)
    
    # Xử lý comment để hiển thị đúng
    formatted_xml = formatted_xml.replace("<!--", "<!-- ").replace("-->", " -->")
    
    return formatted_xml

def phan_tich():
    """
    Chức năng phân tích file XML
    """
    print("\nCHỨC NĂNG PHÂN TÍCH FILE XML")
    print("--------------------------")
    
    while True:
        # Nhập đường dẫn file XML
        duong_dan_file = get_input_with_space_exit("\nNhập đường dẫn đến file XML (nhấn Space để quay lại): ")
        if duong_dan_file == ' ':
            break
        
        if not os.path.exists(duong_dan_file):
            print(f"Lỗi: File {duong_dan_file} không tồn tại")
            continue
        
        # Kiểm tra xem có phải là file XML không
        if not duong_dan_file.lower().endswith('.xml'):
            print(f"Lỗi: File {duong_dan_file} không phải là file XML")
            continue
        
        # Thực hiện phân tích
        ket_qua = phan_tich_file_xml(duong_dan_file)
        
        if ket_qua and ket_qua['so_luong_contentuid_trung_lap'] > 0:
            print(f"\n⚠️  Phát hiện {ket_qua['so_luong_contentuid_trung_lap']} contentUID trùng lặp!")
            kiem_tra = input("Bạn có muốn xem chi tiết các contentUID trùng lặp? (y/n): ")
            if kiem_tra.lower() == 'y':
                tim_contentuid_trung_lap_trong_file(duong_dan_file)

def so_sanh():
    """
    Chức năng so sánh hai file XML
    """
    print("\nCHỨC NĂNG SO SÁNH HAI FILE XML")
    print("------------------------------")
    
    while True:
        # Nhập đường dẫn file XML thứ nhất
        file_a = get_input_with_space_exit("\nNhập đường dẫn đến file XML thứ nhất (nhấn Space để quay lại): ")
        if file_a == ' ':
            break
        
        if not os.path.exists(file_a):
            print(f"Lỗi: File {file_a} không tồn tại")
            continue
        
        if not file_a.lower().endswith('.xml'):
            print(f"Lỗi: File {file_a} không phải là file XML")
            continue
        
        # Nhập đường dẫn file XML thứ hai
        file_b = input("Nhập đường dẫn đến file XML thứ hai: ")
        if not os.path.exists(file_b):
            print(f"Lỗi: File {file_b} không tồn tại")
            continue
        
        if not file_b.lower().endswith('.xml'):
            print(f"Lỗi: File {file_b} không phải là file XML")
            continue
        
        # Thực hiện so sánh
        ket_qua_trung, contentuid_chi_co_trong_a, contentuid_chi_co_trong_b = so_sanh_hai_file_xml(file_a, file_b)
        
        if not ket_qua_trung and not contentuid_chi_co_trong_a and not contentuid_chi_co_trong_b:
            print("Lỗi khi so sánh hai file")
            continue
        
        # Hiển thị menu chức năng
        print("\nChọn chức năng:")
        print("--- Xử lý các contentUID trùng nhau ---")
        print("1. Lọc các contentUID trùng nhau ra file")
        print("2. Lọc và xóa các contentUID trùng nhau ở file A")
        print("3. Lọc và xóa các contentUID trùng nhau ở file B")
        print("4. Lọc và xóa các contentUID trùng nhau ở cả hai file")
        print("5. Xóa các contentUID trùng nhau ở file A")
        print("6. Xóa các contentUID trùng nhau ở file B")
        print("7. Xóa các contentUID trùng nhau ở cả hai file")
        print("--- Xử lý các contentUID KHÔNG trùng nhau ---")
        print("8. Lọc các contentUID chỉ có trong file A ra file")
        print("9. Lọc các contentUID chỉ có trong file B ra file")
        print("10. Lọc các contentUID không trùng nhau ở cả hai file")
        print("0. Quay lại")
        print("00. Quay về màn hình chính")
        
        lua_chon = input("\nNhập lựa chọn của bạn: ")
        
        if lua_chon == "0":
            continue
        elif lua_chon == "00":
            break
            
        elif lua_chon == "1":
            # Lọc ra file
            xuat_contentuid_trung_ra_file(ket_qua_trung)
            
        elif lua_chon == "2":
            # Lọc và xóa ở file A
            file_ket_qua = xuat_contentuid_trung_ra_file(ket_qua_trung)
            xoa_contentuid_trung_trong_file(file_a, [uid for uid, _ in ket_qua_trung])
            
        elif lua_chon == "3":
            # Lọc và xóa ở file B
            file_ket_qua = xuat_contentuid_trung_ra_file(ket_qua_trung)
            xoa_contentuid_trung_trong_file(file_b, [uid for uid, _ in ket_qua_trung])
            
        elif lua_chon == "4":
            # Lọc và xóa ở cả hai file
            file_ket_qua = xuat_contentuid_trung_ra_file(ket_qua_trung)
            xoa_contentuid_trung_trong_file(file_a, [uid for uid, _ in ket_qua_trung])
            xoa_contentuid_trung_trong_file(file_b, [uid for uid, _ in ket_qua_trung])
            
        elif lua_chon == "5":
            # Xóa ở file A
            xoa_contentuid_trung_trong_file(file_a, [uid for uid, _ in ket_qua_trung])
            
        elif lua_chon == "6":
            # Xóa ở file B
            xoa_contentuid_trung_trong_file(file_b, [uid for uid, _ in ket_qua_trung])
            
        elif lua_chon == "7":
            # Xóa ở cả hai file
            xoa_contentuid_trung_trong_file(file_a, [uid for uid, _ in ket_qua_trung])
            xoa_contentuid_trung_trong_file(file_b, [uid for uid, _ in ket_qua_trung])
            
        elif lua_chon == "8":
            # Lọc các contentUID chỉ có trong file A
            if contentuid_chi_co_trong_a:
                # Lấy nội dung từ file A
                ket_qua_a = lay_noi_dung_theo_contentuid(file_a, contentuid_chi_co_trong_a)
                if ket_qua_a:
                    xuat_contentuid_khong_trung_ra_file(ket_qua_a, "chi_co_trong_fileA")
                else:
                    print("Không thể lấy nội dung từ file A")
            else:
                print("Không có contentUID nào chỉ xuất hiện trong file A")
            
        elif lua_chon == "9":
            # Lọc các contentUID chỉ có trong file B
            if contentuid_chi_co_trong_b:
                # Lấy nội dung từ file B
                ket_qua_b = lay_noi_dung_theo_contentuid(file_b, contentuid_chi_co_trong_b)
                if ket_qua_b:
                    xuat_contentuid_khong_trung_ra_file(ket_qua_b, "chi_co_trong_fileB")
                else:
                    print("Không thể lấy nội dung từ file B")
            else:
                print("Không có contentUID nào chỉ xuất hiện trong file B")
            
        elif lua_chon == "10":
            # Lọc các contentUID không trùng nhau ở cả hai file
            if contentuid_chi_co_trong_a:
                # Lấy nội dung từ file A
                ket_qua_a = lay_noi_dung_theo_contentuid(file_a, contentuid_chi_co_trong_a)
                if ket_qua_a:
                    xuat_contentuid_khong_trung_ra_file(ket_qua_a, "chi_co_trong_fileA")
                else:
                    print("Không thể lấy nội dung từ file A")
                
            if contentuid_chi_co_trong_b:
                # Lấy nội dung từ file B
                ket_qua_b = lay_noi_dung_theo_contentuid(file_b, contentuid_chi_co_trong_b)
                if ket_qua_b:
                    xuat_contentuid_khong_trung_ra_file(ket_qua_b, "chi_co_trong_fileB")
                else:
                    print("Không thể lấy nội dung từ file B")
                    
            if not contentuid_chi_co_trong_a and not contentuid_chi_co_trong_b:
                print("Không có contentUID nào chỉ xuất hiện trong một file")
            
        else:
            print("Lựa chọn không hợp lệ")

def main():
    print("CÔNG CỤ XỬ LÝ FILE XML")
    print("----------------------")
    
    while True:
        print("\nChọn chức năng:")
        print("1. Tìm kiếm và xóa nội dung")
        print("2. Phân tích file")
        print("3. So sánh hai file")
        print("0. Thoát")
        
        lua_chon = input("\nNhập lựa chọn của bạn: ")
        
        if lua_chon == "0":
            break
            
        elif lua_chon == "1":
            tim_loc_xoa()
            
        elif lua_chon == "2":
            phan_tich()
            
        elif lua_chon == "3":
            so_sanh()
            
        else:
            print("Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()

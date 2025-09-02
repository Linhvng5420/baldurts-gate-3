#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tim_Loc_Xoa.py - Tool tìm kiếm, xóa, so sánh và phân tích file XML
"""

import os
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import sys

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
        
        # Ghi ra file
        tree = ET.ElementTree(root)
        tree.write(ten_file, encoding="utf-8", xml_declaration=True)
        
        print(f"Đã xuất kết quả ra file XML: {ten_file}")
        return ten_file
        
    except Exception as e:
        print(f"Lỗi khi xuất file XML: {e}")
        return None

def xoa_noi_dung(duong_dan_file, ket_qua):
    """
    Xóa nội dung đã tìm thấy từ file
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML cần xóa nội dung
        ket_qua (list): Danh sách các phần tử cần xóa (contentuid, nội dung, dòng XML)
        
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
    """
    try:
        # Đọc file XML
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        
        # Tạo danh sách contentuid cần xóa
        uid_can_xoa = [item[0] for item in ket_qua]
        
        # Đếm số phần tử bị xóa
        so_luong_xoa = 0
        
        # Tìm và xóa các phần tử content có contentuid trong danh sách cần xóa
        for content in root.findall('.//content'):
            content_uid = content.get('contentuid')
            if content_uid in uid_can_xoa:
                root.remove(content)
                so_luong_xoa += 1
        
        # Kiểm tra nếu số lượng xóa khác với số lượng tìm thấy
        if so_luong_xoa != len(uid_can_xoa):
            print(f"Cảnh báo: Chỉ tìm thấy và xóa {so_luong_xoa}/{len(uid_can_xoa)} phần tử")
        
        # Tạo file backup trước khi ghi đè
        backup_dir = os.path.dirname(duong_dan_file)
        backup_file = os.path.join(backup_dir, f"backup_{os.path.basename(duong_dan_file)}")
        tree.write(backup_file, encoding="utf-8", xml_declaration=True)
        print(f"Đã tạo file backup: {backup_file}")
        
        # Ghi lại file gốc
        tree.write(duong_dan_file, encoding="utf-8", xml_declaration=True)
        
        print(f"Đã xóa {so_luong_xoa} phần tử từ file: {duong_dan_file}")
        return True
        
    except Exception as e:
        print(f"Lỗi khi xóa nội dung: {e}")
        return False

def phan_tich_file(duong_dan_file):
    """
    Phân tích thông tin của file XML
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML cần phân tích
        
    Returns:
        dict: Thông tin phân tích
    """
    if not os.path.exists(duong_dan_file):
        print(f"Lỗi: File {duong_dan_file} không tồn tại")
        return None
    
    try:
        # Đọc file XML
        with open(duong_dan_file, 'r', encoding='utf-8') as file:
            noi_dung = file.readlines()
        
        # Đếm tổng số dòng
        so_dong = len(noi_dung)
        
        # Đếm số dòng trống
        so_dong_trong = sum(1 for dong in noi_dung if dong.strip() == '')
        
        # Đếm số dòng trừ khoảng trắng
        so_dong_co_noi_dung = so_dong - so_dong_trong
        
        # Đếm số lượng contentuid
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        so_contentuid = len(root.findall('.//content'))
        
        # Hiển thị thông tin
        print(f"\nThông tin phân tích file: {duong_dan_file}")
        print(f"- Tổng số dòng: {so_dong}")
        print(f"- Số dòng trống: {so_dong_trong}")
        print(f"- Số dòng có nội dung: {so_dong_co_noi_dung}")
        print(f"- Tổng số contentuid: {so_contentuid}")
        
        return {
            'duong_dan': duong_dan_file,
            'so_dong': so_dong,
            'so_dong_trong': so_dong_trong,
            'so_dong_co_noi_dung': so_dong_co_noi_dung,
            'so_contentuid': so_contentuid
        }
        
    except Exception as e:
        print(f"Lỗi khi phân tích file: {e}")
        return None

def lay_danh_sach_contentuid(duong_dan_file):
    """
    Lấy danh sách contentuid từ file XML
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML
        
    Returns:
        dict: Dictionary với key là contentuid, value là nội dung và các thuộc tính khác
    """
    if not os.path.exists(duong_dan_file):
        print(f"Lỗi: File {duong_dan_file} không tồn tại")
        return {}
    
    try:
        # Đọc file XML
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        
        # Tạo dictionary lưu contentuid và nội dung
        contentuid_dict = {}
        
        for content in root.findall('.//content'):
            content_uid = content.get('contentuid')
            if content_uid:
                # Lưu element và tất cả thuộc tính
                contentuid_dict[content_uid] = {
                    'element': content,
                    'text': content.text or '',
                    'attributes': {k: v for k, v in content.attrib.items()}
                }
        
        return contentuid_dict
        
    except Exception as e:
        print(f"Lỗi khi lấy danh sách contentuid: {e}")
        return {}

def so_sanh_file(duong_dan_file_a, duong_dan_file_b):
    """
    So sánh hai file XML
    
    Args:
        duong_dan_file_a (str): Đường dẫn đến file XML A
        duong_dan_file_b (str): Đường dẫn đến file XML B
        
    Returns:
        tuple: Danh sách contentuid chung, riêng file A, riêng file B
    """
    print("\nĐang tiến hành so sánh hai file...")
    
    # Phân tích cả hai file
    phan_tich_a = phan_tich_file(duong_dan_file_a)
    phan_tich_b = phan_tich_file(duong_dan_file_b)
    
    if not phan_tich_a or not phan_tich_b:
        return None, None, None
    
    # Lấy danh sách contentuid của hai file
    contentuid_a = lay_danh_sach_contentuid(duong_dan_file_a)
    contentuid_b = lay_danh_sach_contentuid(duong_dan_file_b)
    
    # Tìm contentuid chung và riêng
    contentuid_chung = {}
    for uid in contentuid_a:
        if uid in contentuid_b:
            contentuid_chung[uid] = {
                'a': contentuid_a[uid],
                'b': contentuid_b[uid]
            }
    
    contentuid_rieng_a = {uid: contentuid_a[uid] for uid in contentuid_a if uid not in contentuid_b}
    contentuid_rieng_b = {uid: contentuid_b[uid] for uid in contentuid_b if uid not in contentuid_a}
    
    # Hiển thị thông tin so sánh
    print("\nKết quả so sánh:")
    print(f"- Số lượng contentuid trong file A: {len(contentuid_a)}")
    print(f"- Số lượng contentuid trong file B: {len(contentuid_b)}")
    print(f"- Số lượng contentuid trùng nhau: {len(contentuid_chung)}")
    print(f"- Số lượng contentuid riêng file A: {len(contentuid_rieng_a)}")
    print(f"- Số lượng contentuid riêng file B: {len(contentuid_rieng_b)}")
    
    return contentuid_chung, contentuid_rieng_a, contentuid_rieng_b

def xuat_contentuid_chung(contentuid_chung, ten_file="trung_contentuid.xml"):
    """
    Xuất danh sách contentuid trùng nhau ra file
    
    Args:
        contentuid_chung (dict): Dictionary chứa contentuid trùng nhau
        ten_file (str): Tên file xuất
        
    Returns:
        str: Đường dẫn file đã xuất
    """
    try:
        # Tạo thư mục output/filtered nếu chưa tồn tại
        output_dir = os.path.join("output", "filtered")
        os.makedirs(output_dir, exist_ok=True)
        
        # Tạo tên file với thời gian hiện tại
        thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
        ten_file_day_du = os.path.join(output_dir, f"{os.path.splitext(ten_file)[0]}_{thoi_gian}.xml")
        
        root = ET.Element("contentList")
        
        # Thêm phần tử chú thích
        comment = ET.SubElement(root, "comment")
        comment.text = f"Danh sách contentuid trùng nhau - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Thêm các contentuid trùng nhau
        for uid, data in contentuid_chung.items():
            # Lấy phần tử từ file A
            element_info = data['a']
            
            # Tạo phần tử content mới với các thuộc tính của phần tử gốc
            content_element = ET.SubElement(root, "content")
            for key, value in element_info['attributes'].items():
                content_element.set(key, value)
            content_element.text = element_info['text']
        
        # Ghi ra file
        tree = ET.ElementTree(root)
        tree.write(ten_file_day_du, encoding="utf-8", xml_declaration=True)
        
        print(f"Đã xuất danh sách contentuid trùng nhau ra file: {ten_file_day_du}")
        return ten_file_day_du
        
    except Exception as e:
        print(f"Lỗi khi xuất contentuid trùng nhau: {e}")
        return None

def xoa_contentuid_trung_nhau(duong_dan_file, contentuid_can_xoa):
    """
    Xóa các contentuid trùng nhau từ file
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML cần xóa
        contentuid_can_xoa (list): Danh sách contentuid cần xóa
        
    Returns:
        bool: True nếu xóa thành công, False nếu có lỗi
    """
    try:
        # Đọc file XML
        tree = ET.parse(duong_dan_file)
        root = tree.getroot()
        
        # Đếm số phần tử bị xóa
        so_luong_xoa = 0
        
        # Tìm và xóa các phần tử content có contentuid trong danh sách cần xóa
        for content in root.findall('.//content'):
            content_uid = content.get('contentuid')
            if content_uid in contentuid_can_xoa:
                root.remove(content)
                so_luong_xoa += 1
        
        # Tạo file backup trước khi ghi đè
        backup_dir = os.path.dirname(duong_dan_file)
        backup_file = os.path.join(backup_dir, f"backup_{os.path.basename(duong_dan_file)}")
        tree.write(backup_file, encoding="utf-8", xml_declaration=True)
        print(f"Đã tạo file backup: {backup_file}")
        
        # Ghi lại file gốc
        tree.write(duong_dan_file, encoding="utf-8", xml_declaration=True)
        
        print(f"Đã xóa {so_luong_xoa} phần tử từ file: {duong_dan_file}")
        return True
        
    except Exception as e:
        print(f"Lỗi khi xóa contentuid: {e}")
        return False

def tim_loc_xoa_menu():
    """
    Menu chức năng Tìm, Lọc, Xóa
    """
    print("\nCHỨC NĂNG TÌM KIẾM VÀ XÓA NỘI DUNG")
    print("------------------------------------------------")
    
    while True:
        # Nhập đường dẫn file XML
        duong_dan_file = input("\nNhập đường dẫn đến file XML (nhấn Enter để quay lại menu chính): ")
        if not duong_dan_file:
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
        
        print("\n------------------------------------------------")

def so_sanh_menu():
    """
    Menu chức năng So sánh
    """
    print("\nCHỨC NĂNG SO SÁNH HAI FILE XML")
    print("------------------------------------------------")
    
    # Nhập đường dẫn file A
    duong_dan_file_a = input("\nNhập đường dẫn đến file XML A (nhấn Enter để quay lại menu chính): ")
    if not duong_dan_file_a:
        return
    
    if not os.path.exists(duong_dan_file_a):
        print(f"Lỗi: File {duong_dan_file_a} không tồn tại")
        return
    
    if not duong_dan_file_a.lower().endswith('.xml'):
        print(f"Lỗi: File {duong_dan_file_a} không phải là file XML")
        return
    
    # Nhập đường dẫn file B
    duong_dan_file_b = input("Nhập đường dẫn đến file XML B: ")
    if not duong_dan_file_b:
        print("Đường dẫn file B không được để trống")
        return
    
    if not os.path.exists(duong_dan_file_b):
        print(f"Lỗi: File {duong_dan_file_b} không tồn tại")
        return
    
    if not duong_dan_file_b.lower().endswith('.xml'):
        print(f"Lỗi: File {duong_dan_file_b} không phải là file XML")
        return
    
    # Tiến hành so sánh
    contentuid_chung, contentuid_rieng_a, contentuid_rieng_b = so_sanh_file(duong_dan_file_a, duong_dan_file_b)
    
    if contentuid_chung is None:
        return
    
    if not contentuid_chung:
        print("\nKhông có contentuid trùng nhau giữa hai file.")
        return
    
    while True:
        # Hiển thị menu lựa chọn
        print("\nLựa chọn xử lý contentuid trùng nhau:")
        print("1. Lọc các contentuid trùng nhau ra file trung_contentuid.xml")
        print("2. Lọc contentuid trùng nhau ra file và xóa chúng ở file A")
        print("3. Lọc contentuid trùng nhau ra file và xóa chúng ở file B")
        print("4. Lọc contentuid trùng nhau ra file và xóa chúng ở cả hai file")
        print("5. Xóa contentuid trùng nhau ở file A")
        print("6. Xóa contentuid trùng nhau ở file B")
        print("7. Xóa contentuid trùng nhau ở cả hai file")
        print("0. Quay lại")
        
        lua_chon = input("Nhập lựa chọn của bạn: ")
        
        if lua_chon == "0":
            break
        
        # Lọc ra file
        if lua_chon in ["1", "2", "3", "4"]:
            ten_file_xuat = xuat_contentuid_chung(contentuid_chung)
        
        # Xóa ở file A
        if lua_chon in ["2", "4", "5", "7"]:
            xoa_contentuid_trung_nhau(duong_dan_file_a, contentuid_chung.keys())
        
        # Xóa ở file B
        if lua_chon in ["3", "4", "6", "7"]:
            xoa_contentuid_trung_nhau(duong_dan_file_b, contentuid_chung.keys())
        
        if lua_chon not in ["0", "1", "2", "3", "4", "5", "6", "7"]:
            print("Lựa chọn không hợp lệ!")

def phan_tich_menu():
    """
    Menu chức năng Phân tích
    """
    print("\nCHỨC NĂNG PHÂN TÍCH FILE XML")
    print("------------------------------------------------")
    
    # Nhập đường dẫn file
    duong_dan_file = input("\nNhập đường dẫn đến file XML (nhấn Enter để quay lại menu chính): ")
    if not duong_dan_file:
        return
    
    if not os.path.exists(duong_dan_file):
        print(f"Lỗi: File {duong_dan_file} không tồn tại")
        return
    
    if not duong_dan_file.lower().endswith('.xml'):
        print(f"Lỗi: File {duong_dan_file} không phải là file XML")
        return
    
    # Tiến hành phân tích
    phan_tich_file(duong_dan_file)

def main():
    print("CÔNG CỤ TÌM KIẾM, XÓA, SO SÁNH VÀ PHÂN TÍCH FILE XML")
    print("====================================================")
    
    while True:
        print("\nCHỌN CHỨC NĂNG:")
        print("1. Tìm kiếm và Xóa nội dung")
        print("2. So sánh hai file")
        print("3. Phân tích file")
        print("0. Thoát")
        
        lua_chon = input("Nhập lựa chọn của bạn: ")
        
        if lua_chon == "0":
            print("\nĐã thoát chương trình!")
            break
        
        elif lua_chon == "1":
            tim_loc_xoa_menu()
        
        elif lua_chon == "2":
            so_sanh_menu()
        
        elif lua_chon == "3":
            phan_tich_menu()
        
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()

import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

# Thêm từ điển các từ tiếng Anh thường gặp trong game và bản dịch tiếng Việt tương ứng
TU_DIEN_PHO_BIEN = {
    "is": "là",
    "are": "là",
    "am": "là",
    "you": "bạn",
    "I": "tôi",
    "we": "chúng ta",
    "they": "họ",
    "he": "anh ấy",
    "she": "cô ấy",
    "hello": "xin chào",
    "hi": "chào",
    "what": "gì",
    "where": "ở đâu",
    "when": "khi nào",
    "why": "tại sao",
    "how": "thế nào",

}

def tim_kiem_noi_dung(duong_dan_file, tu_khoa_list, hien_thi_ket_qua=True, xuat_file=False, dinh_dang_xuat='txt'):
    """
    Tìm kiếm nội dung trong file XML dựa trên danh sách từ khóa
    
    Args:
        duong_dan_file (str): Đường dẫn đến file XML cần tìm kiếm
        tu_khoa_list (list): Danh sách các từ khóa cần tìm
        hien_thi_ket_qua (bool): Hiển thị kết quả tìm kiếm
        xuat_file (bool): Xuất kết quả ra file
        dinh_dang_xuat (str): Định dạng file xuất (txt hoặc xml)
        
    Returns:
        list: Danh sách các cặp (contentuid, nội dung, từ khóa, dòng XML) tìm thấy
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
        
        # Tìm kiếm các phần tử content chứa từ khóa
        ket_qua = []
        so_luong = 0
        
        # Xử lý các từ khóa tiếng Anh phổ biến
        tu_khoa_tim_kiem = []
        for tu_khoa in tu_khoa_list:
            tu_khoa = tu_khoa.strip().lower()
            if tu_khoa in TU_DIEN_PHO_BIEN:
                tu_khoa_tim_kiem.append(TU_DIEN_PHO_BIEN[tu_khoa])
                tu_khoa_tim_kiem.append(tu_khoa)  # Vẫn giữ từ tiếng Anh để tìm trong các đoạn text tiếng Anh
            else:
                tu_khoa_tim_kiem.append(tu_khoa)
        
        # Loại bỏ từ khóa trùng lặp và rỗng
        tu_khoa_tim_kiem = [tk for tk in tu_khoa_tim_kiem if tk.strip()]
        tu_khoa_tim_kiem = list(dict.fromkeys(tu_khoa_tim_kiem))
        
        for content in root.findall('.//content'):
            noi_dung = content.text
            if noi_dung:
                content_uid = content.get('contentuid', 'không có uid')
                
                # Tạo dòng XML đầy đủ cho nội dung này
                xml_line = get_xml_line_for_element(xml_content, content_uid, noi_dung)
                
                # Kiểm tra từng từ khóa
                for tu_khoa in tu_khoa_tim_kiem:
                    tu_khoa_original = tu_khoa
                    if tu_khoa and tu_khoa.lower() in noi_dung.lower():
                        # Tìm ra từ khóa gốc từ danh sách nhập vào
                        tu_khoa_goc = tim_tu_khoa_goc(tu_khoa, tu_khoa_list)
                        ket_qua.append((content_uid, noi_dung, tu_khoa_goc, xml_line))
                        so_luong += 1
                        if hien_thi_ket_qua:
                            print(f"\n[{so_luong}] UID: {content_uid}")
                            print(f"Từ khóa: '{tu_khoa_goc}'")
                            print(f"Nội dung: {noi_dung}")
                            print(f"Dòng XML: {xml_line}")
                        break  # Tránh trùng lặp kết quả nếu nhiều từ khóa cùng xuất hiện trong một nội dung
        
        tu_khoa_str = "', '".join(tu_khoa_list)
        print(f"\nTìm thấy {so_luong} kết quả cho các từ khóa: '{tu_khoa_str}'")
        
        if xuat_file and ket_qua:
            xuat_ket_qua_ra_file(tu_khoa_list, ket_qua, dinh_dang_xuat)
        
        return ket_qua
    
    except Exception as e:
        print(f"Lỗi khi tìm kiếm: {e}")
        return []

def tim_tu_khoa_goc(tu_khoa_tim_thay, tu_khoa_list):
    """
    Tìm từ khóa gốc trong danh sách từ khóa nhập vào
    
    Args:
        tu_khoa_tim_thay (str): Từ khóa đã tìm thấy (có thể là bản dịch)
        tu_khoa_list (list): Danh sách từ khóa gốc nhập vào
        
    Returns:
        str: Từ khóa gốc tương ứng
    """
    # Nếu từ khóa tìm thấy nằm trong danh sách gốc, trả về chính nó
    tu_khoa_tim_thay_lower = tu_khoa_tim_thay.lower()
    for tk in tu_khoa_list:
        if tk.lower() == tu_khoa_tim_thay_lower:
            return tk
    
    # Nếu từ khóa tìm thấy là bản dịch, tìm từ khóa tiếng Anh tương ứng
    for eng, vie in TU_DIEN_PHO_BIEN.items():
        if vie.lower() == tu_khoa_tim_thay_lower:
            for tk in tu_khoa_list:
                if tk.lower() == eng:
                    return tk
    
    # Nếu không tìm thấy, trả về từ khóa đầu tiên trong danh sách
    return tu_khoa_list[0] if tu_khoa_list else tu_khoa_tim_thay

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

def xuat_ket_qua_ra_file(tu_khoa_list, ket_qua, dinh_dang='txt'):
    """
    Xuất kết quả tìm kiếm ra file
    
    Args:
        tu_khoa_list (list): Danh sách từ khóa đã tìm kiếm
        ket_qua (list): Danh sách kết quả tìm thấy
        dinh_dang (str): Định dạng file xuất (txt hoặc xml)
    """
    thoi_gian = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if dinh_dang.lower() == 'xml':
        ten_file = f"ket_qua_tim_kiem_{thoi_gian}.xml"
        xuat_ket_qua_ra_xml(tu_khoa_list, ket_qua, ten_file)
    else:
        ten_file = f"ket_qua_tim_kiem_{thoi_gian}.txt"
        xuat_ket_qua_ra_txt(tu_khoa_list, ket_qua, ten_file)

def xuat_ket_qua_ra_txt(tu_khoa_list, ket_qua, ten_file):
    """
    Xuất kết quả tìm kiếm ra file text
    
    Args:
        tu_khoa_list (list): Danh sách từ khóa đã tìm kiếm
        ket_qua (list): Danh sách kết quả tìm thấy
        ten_file (str): Tên file xuất
    """
    try:
        with open(ten_file, 'w', encoding='utf-8') as f:
            tu_khoa_str = "', '".join(tu_khoa_list)
            f.write(f"Kết quả tìm kiếm cho các từ khóa: '{tu_khoa_str}'\n")
            f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Số lượng kết quả: {len(ket_qua)}\n\n")
            
            for i, (uid, noi_dung, tu_khoa, xml_line) in enumerate(ket_qua, 1):
                f.write(f"[{i}] UID: {uid}\n")
                f.write(f"Từ khóa: '{tu_khoa}'\n")
                f.write(f"Nội dung: {noi_dung}\n")
                f.write(f"Dòng XML: {xml_line}\n\n")
        
        print(f"Đã xuất kết quả ra file text: {ten_file}")
    except Exception as e:
        print(f"Lỗi khi xuất file text: {e}")

def doc_tu_khoa_tu_file(duong_dan_file):
    """
    Đọc danh sách từ khóa từ một file txt
    
    Args:
        duong_dan_file (str): Đường dẫn đến file txt chứa từ khóa
        
    Returns:
        list: Danh sách các từ khóa đọc được
    """
    try:
        if not os.path.exists(duong_dan_file):
            print(f"Lỗi: File {duong_dan_file} không tồn tại")
            return []
        
        if not duong_dan_file.lower().endswith('.txt'):
            print(f"Lỗi: File {duong_dan_file} không phải là file TXT")
            return []
        
        with open(duong_dan_file, 'r', encoding='utf-8') as file:
            tu_khoa_list = []
            for line in file:
                line = line.strip()
                if line:  # Bỏ qua các dòng trống
                    # Nếu dòng có nhiều từ khóa cách nhau bằng dấu phẩy
                    if ',' in line:
                        tu_khoa_list.extend([tk.strip() for tk in line.split(',') if tk.strip()])
                    else:
                        tu_khoa_list.append(line)
        
        # Loại bỏ các từ khóa trùng lặp
        tu_khoa_list = list(dict.fromkeys(tu_khoa_list))
        
        print(f"Đã đọc được {len(tu_khoa_list)} từ khóa từ file")
        return tu_khoa_list
        
    except Exception as e:
        print(f"Lỗi khi đọc file từ khóa: {e}")
        return []

def xuat_ket_qua_ra_xml(tu_khoa_list, ket_qua, ten_file):
    """
    Xuất kết quả tìm kiếm ra file XML
    
    Args:
        tu_khoa_list (list): Danh sách từ khóa đã tìm kiếm
        ket_qua (list): Danh sách kết quả tìm thấy
        ten_file (str): Tên file xuất
    """
    try:
        root = ET.Element("contentList")
        
        # Thêm phần tử chú thích
        comment = ET.SubElement(root, "comment")
        tu_khoa_str = "', '".join(tu_khoa_list)
        comment.text = f"Kết quả tìm kiếm cho các từ khóa: '{tu_khoa_str}' - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Thêm các kết quả tìm được
        for uid, noi_dung, tu_khoa, xml_line in ket_qua:
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
    except Exception as e:
        print(f"Lỗi khi xuất file XML: {e}")

def hien_thi_tu_dien():
    """
    Hiển thị từ điển các từ phổ biến để người dùng tham khảo
    """
    print("\nDanh sách từ tiếng Anh phổ biến và bản dịch tiếng Việt:")
    print("-" * 50)
    
    # Sắp xếp từ điển theo bảng chữ cái
    tu_dien_sorted = sorted(TU_DIEN_PHO_BIEN.items())
    
    # Hiển thị theo cột
    width = max(len(k) for k, _ in tu_dien_sorted) + 2
    for i, (eng, vie) in enumerate(tu_dien_sorted, 1):
        print(f"{i:2d}. {eng:{width}} -> {vie}")

def main():
    print("CÔNG CỤ TÌM KIẾM NỘI DUNG TRONG FILE XML")
    print("----------------------------------------")
    print("(Có thể nhập nhiều từ khóa cách nhau bằng dấu phẩy)")
    print("(Hỗ trợ nhập từ tiếng Anh phổ biến)")
    
    while True:
        print("\n1. Tìm kiếm (nhập từ khóa trực tiếp)")
        print("2. Tìm kiếm (đọc từ khóa từ file)")
        print("3. Xem danh sách từ tiếng Anh phổ biến")
        print("0. Thoát")
        
        lua_chon = input("Nhập lựa chọn của bạn: ")
        
        if lua_chon == "0":
            break
        
        elif lua_chon == "3":
            hien_thi_tu_dien()
            continue
        
        elif lua_chon == "1" or lua_chon == "2":
            # Nhập đường dẫn file XML
            duong_dan_file = input("\nNhập đường dẫn đến file XML (nhấn Enter để thoát): ")
            if not duong_dan_file:
                continue
            
            if not os.path.exists(duong_dan_file):
                print(f"Lỗi: File {duong_dan_file} không tồn tại")
                continue
            
            # Kiểm tra xem có phải là file XML không
            if not duong_dan_file.lower().endswith('.xml'):
                print(f"Lỗi: File {duong_dan_file} không phải là file XML")
                continue
            
            # Lấy từ khóa tìm kiếm
            tu_khoa_list = []
            
            if lua_chon == "1":  # Nhập từ khóa trực tiếp
                # Nhập từ khóa tìm kiếm
                tu_khoa_input = input("Nhập từ khóa cần tìm kiếm (nhiều từ khóa cách nhau bằng dấu phẩy): ")
                if not tu_khoa_input:
                    print("Từ khóa không được để trống")
                    continue
                
                # Tách các từ khóa
                tu_khoa_list = [tk.strip() for tk in tu_khoa_input.split(',') if tk.strip()]
            
            elif lua_chon == "2":  # Đọc từ khóa từ file
                duong_dan_file_tu_khoa = input("Nhập đường dẫn đến file TXT chứa từ khóa: ")
                if not duong_dan_file_tu_khoa:
                    print("Đường dẫn file từ khóa không được để trống")
                    continue
                
                tu_khoa_list = doc_tu_khoa_tu_file(duong_dan_file_tu_khoa)
            
            if not tu_khoa_list:
                print("Không có từ khóa hợp lệ")
                continue
            
            # Hỏi xuất kết quả ra file
            xuat_file = input("Bạn có muốn xuất kết quả ra file không? (y/n): ").lower() == 'y'
            
            dinh_dang = "txt"  # Mặc định là file text
            if xuat_file:
                dinh_dang_input = input("Chọn định dạng xuất file (txt/xml): ").lower()
                if dinh_dang_input in ["xml", "txt"]:
                    dinh_dang = dinh_dang_input
                else:
                    print("Định dạng không hợp lệ, sẽ xuất ra file text")
            
            # Thực hiện tìm kiếm
            tim_kiem_noi_dung(duong_dan_file, tu_khoa_list, True, xuat_file, dinh_dang)
        
        print("\n----------------------------------------")

if __name__ == "__main__":
    main()

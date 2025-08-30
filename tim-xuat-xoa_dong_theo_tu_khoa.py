import xml.etree.ElementTree as ET
import os  # Import thư viện os để làm việc với đường dẫn

# Hàm pretty print XML
def indent(elem, level=0):
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

print("\n--- THÔNG TIN ỨNG DỤNG ---")
print("Tên: Ứng dụng lọc dòng XML theo từ khóa")
print("Mô tả: Ứng dụng này giúp bạn lọc, xuất, và xóa các dòng trong file XML chứa một từ khóa nhất định.")
print("---")

# Nhập từ khóa
keyword = input("Nhập từ khóa cần lọc (ví dụ Portrait): ").strip()
if not keyword:
    print("⚠️ Bạn chưa nhập từ khóa!")
    exit()

# Nhập đường dẫn file XML
file_path = input("Nhập đường dẫn file XML cần xử lý: ").strip()
if not file_path:
    print("⚠️ Bạn chưa nhập đường dẫn file!")
    exit()

try:
    tree = ET.parse(file_path)
except Exception as e:
    print(f"❌ Lỗi khi đọc file: {e}")
    exit()

root = tree.getroot()

# Tạo root mới cho file kết quả
result_root = ET.Element("contentList")

# Lọc các content chứa từ khóa
count = 0
for content in root.findall("content"):
    text = content.text or ""
    if keyword.lower() in text.lower():
        new_content = ET.Element("content", content.attrib)
        new_content.text = text
        result_root.append(new_content)
        count += 1

if count == 0:
    print(f"⚠️ Không tìm thấy dòng nào chứa từ khóa '{keyword}'")
else:
    # Tạo thư mục output nếu nó không tồn tại
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tên file theo từ khóa viết thường, đặt trong thư mục output
    output_file = os.path.join(output_dir, f"{keyword.lower()}.xml")

    # Format đẹp
    indent(result_root)

    # Ghi ra file mới
    ET.ElementTree(result_root).write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"✅ Hoàn thành! Đã tạo {output_file} với {count} dòng chứa từ khóa '{keyword}'")

    # Hỏi người dùng có muốn xóa các dòng đã lọc trong file gốc không
    xoa_file = input("Bạn có muốn xóa các dòng đã lọc trong file gốc (y/n)? ").strip().lower()
    if xoa_file == "y":
        # Tạo root mới chứa các content không chứa từ khóa
        new_root = ET.Element("contentList")
        for content in root.findall("content"):
            text = content.text or ""
            if keyword.lower() not in text.lower():
                new_content = ET.Element("content", content.attrib)
                new_content.text = text
                new_root.append(new_content)
        
        # Format đẹp
        indent(new_root)
        
        # Ghi lại vào file gốc
        ET.ElementTree(new_root).write(file_path, encoding="utf-8", xml_declaration=True)
        print(f"✅ Đã xóa các dòng chứa từ khóa '{keyword}' trong file gốc.")
    else:
        print("❌ Không xóa dòng nào trong file gốc.")

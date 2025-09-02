import xml.etree.ElementTree as ET
import os

# Hàm format XML đẹp (pretty print)
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

# Nhập đường dẫn file từ bàn phím
file_a = input("👉 Nhập đường dẫn file A (nguồn): ").strip()
file_b = input("👉 Nhập đường dẫn file B (đích): ").strip()

# Đọc file
try:
    tree_a = ET.parse(file_a)
    tree_b = ET.parse(file_b)
except Exception as e:
    print(f"❌ Lỗi khi đọc file: {e}")
    exit()

root_a = tree_a.getroot()
root_b = tree_b.getroot()

# Tạo map contentuid cho file B
b_dict = {c.attrib["contentuid"]: c for c in root_b.findall("content")}

update_count = 0
add_count = 0

# Duyệt qua các content trong file A
for a_content in root_a.findall("content"):
    uid = a_content.attrib["contentuid"]
    text = a_content.text if a_content.text else ""

    if uid in b_dict:
        # Nếu đã có trong B → cập nhật text
        b_dict[uid].text = text
        update_count += 1
    else:
        # Nếu chưa có → thêm vào B (giữ nguyên version của A)
        new_content = ET.Element("content", {
            "contentuid": uid,
            "version": a_content.attrib.get("version", "0")
        })
        new_content.text = text
        root_b.append(new_content)
        add_count += 1

# Format XML đẹp
indent(root_b)

# Xuất ra file mới để an toàn
output_file = os.path.splitext(file_b)[0] + "_merged.xml"
tree_b.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"✅ Hoàn thành!")
print(f"   - Đã cập nhật {update_count} dòng.")
print(f"   - Đã thêm mới {add_count} dòng.")
print(f"   - File kết quả: {output_file}")

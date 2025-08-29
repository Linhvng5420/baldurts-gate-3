import xml.etree.ElementTree as ET

# Hàm thụt lề (pretty print)
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

# Đọc file eng.xml và vie.xml
tree_eng = ET.parse("eng.xml")
tree_vie = ET.parse("vie.xml")

root_eng = tree_eng.getroot()
root_vie = tree_vie.getroot()

# Tạo map từ vie.xml (dựa vào contentuid)
vie_dict = {c.attrib["contentuid"]: c for c in root_vie.findall("content")}

# Tạo root mới cho vh.xml
vh_root = ET.Element("contentList")

# Tạo root mới cho vh-eng.xml
vh_eng_root = ET.Element("contentList")

for eng_content in root_eng.findall("content"):
    uid = eng_content.attrib["contentuid"]
    
    if uid in vie_dict:
        # Nếu có trong vie thì lấy nội dung vie + sửa version=50
        vie_content = vie_dict[uid]
        new_content = ET.Element("content", {
            "contentuid": uid,
            "version": "50"
        })
        new_content.text = vie_content.text
        vh_root.append(new_content)
    else:
        # Nếu chỉ có trong eng thì ghi vào vh-eng.xml
        new_content = ET.Element("content", {
            "contentuid": uid,
            "version": eng_content.attrib["version"]
        })
        new_content.text = eng_content.text
        vh_eng_root.append(new_content)

# Gọi indent để format đẹp
indent(vh_root)
indent(vh_eng_root)

# Xuất ra file vh.xml
vh_tree = ET.ElementTree(vh_root)
vh_tree.write("vh.xml", encoding="utf-8", xml_declaration=True)

# Xuất ra file vh-eng.xml
vh_eng_tree = ET.ElementTree(vh_eng_root)
vh_eng_tree.write("vh-eng.xml", encoding="utf-8", xml_declaration=True)

# Thông báo khi hoàn thành
print("✅ Hoàn thành! Đã tạo ra 2 file: vh.xml và vh-eng.xml (có định dạng đẹp).")

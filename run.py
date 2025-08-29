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

# Dùng dict nhưng KHÔNG bỏ qua trùng lặp (chỉ để tra nhanh)
vie_dict = {}
for c in root_vie.findall("content"):
    uid = c.attrib["contentuid"]
    if uid not in vie_dict:   # chỉ lấy lần đầu tiên
        vie_dict[uid] = c

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
        new_content.text = vie_content.text if vie_content.text else ""
        vh_root.append(new_content)
    else:
        # Nếu chỉ có trong eng thì ghi vào vh-eng.xml
        new_content = ET.Element("content", {
            "contentuid": uid,
            "version": eng_content.attrib["version"]
        })
        new_content.text = eng_content.text if eng_content.text else ""
        vh_eng_root.append(new_content)

# Format XML đẹp
indent(vh_root)
indent(vh_eng_root)

# Xuất ra file
ET.ElementTree(vh_root).write("vh.xml", encoding="utf-8", xml_declaration=True)
ET.ElementTree(vh_eng_root).write("vh-eng.xml", encoding="utf-8", xml_declaration=True)

print("✅ Hoàn thành! Đã tạo vh.xml và vh-eng.xml (không bị mất dòng).")

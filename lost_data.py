import xml.etree.ElementTree as ET

# Hàm pretty print
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

# Đọc file eng.xml và vh.xml
tree_eng = ET.parse("eng.xml")
tree_vh = ET.parse("vh_merge.xml")

root_eng = tree_eng.getroot()
root_vh = tree_vh.getroot()

# Lấy danh sách contentuid trong vh.xml
vh_uids = {c.attrib["contentuid"] for c in root_vh.findall("content")}

# Root mới cho lost-eng.xml
lost_root = ET.Element("contentList")

# Kiểm tra contentuid nào có trong eng mà không có trong vh
for eng_content in root_eng.findall("content"):
    uid = eng_content.attrib["contentuid"]
    if uid not in vh_uids:
        # Giữ nguyên nội dung từ eng
        new_content = ET.Element("content", {
            "contentuid": uid,
            "version": eng_content.attrib["version"]
        })
        new_content.text = eng_content.text if eng_content.text else ""
        lost_root.append(new_content)

# Format đẹp
indent(lost_root)

# Ghi ra file lost-eng.xml
ET.ElementTree(lost_root).write("lost-eng.xml", encoding="utf-8", xml_declaration=True)

print("✅ Hoàn thành! Đã tạo file lost-eng.xml (chứa các dòng bị mất sau khi tách).")

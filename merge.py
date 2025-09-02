import re

# Nhập đường dẫn file
file_a = r"D:\Games\Baldurt's Gate VH\baldurts-gate-3\output\filtered\CutCanhTem50k_20250902_1200\workkeys_extracted_Vietnamese_20250902_094615_20250902_133600.xml"
file_b = r"D:\Games\Baldurt's Gate VH\baldurts-gate-3\output\filtered\vietnamese_VH.xml"

# Đọc file gốc
with open(file_a, "r", encoding="utf-8") as f:
    content_a = f.read()

with open(file_b, "r", encoding="utf-8") as f:
    content_b = f.read()

# Regex bắt <content ...> ... </content> (nhiều dòng)
pattern = re.compile(r'<content\s+contentuid="([^"]+)"[^>]*>.*?</content>', re.DOTALL)

# Tạo dict từ file B
b_dict = {m.group(1): m.group(0) for m in pattern.finditer(content_b)}

# Lưu contentuid trong A
a_uids = set()
output_parts = []
last_end = 0
update_count, add_count = 0, 0

# Duyệt qua từng block trong A
for m in pattern.finditer(content_a):
    uid = m.group(1)
    a_uids.add(uid)
    block = m.group(0)

    # Nếu có trong B → thay
    if uid in b_dict:
        if block != b_dict[uid]:
            block = b_dict[uid]
            update_count += 1
    output_parts.append(content_a[last_end:m.start()])
    output_parts.append(block)
    last_end = m.end()

# Thêm phần còn lại (sau content cuối cùng)
output_parts.append(content_a[last_end:])

# Thêm mới ở cuối file
new_uids = [uid for uid in b_dict if uid not in a_uids]
if new_uids:
    # Thêm comment trước
    output_parts.append("\n\t<!-- Thêm Việt Hóa Mới -->\n")
    for uid in new_uids:
        # Thêm tab thụt vào
        new_block = "\t" + b_dict[uid].replace("\n", "\n\t") + "\n"
        output_parts.append(new_block)
        add_count += 1

# Ghi đè file A
with open(file_a, "w", encoding="utf-8") as f:
    f.write("".join(output_parts))

print(f"✅ Hoàn thành update trực tiếp trong file A.")
print(f"   - Đã cập nhật {update_count} dòng.")
print(f"   - Đã thêm mới {add_count} dòng (có tab + comment).")
print(f"   - File kết quả: {file_a}")

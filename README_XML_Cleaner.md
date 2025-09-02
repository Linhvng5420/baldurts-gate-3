# XML Cleaner - Công cụ làm sạch file XML

Hai script Python để xóa comment và dòng trống trong file XML mà không thay đổi format và cấu trúc XML.

## Tổng quan

- **`xml_cleaner.py`**: Phiên bản cơ bản, dễ sử dụng
- **`xml_cleaner_advanced.py`**: Phiên bản nâng cao với nhiều tùy chọn

## xml_cleaner.py (Phiên bản cơ bản)

### Sử dụng

```bash
# Làm sạch file đơn lẻ (ghi đè file gốc)
python xml_cleaner.py file.xml

# Làm sạch file đơn lẻ (lưu file mới)
python xml_cleaner.py file.xml file_clean.xml

# Làm sạch tất cả file XML trong thư mục (ghi đè)
python xml_cleaner.py --batch ./data/

# Làm sạch tất cả file XML trong thư mục (lưu vào thư mục khác)
python xml_cleaner.py --batch ./input/ ./output/
```

### Tính năng

- ✅ Xóa comment XML (`<!-- -->`)
- ✅ Xóa dòng trống
- ✅ Giữ nguyên format và indentation XML
- ✅ Xử lý batch nhiều file
- ✅ Thống kê chi tiết

## xml_cleaner_advanced.py (Phiên bản nâng cao)

### Sử dụng

```bash
# Cơ bản
python xml_cleaner_advanced.py file.xml
python xml_cleaner_advanced.py file.xml -o cleaned.xml

# Xử lý thư mục
python xml_cleaner_advanced.py -d ./input/ -o ./output/
python xml_cleaner_advanced.py -d ./data/ --recursive

# Tùy chọn nâng cao
python xml_cleaner_advanced.py file.xml --no-comments     # Không xóa comment
python xml_cleaner_advanced.py file.xml --no-empty-lines  # Không xóa dòng trống  
python xml_cleaner_advanced.py file.xml --no-backup       # Không tạo backup
python xml_cleaner_advanced.py -d ./data/ -r -p "*.xml"   # Đệ quy với pattern
```

### Tính năng

- ✅ Tất cả tính năng của phiên bản cơ bản
- ✅ **Backup tự động** file gốc
- ✅ **Tùy chọn linh hoạt** (có thể tắt bất kỳ tính năng nào)
- ✅ **Xử lý đệ quy** thư mục con
- ✅ **Pattern matching** tùy chỉnh
- ✅ **Thống kê chi tiết** toàn diện
- ✅ **Command-line interface** hoàn chỉnh

### Tùy chọn

| Tùy chọn | Mô tả |
|----------|--------|
| `--no-comments` | Không xóa comment XML |
| `--no-empty-lines` | Không xóa dòng trống |
| `--no-backup` | Không tạo backup file gốc |
| `--no-indent` | Không giữ nguyên indentation (cẩn thận!) |
| `-r, --recursive` | Tìm kiếm đệ quy trong thư mục con |
| `-p, --pattern` | Pattern file để tìm (mặc định: *.xml) |

## Ví dụ thực tế

### Làm sạch file hiện tại
```bash
# Phiên bản cơ bản
python xml_cleaner.py "output\\filtered\\CutCanhTem50k_20250902_1200\\English_no-cmt.xml"

# Phiên bản nâng cao với backup
python xml_cleaner_advanced.py "output\\filtered\\CutCanhTem50k_20250902_1200\\English_no-cmt.xml" -o cleaned.xml
```

### Xử lý toàn bộ thư mục dự án
```bash
# Làm sạch tất cả file XML trong dự án
python xml_cleaner_advanced.py -d . --recursive --no-backup
```

### Chỉ xóa comment, giữ dòng trống
```bash
python xml_cleaner_advanced.py file.xml --no-empty-lines
```

## Kết quả

Script sẽ hiển thị thống kê chi tiết:

```
🎉 TỔNG KẾT
============================================================
📁 File đã xử lý: 1
✅ File thành công: 1  
❌ File lỗi: 0
💬 Tổng comment đã xóa: 39
📄 Tổng dòng trống đã xóa: 319
🗑️ Tổng dòng đã xóa: 358
```

## Lưu ý quan trọng

- ⚠️ **Luôn backup file quan trọng** trước khi xử lý
- ✅ Script **giữ nguyên encoding UTF-8** và format XML
- ✅ **Không thay đổi cấu trúc** hay nội dung XML
- ✅ **An toàn** với file lớn (đã test với file 233k+ dòng)

## Yêu cầu hệ thống

- Python 3.6+
- Các thư viện chuẩn: `re`, `os`, `sys`, `pathlib`, `datetime`, `argparse`

## Tác giả

Tạo bởi GitHub Copilot cho dự án Việt hóa Baldur's Gate 3.

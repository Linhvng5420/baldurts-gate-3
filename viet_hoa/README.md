# 🇻🇳 Việt Hóa Directory - File Việt hóa có sẵn

Thư mục chứa các file Việt hóa từ nhiều nguồn khác nhau để tham khảo và sử dụng.

## 📄 Danh sách file

| File | Nguồn | Mô tả | Trạng thái |
|------|-------|-------|------------|
| `eng_update_path8_version_4.116897358.xml` | 🎮 Game Update | English gốc từ BG3 Path8 | ✅ Reference |
| `english .xml` | 🎮 Game Base | English file gốc khác | ✅ Reference |
| `vh_anonymous_path3.xml` | 👤 Anonymous | Bản VH từ contributor ẩn danh | 🔄 Path3 |
| `vh_code_keywork.xml` | 🔑 Keywords | Từ khóa code và keywords VH | 📝 Dictionary |
| `vh_ngvlinhfb_path8.xml` | 👨‍💻 NgVLinhFB | Bản VH từ NgVLinhFB | 🔄 Path8 |

## 🎯 Cách sử dụng

### 1. Tham khảo bản dịch
```bash
# So sánh cách dịch giữa các nguồn
# Tìm contentuid giống nhau để học cách dịch
grep "contentuid=\"h123456789\"" *.xml
```

### 2. Gộp nhiều bản dịch
```bash
# Sử dụng XML Manager để gộp
# File Reference: eng_update_path8_version_4.116897358.xml
# File Merge: vh_*.xml
```

### 3. Làm từ điển
```bash
# vh_code_keywork.xml chứa từ khóa chuyên ngành
# Dùng để tra cứu thuật ngữ game
```

## 📊 Thống kê nhanh

### Path Version Coverage:
- **Path3**: `vh_anonymous_path3.xml`
- **Path8**: `vh_ngvlinhfb_path8.xml`, `eng_update_path8_version_4.116897358.xml`

### Loại nội dung:
- **Game Update**: Nội dung mới nhất từ game
- **Community Translation**: Bản dịch từ cộng đồng
- **Keywords Dictionary**: Từ điển thuật ngữ

## 🔍 Kiểm tra chất lượng

### Sử dụng Enhanced Filter để phân tích:
```bash
# Phân tích file VH
python src/bg3_filter_enhanced.py viet_hoa/vh_ngvlinhfb_path8.xml --analyze-only

# So sánh với English gốc
python src/bg3_filter_enhanced.py viet_hoa/eng_update_path8_version_4.116897358.xml --analyze-only
```

### Tìm kiếm nội dung cụ thể:
```bash
# Tìm tên nhân vật
grep -i "astarion\|shadowheart\|gale" *.xml

# Tìm UI elements  
grep -i "menu\|button\|dialog" *.xml
```

## ⚙️ Gộp file thông minh

### Workflow khuyến nghị:
1. **Base file**: `eng_update_path8_version_4.116897358.xml`
2. **Merge with**: `vh_ngvlinhfb_path8.xml` (cùng Path version)
3. **Reference**: `vh_code_keywork.xml` cho thuật ngữ
4. **Alternative**: `vh_anonymous_path3.xml` cho những phần còn thiếu

### Sử dụng XML Manager:
```
🔄 Tab: Gộp File XML
├── File Bị Kiểm Tra: eng_update_path8_version_4.116897358.xml
├── File Lấy Mẫu KT: vh_ngvlinhfb_path8.xml  
├── Content Version: 50 (hoặc tùy chọn)
└── 🚀 Bắt Đầu Gộp
```

## 📋 Notes quan trọng

### Version Management:
- **Version 1**: English gốc từ game
- **Version 50**: Bản Việt hóa mặc định
- **Version tùy chỉnh**: Cho team/contributor riêng

### Encoding:
- Tất cả file đều UTF-8
- Hỗ trợ ký tự đặc biệt Việt Nam
- Tương thích với BG3 engine

### Conflicts:
- Khi gộp có thể xảy ra xung đột
- Ưu tiên bản dịch mới hơn
- Kiểm tra trong `output/conflict/`

## 🔗 Workflow với project

### Input cho processing:
1. Copy file cần thiết vào `data/input/`
2. Sử dụng như base file cho merge/filter

### Reference cho translation:
1. Mở file để tra cứu cách dịch
2. Copy term đã dịch cho consistency

### Quality assurance:
1. So sánh kết quả với file reference
2. Đảm bảo không mất nội dung quan trọng

## ⚠️ Lưu ý

- **Chỉ đọc**: Không chỉnh sửa trực tiếp file trong thư mục này
- **Copyright**: Tôn trọng bản quyền của các contributor
- **Credit**: Ghi nhận nguồn khi sử dụng
- **Backup**: Giữ nguyên file gốc cho tham khảo

## 🆕 Cập nhật

Khi có file VH mới:
1. Đặt file vào thư mục này
2. Cập nhật README với thông tin file
3. Test compatibility với tools hiện tại
4. Chia sẻ với community nếu chất lượng tốt

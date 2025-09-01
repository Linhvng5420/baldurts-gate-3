# 💾 Data Directory - Quản lý dữ liệu BG3

Thư mục chính chứa tất cả dữ liệu XML cho project Việt hóa BG3.

## 📂 Cấu trúc thư mục

### 📥 `input/` - File đầu vào
```
input/
├── sample_english.xml     # 📄 File mẫu để test các tính năng
├── eng.xml               # 🇬🇧 File English gốc từ game (đặt ở đây)
├── vie.xml               # 🇻🇳 File Việt hóa đã dịch (đặt ở đây)
└── README.md             # 📖 Hướng dẫn sử dụng input
```

**Mục đích**: Chứa file XML đầu vào để xử lý
**Sử dụng**: Đặt file cần xử lý vào đây trước khi chạy tools

### 📤 `filtered/` - Kết quả filter cũ (Legacy)
```
filtered/
├── README.md             # 📖 Hướng dẫn về filter output
└── [các file kết quả]    # 📄 File được tạo bởi filter cũ
```

**Mục đích**: Lưu kết quả từ hệ thống filter cũ
**Trạng thái**: Legacy - Khuyến nghị dùng Enhanced Filter

### 🚧 `wip/` - Work in Progress
```
wip/
├── Package English Path8_4.116897358/     # 🎮 Game BG3 gốc version Path8
│   ├── english.xml                        # 📄 File XML đã convert
│   └── Localization/                      # 📁 File .loca gốc
├── Package English VH AI Path3/           # 🤖 Bản Việt hóa AI
├── Package English VH CutCanhTem Path8/   # ✂️ Bản VH CutCanhTem  
└── Package Nén Mod Việt Hóa/             # 📦 Package mod đóng gói
```

**Mục đích**: Chứa các file đang xử lý, các version khác nhau
**Sử dụng**: Làm việc với nhiều version cùng lúc

## 🎯 Workflow sử dụng

### 1. Chuẩn bị file input
```bash
# Copy file cần xử lý vào input/
cp /path/to/english.xml data/input/eng.xml
cp /path/to/vietnamese.xml data/input/vie.xml
```

### 2. Sử dụng Enhanced Filter
```bash
# File sẽ được xử lý từ input/ và xuất ra output/filtered/
python src/bg3_filter_enhanced_gui.py
```

### 3. Sử dụng XML Manager
```bash
# Gộp file từ input/ 
python src/bg3_xml_manager.py
```

## ⚠️ Lưu ý quan trọng

- **Không** commit file XML lớn vào Git (đã có .gitignore)
- File trong `wip/` là để reference, không chỉnh sửa trực tiếp
- Backup file quan trọng trước khi xử lý
- Sử dụng `sample_english.xml` để test tính năng mới

## 📋 Checklist trước khi xử lý

- [ ] Đã backup file gốc
- [ ] File XML hợp lệ (có thể mở bằng text editor)
- [ ] Đặt đúng vị trí trong thư mục tương ứng
- [ ] Chọn đúng tool cho mục đích sử dụng

## 🔗 Liên quan

- **Output**: Kết quả được lưu trong `output/`
- **Tools**: Sử dụng các tool trong `src/`
- **Config**: Cấu hình trong các file `.json`

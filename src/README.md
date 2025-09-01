# 💻 BG3 XML Manager - Source Code

Thư mục chứa mã nguồn chính của project BG3 XML Manager & Enhanced Filter.

## 📂 Cấu trúc file

### 🖥️ Ứng dụng chính

| File | Mô tả | Trạng thái |
|------|--------|------------|
| `bg3_filter_enhanced_gui.py` | 🖼️ GUI cho Enhanced Filter - **Khuyến nghị sử dụng** | ✅ Hoàn thiện |
| `bg3_filter_enhanced.py` | ⚡ Engine xử lý filter nâng cao - Core logic | ✅ Hoàn thiện |
| `bg3_xml_manager.py` | 🔧 XML Manager GUI - Gộp, tìm kiếm, kiểm tra | ✅ Hoàn thiện |

### 🛠️ Tiện ích

| File | Mô tả | Sử dụng |
|------|--------|---------|
| `setup.py` | 🛠️ Thiết lập cấu trúc project | Tự động |
| `system_check.py` | 🔍 Kiểm tra yêu cầu hệ thống | Tự động |
| `create_sample_data.py` | 📊 Tạo dữ liệu mẫu để test | Phát triển |

### ⚙️ Cấu hình

| File | Mô tả | Format |
|------|--------|--------|
| `filter_config.json` | ⚙️ Cấu hình Enhanced Filter | JSON |
| `config.json` | 📋 Cấu hình XML Manager | JSON |
| `project_info.json` | ℹ️ Thông tin project | JSON |

### 📜 File tự sinh

| Pattern | Mô tả | Quản lý |
|---------|-------|---------|
| `*.log` | 📝 Log files từ các ứng dụng | Tự động |
| `*_analysis.json` | 📈 Kết quả phân tích XML | Tự động |

## 🚀 Cách sử dụng

### 1. Cho người dùng cuối:
```bash
# Sử dụng GUI Enhanced Filter (Khuyến nghị)
python bg3_filter_enhanced_gui.py

# Hoặc XML Manager cổ điển
python bg3_xml_manager.py
```

### 2. Cho developer:
```bash
# Command line Enhanced Filter
python bg3_filter_enhanced.py input.xml --ui-text

# Kiểm tra hệ thống
python system_check.py

# Thiết lập project
python setup.py setup
```

## 📖 Tài liệu chi tiết

- **Enhanced Filter**: Xem hướng dẫn trong GUI application
- **XML Manager**: Xem README chính của project
- **Cấu hình**: Chỉnh sửa file JSON tương ứng

## ⚠️ Lưu ý

- File `*.log` và `*_analysis.json` được tạo tự động
- Không chỉnh sửa trực tiếp file config khi ứng dụng đang chạy
- Backup config trước khi thay đổi cài đặt quan trọng

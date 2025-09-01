LƯU Ý: PHẢI MỞ VÀ XEM HƯỚNG DẪN TRÊN GITHUB CHROME, WINDOWS KHÔNG HỖ TRỢ XEM MÃ MARKDOWN

# Baldur's Gate 3 XML Manager & Enhanced Filter v2.0

Bộ công cụ quản lý và xử lý file XML cho dự án Việt hóa Baldur's Gate 3.

## 🚀 Công cụ chính

### 1. BG3 Enhanced Filter GUI (`bg3_filter_enhanced_gui.py`) 🆕✨
- **Giao diện đồ họa trực quan** với hướng dẫn chi tiết
- **Ví dụ thực tế** cho từng tính năng filter
- **Xem trước kết quả** trước khi lọc
- **Theo dõi tiến độ** realtime với progress bar
- **Quản lý cài đặt** dễ dàng qua GUI
- **Log viewer** tích hợp để debug

### 2. BG3 Enhanced Filter (`bg3_filter_enhanced.py`)
- **UI Text Filter**: Tách giao diện người dùng
- **English Filter**: Lọc/loại bỏ text tiếng Anh
- **Dialogue Filter**: Tách đối thoại trong game
- **Technical Filter**: Lọc text kỹ thuật
- **Context Filter**: Phân loại theo nội dung
- **Analysis Mode**: Phân tích file mà không tạo output

### 3. BG3 XML Manager (`bg3_xml_manager.py`)
- Gộp file XML localization
- Tìm kiếm và kiểm tra dữ liệu
- Thống kê và phân tích
- Quản lý cấu hình

## 🎯 Quick Start

### 🚀 Chạy ứng dụng chính (Khuyến nghị):
```batch
# 1. Thiết lập lần đầu (chỉ chạy 1 lần)
setup_first_time.bat

# 2. Enhanced Filter GUI - Khuyến nghị cho người mới  
python src/bg3_filter_enhanced_gui.py

# 3. XML Manager cổ điển - Gộp, tìm kiếm, kiểm tra
run_bg3_manager.bat
```

### 📁 Hoặc sử dụng Batch Files:
```batch
# Enhanced Filter Tool (Command line với menu)
run_bg3_enhanced_filter.bat

# XML Manager (GUI application)  
run_bg3_manager.bat

# Thiết lập project lần đầu
setup_first_time.bat

# Mở VS Code để chỉnh sửa
"Open VS Code.cmd"
```

### 💻 Command Line cho Developer:
```bash
# Lọc UI text
python src/bg3_filter_enhanced.py input.xml --ui-text

# Lọc tất cả loại
python src/bg3_filter_enhanced.py input.xml --all

# Chỉ phân tích (không tạo file output)
python src/bg3_filter_enhanced.py input.xml --analyze-only

# Kiểm tra hệ thống
python src/system_check.py

# Thiết lập project
python src/setup.py setup
```

## 📁 Cấu trúc thư mục

```
baldurts-gate-3/
├── src/                           # 💻 Source Code - Mã nguồn chính
│   ├── bg3_filter_enhanced_gui.py # 🖥️  GUI cho Enhanced Filter (Khuyến nghị)
│   ├── bg3_filter_enhanced.py     # ⚡ Enhanced Filter Engine - Bộ lọc nâng cao
│   ├── bg3_xml_manager.py         # 🔧 XML Manager GUI - Quản lý XML cơ bản  
│   ├── create_sample_data.py      # 📊 Tạo dữ liệu mẫu cho test
│   ├── filter_config.json         # ⚙️  Cấu hình filter nâng cao
│   ├── setup.py                   # 🛠️  Thiết lập project
│   ├── system_check.py            # 🔍 Kiểm tra hệ thống
│   ├── config.json                # 📋 Cấu hình XML Manager
│   ├── project_info.json          # ℹ️  Thông tin project
│   ├── *.log                      # 📜 Log files (tự sinh)
│   └── *_analysis.json            # 📈 Kết quả phân tích (tự sinh)
│
├── data/                          # 💾 Xử lý dữ liệu
│   ├── input/                     # 📥 File XML đầu vào
│   │   ├── sample_english.xml     # 📄 File mẫu để test
│   │   └── README.md              # 📖 Hướng dẫn input
│   ├── filtered/                  # 📤 Kết quả filter cũ (legacy)
│   └── wip/                       # 🚧 Work in progress - File đang xử lý
│       ├── Package English Path8_4.116897358/  # 🎮 Game BG3 gốc
│       ├── Package English VH AI Path3/        # 🤖 Bản VH AI
│       ├── Package English VH CutCanhTem Path8/ # ✂️ Bản VH CutCanhTem
│       └── Package Nén Mod Việt Hóa/           # 📦 Mod VH đóng gói
│
├── output/                        # 📂 Thư mục đầu ra
│   ├── conflict/                  # ⚠️  Xử lý xung đột
│   └── filtered/                  # 📋 Enhanced filter output 🆕
│       └── [filename]/            # 📁 Phân loại theo file nguồn
│           ├── ui_text.xml        # 🖼️  Text giao diện
│           ├── english_only.xml   # 🇬🇧 Text chỉ tiếng Anh
│           ├── dialogue.xml       # 💬 Đối thoại
│           ├── by_context/        # 🏷️  Phân loại theo context
│           └── filter_report.txt  # 📊 Báo cáo filter
│
├── tool/                          # 🛠️  Công cụ hỗ trợ
│   └── ExportTool-v1.19.5/        # 📦 ExportTool cho BG3
│       ├── ConverterApp.exe       # 🔄 Converter chính
│       └── Tools/                 # 🧰 Các tool khác
│
├── viet_hoa/                      # 🇻🇳 File Việt hóa có sẵn
│   ├── eng_update_path8_version_4.116897358.xml  # 📄 English update
│   ├── vh_anonymous_path3.xml     # 👤 VH Anonymous
│   ├── vh_code_keywork.xml        # 🔑 VH Code Keywords
│   └── vh_ngvlinhfb_path8.xml     # 👨‍💻 VH NgVLinhFB
│
├── 🚀 run_bg3_manager.bat         # ▶️  Chạy XML Manager (Chính)
├── ⚡ run_bg3_enhanced_filter.bat # ▶️  Chạy Enhanced Filter
├── 🛠️  setup_first_time.bat       # 🎯 Thiết lập lần đầu
├── 💻 Open VS Code.cmd            # 🔧 Mở VS Code để edit
├── 🔗 Open ConverterApp.exe.lnk   # 📦 Shortcut ExportTool
├── 📖 README.md                   # 📋 Hướng dẫn chính (file này)
├── 📖 README Hướng Dẫn Việt Hóa Game BG3.md  # 🎮 Hướng dẫn VH game
└── 🚫 .gitignore                  # 📝 Git ignore rules
```
├── data/                        # Data processing
│   ├── input/                   # Input files
│   ├── filtered/               # Legacy filter output
│   └── wip/                    # Work in progress
│
├── output/                     # Output directory
│   ├── conflict/              # Conflict resolution
│   └── filtered/              # Enhanced filter output 🆕
│       └── [filename]/        # Organized by source file
│           ├── ui_text.xml    # UI text
│           ├── english_only.xml
│           ├── dialogue.xml
│           ├── by_context/    # Context-based filtering
│           └── filter_report.txt
│
├── docs/                      # Documentation
│   └── BG3_Enhanced_Filter_Guide.md 🆕
│
├── 🚀 setup_first_time.bat        # 🎯 Thiết lập project lần đầu (CHẠY ĐẦU TIÊN)
├── ▶️  run_bg3_manager.bat         # 🔧 XML Manager - Gộp, tìm kiếm, kiểm tra  
├── ⚡ run_bg3_enhanced_filter.bat # 🔍 Enhanced Filter - Menu command line
├── 💻 Open VS Code.cmd            # 🛠️  Mở VS Code để chỉnh sửa code
├── 🔗 Open ConverterApp.exe.lnk   # 📦 Shortcut tới ExportTool
├── 📖 README.md                   # 📋 Hướng dẫn chính (file này)
├── 📖 README Hướng Dẫn Việt Hóa Game BG3.md  # 🎮 Hướng dẫn VH game cụ thể
└── 🚫 .gitignore                  # 📝 Git ignore rules
├── QUICK_START.md               # Hướng dẫn nhanh
└── PROJECT_STRUCTURE.md         # Cấu trúc dự án
```

## 🔧 Hướng dẫn chi tiết

# 🚀 Hướng Dẫn Nhanh - BG3 XML Manager v2.0

## 🏁 Bắt đầu ngay

### 1. Thiết lập lần đầu
```
Double-click: setup_first_time.bat
```

### 2. Chạy ứng dụng
```
Double-click: run_bg3_manager.bat
```

### 3. Chuẩn bị file để tiến hành Việt Hóa Game
- Đặt `English.xml` (file tiếng Anh gốc của Game) vào `data/input/`
- Đặt `English_VH.xml` (file tiếng Việt - Việt Hóa phiên bản cũ Nếu Có) vào `data/input/` (Tên gốc là `English.xml`, nhưng đã phải đặt lại tên tránh nhầm lẫn với file gốc)

## ⚡ Quy trình nhanh

### Gộp file XML:
1. **Tab "🔄 Gộp File XML"**
2. Chọn file ENG và VIE
3. Nhấn "🚀 Bắt Đầu Gộp File"
4. Kết quả trong thư mục `output/`

### Tìm kiếm:
1. **Tab "🔍 Tìm Kiếm & Lọc"**
2. Chọn file XML
3. Nhập từ khóa (cách nhau bằng dấu phẩy)
4. Nhấn "🔍 Tìm"

### Kiểm tra dữ liệu:
1. **Tab "🔍 Kiểm Tra Dữ Liệu"**
2. Chọn file gốc và file đã gộp
3. Nhấn "🔍 Kiểm Tra"

# Project Update Summary

## Hoàn thành: Tách và nâng cấp BG3 Filter Tool

### 📋 Công việc đã thực hiện:

#### 1. Tách filter khỏi BG3 XML Manager ✅
- Đã loại bỏ hoàn toàn filter functionality từ `bg3_xml_manager.py`
- Manager giờ chỉ tập trung vào merge, search, check và stats
- Thêm button link đến Enhanced Filter Tool trong Manager

#### 2. Tạo BG3 Enhanced Filter Tool mới ✅
**File**: `src/bg3_filter_enhanced.py`

**Tính năng nâng cao**:
- ✅ **UI Text Filter** - Tách giao diện người dùng (cải tiến từ tool cũ)
- ✅ **English Filter** - Lọc/loại bỏ text chỉ tiếng Anh
- ✅ **Non-English Filter** - Giữ lại text không phải tiếng Anh
- ✅ **Dialogue Filter** - Tách đối thoại trong game
- ✅ **Technical Filter** - Lọc text kỹ thuật, debug, system
- ✅ **Context Filter** - Phân loại theo nội dung (combat, inventory, menu, quest, character)
- ✅ **Analysis Mode** - Phân tích file không tạo output
- ✅ **Configurable** - File config JSON tùy chỉnh
- ✅ **Progress Tracking** - Hiển thị tiến độ cho file lớn
- ✅ **Multiple Output** - Tạo nhiều file output cùng lúc

#### 3. Tạo hệ thống hỗ trợ ✅
- ✅ **Config File**: `src/filter_config.json` - Cấu hình chi tiết
- ✅ **Batch File**: `run_bg3_enhanced_filter.bat` - Giao diện dễ sử dụng
- ✅ **Documentation**: `docs/BG3_Enhanced_Filter_Guide.md` - Hướng dẫn chi tiết
- ✅ **Logging**: Ghi log chi tiết quá trình xử lý

#### 4. Tối ưu hóa tool cũ ✅
- Tool cũ `bg3_filter_keywork.py` vẫn giữ lại, tập trung chỉ UI filter
- Đơn giản hóa và tối ưu hiệu suất

### 📊 Kết quả test thực tế:

**File test**: `data/wip/Package English Path8_4.116897358/english.xml`
- **Tổng entries**: 232,872
- **UI text tìm thấy**: 62,593 (26.9%)
- **English-only candidates**: 230,221 (98.9%)
- **Dialogue candidates**: 75,259 (32.3%)
- **Technical candidates**: 28,039 (12.0%)

**Context phân bố**:
- Combat: 15,847
- Menu: 20,751
- Inventory: 6,716
- Character: 5,446
- Quest: 6,730

**Hiệu suất**: Xử lý 232K entries trong ~15 giây

### 🚀 Cách sử dụng:

#### Command Line:
```bash
# Lọc UI text
python src/bg3_filter_enhanced.py input.xml --ui-text

# Lọc English-only
python src/bg3_filter_enhanced.py input.xml --english-only

# Lọc tất cả loại
python src/bg3_filter_enhanced.py input.xml --all

# Chỉ phân tích
python src/bg3_filter_enhanced.py input.xml --analyze-only
```

#### Batch File (Dễ dùng):
```bash
.\run_bg3_enhanced_filter.bat
```

### 📁 Output Structure:
```
output/filtered/
├── [filename]/
│   ├── ui_text.xml
│   ├── english_only.xml
│   ├── non_english.xml
│   ├── dialogue.xml
│   ├── technical.xml
│   ├── by_context/
│   │   ├── combat.xml
│   │   ├── inventory.xml
│   │   ├── menu.xml
│   │   ├── quest.xml
│   │   └── character.xml
│   └── filter_report.txt
```

### 🔧 Cấu hình có thể tùy chỉnh:
- **UI Filter**: Độ dài max, số keywords tối thiểu
- **English Filter**: Bảo toàn system markers
- **Dialogue Filter**: Độ dài min/max
- **Context Filter**: Các category muốn lọc
- **Output Settings**: Thư mục output, tạo subfolder

### ✨ Ưu điểm so với tool cũ:

1. **Đa dạng filter**: 6 loại filter khác nhau
2. **Hiệu suất cao**: Progress tracking, optimized processing
3. **Linh hoạt**: Config JSON, command line options
4. **Dễ sử dụng**: Batch file, help system
5. **Báo cáo chi tiết**: Statistics, samples, analysis
6. **Maintainable**: Clean code, modular design

---
*BG3 XML Manager v2.0 - Made with ❤️ for BG3 Vietnam Community*


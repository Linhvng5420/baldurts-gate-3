# Hướng Dẫn Việt Hóa Game Baldur's Gate 3

## 1. CHUẨN BỊ

Đảm bảo bạn đã hoàn thành các bước sau:

### 1.1. Thiết lập lần đầu
```bash
# Double-click file này để thiết lập ban đầu
setup_first_time.bat
```

### 1.2. Chạy ứng dụng BG3 Manager
```bash
# Double-click file này để khởi chạy BG3 Manager
run_bg3_manager.bat
```

### 1.3. Chuẩn bị các file cần thiết
- ✅ File `English.pak`, `english.loca`, `english.xml` gốc từ Update mới nhất của Game BG3
- ✅ File `english.xml` từ các bản việt hóa khác (nếu có)


## 2. TẠO CÁC FILE ENGLISH GỐC TỪ GAME BG3

> **Lưu ý:** Trong `data\wip\path8_version_4.116897358\Package English Game Gốc` đã có đủ các file cần thiết. Nếu game có bản update mới hơn `path8_version_4.116897358` thì bạn cần tạo các file mới theo hướng dẫn bên dưới.

### 2.1. Sử dụng ExportTool

Tool ExportTool có sẵn trong thư mục: `tool\ExportTool-v1.19.5`

### 2.2. Giải nén English.pak thành Folder

1. **Mở ExportTool và chọn tab `PAK / LSV Tools`**

2. **Trong khung `Extract Package`:**
   - **Package path:** Chọn file `English.pak` gốc từ Game BG3  
     📁 `SteamLibrary\steamapps\common\Baldurs Gate 3\Data\Localization\English.pak`
   - **Destination path:** Chọn thư mục `data/wip` và đặt tên là `Package English (Version Game)`
   - **Nhấn `Extract Package`**

3. **Tạo Folder chuẩn bị nén Mod:**
   - Copy folder vừa giải nén ở trên
   - Đổi tên thành `Package Nén Mod Việt Hóa` trong `data/wip`
   - ⚠️ **Quan trọng:** Xóa file `english.loca` đi (sẽ thay thế bằng file đã việt hóa sau này)

### 2.3. Cấu trúc thư mục sau khi giải nén

**`Package Location` (bản gốc):**
```
└── Localization/
    └── English/
        ├── english_M_to_X.loca
        ├── english_to_F.loca
        ├── english.loca
        ├── english.xml
        └── Gender/
            ├── Female/
            │   ├── english_F_to_X.loca
            │   ├── english_to_F.loca
            │   └── english.loca
            └── Neutral/
                ├── english_X_to_F.loca
                ├── english_X_to_M.loca
                └── english_X_to_X.loca
```

**`Package Nén Mod Việt Hóa` (không có `english.loca`):**
```
└── Localization/
    └── English/
        ├── english_M_to_X.loca
        ├── english_to_F.loca
        ├── english.xml
        └── Gender/
            ├── Female/
            │   ├── english_F_to_X.loca
            │   ├── english_to_F.loca
            │   └── english.loca
            └── Neutral/
                ├── english_X_to_F.loca
                ├── english_X_to_M.loca
                └── english_X_to_X.loca
```

### 2.4. Chuyển đổi english.loca thành english.xml

1. **Chọn tab `Localization` trong ExportTool**

2. **Thiết lập đường dẫn:**
   - **Input file path:** Chọn file `english.loca` vừa giải nén
   - **Output file path:** Chọn vị trí trong `Package Location`, đặt tên file là `english.xml`

3. **Nhấn `Convert`**

## 3. TIẾN HÀNH VIỆT HÓA

### 3.1. Phương pháp việt hóa

Cấu trúc Text trong BG3:
```xml
	<content contentuid="h000347eag76d8g47b6g9fe3g4f2162783f9d" version="1">That did the trick.</content>
```
   - Bản Việt Hóa mặc định là `version="50"`
   - Bản Việt Hóa của NGVLinhFB mặc định là `version="60"`
   - Bạn tự chọn Version cho mình để sau này chia sẻ cho Cộng Đồng không bị ghi đè.

Bạn có thể sử dụng một trong các phương pháp sau:

#### 📝 Việt hóa thủ công
- Sử dụng **NotePad++** hoặc **VS Code**
- Mở file `english.xml` và dịch từng dòng text

#### 🔧 Sử dụng BG3 Manager Tool
- **Gộp file VH cũ** vào file game update
- **Tách - Lọc - Xóa - So sánh** các đoạn text
- **Tìm code** và **phát hiện thiếu lời thoại**
- Tất cả đều được hỗ trợ sẵn trong `BG3 Manager Tool`

### 3.2. Các tính năng hỗ trợ
- ✅ Tách nội dung cần dịch
- ✅ Lọc và xóa các phần không cần thiết  
- ✅ So sánh với bản việt hóa cũ
- ✅ Tìm kiếm theo mã code
- ✅ Phát hiện lời thoại bị thiếu

## 4. TẠO MOD VIỆT HÓA

Sau khi hoàn thành việt hóa, bạn cần tạo file mod để cài đặt vào game.

### 4.1. Sử dụng ExportTool

Tool ExportTool có sẵn trong: `tool\ExportTool-v1.19.5`

### 4.2. Chuyển đổi english.xml thành english.loca

1. **Mở ExportTool và chọn tab `Localization`**

2. **Thiết lập đường dẫn:**
   - **Input file path:** Chọn file `english.xml` đã được việt hóa
   - **Output file path:** Chọn folder `Package Nén Mod Việt Hóa`, đặt tên file là `english.loca`

3. **Nhấn `Convert`**

### 4.3. Tạo file Mod Việt Hóa (.pak)

1. **Chọn tab `PAK / LSV Tools`**

2. **Trong khung `Create Package`:**
   - **Source path:** Chọn folder `Package Nén Mod Việt Hóa`
   - **Package path:** Chọn folder `data/wip` (nơi lưu file mod)
   - **Thiết lập:**
     - **Version:** `V18 (Baldur's Gate 3 Release)`
     - **Compression:** `LZ4 HC`

3. **Nhấn `Create Package`**

### 4.4. Cài đặt Mod vào Game

Copy file `.pak` vừa tạo vào thư mục `Localization` của BG3:
   ```
   SteamLibrary\steamapps\common\Baldurs Gate 3\Data\Localization\English.pak
   ```

---
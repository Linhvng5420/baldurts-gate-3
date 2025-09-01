# 🛠️ Tools Directory - Công cụ hỗ trợ

Thư mục chứa các công cụ bên ngoài cần thiết cho project BG3.

## 📦 ExportTool v1.19.5

**Nguồn**: LSLib - Công cụ chính thức cho Divinity và BG3
**Mục đích**: Convert giữa các format file của Larian Studios

### 🔧 Các công cụ chính

| Tool | File | Chức năng |
|------|------|-----------|
| **Converter** | `ConverterApp.exe` | 🔄 Convert PAK ↔ Folder, LOCA ↔ XML |
| **Divine** | `Tools/Divine.exe` | 📦 Command line converter |
| **Story Compiler** | `Tools/StoryCompiler.exe` | 📝 Compile story scripts |
| **Story Decompiler** | `Tools/StoryDecompiler.exe` | 📖 Decompile story scripts |

### ⚡ Cách sử dụng với BG3

#### 1. Giải nén English.pak từ game
```
ConverterApp.exe
→ TAB: PAK / LSV Tools  
→ Package path: [English.pak từ game]
→ Output path: [thư mục đích]
→ Extract Package
```

#### 2. Convert english.loca → english.xml
```  
ConverterApp.exe
→ TAB: Localization
→ Input file: english.loca
→ Output file: english.xml  
→ Convert
```

#### 3. Convert english.xml → english.loca (sau khi dịch)
```
ConverterApp.exe  
→ TAB: Localization
→ Input file: english.xml (đã dịch)
→ Output file: english.loca
→ Convert
```

#### 4. Đóng gói thành mod
```
ConverterApp.exe
→ TAB: PAK / LSV Tools
→ Source folder: [thư mục chứa Localization/]
→ Package path: [ModVietnamese.pak]
→ Create Package
```

## 🎯 Workflow chuẩn BG3

### Chuẩn bị file từ game:
1. **Extract game files** → `data/wip/Package English Path8_xxx/`
2. **Convert .loca to .xml** → Để xử lý với tools của chúng ta
3. **Xử lý với BG3 tools** → Filter, merge, translate

### Tạo mod sau khi dịch:
1. **Convert .xml to .loca** → Chuẩn bị cho game
2. **Package thành .pak** → Mod file cuối cùng  
3. **Test trong game** → Đảm bảo hoạt động

## ⚙️ Cấu hình quan trọng

### settings.json
```json
{
  "DefaultResourceFormat": "LSX",
  "EnableDiagnosticMode": false,
  "DebugInfoLevel": "None"
}
```

**Lưu ý**: Không cần chỉnh sửa settings thường xuyên

## 🔗 Shortcut

Đã tạo shortcut trong thư mục gốc:
- `Open ConverterApp.exe.lnk` → Mở ExportTool nhanh

## 📋 Dependencies

ExportTool cần các thư viện:
- ✅ `LSLib.dll` - Core library
- ✅ `Newtonsoft.Json.dll` - JSON processing  
- ✅ `granny2.dll` - 3D asset support
- ✅ `ZstdSharp.dll` - Compression

**Trạng thái**: Tất cả dependencies đã có sẵn ✅

## ⚠️ Lưu ý quan trọng

### Khi sử dụng ExportTool:
- 🔄 **Backup file gốc** trước khi convert
- 📁 **Đặt output ở thư mục riêng** để không bị lẫn
- 🎮 **Test mod trong game** sau khi đóng gói
- 💾 **Không commit các file .pak lớn** vào Git

### Troubleshooting:
- **ExportTool crash**: Kiểm tra file input có hợp lệ
- **Mod không hoạt động**: Đảm bảo cấu trúc folder đúng
- **Text bị lỗi font**: Kiểm tra encoding UTF-8

## 🔗 Tài liệu tham khảo

- **LSLib GitHub**: https://github.com/Norbyte/lslib
- **BG3 Modding Wiki**: Tìm hiểu thêm về modding BG3  
- **Larian Modding**: Tài liệu chính thức từ Larian

## 🆕 Phiên bản

**ExportTool v1.19.5**: Phiên bản ổn định cho BG3
- ✅ Hỗ trợ đầy đủ BG3 formats
- ✅ Convert .loca ↔ .xml hoàn hảo
- ✅ Package management tốt

@echo off
chcp 65001 >nul
title BG3 XML Manager - First Time Setup

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                🚀 THIẾT LẬP LẦN ĐẦU - FIRST TIME SETUP           ║
echo ║                    BG3 XML Manager Version 2.0                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Chào mừng bạn đến với BG3 XML Manager!
echo Chúng tôi sẽ thiết lập mọi thứ cần thiết cho bạn.
echo.

REM Kiểm tra Python
echo 🔍 BƯỚC 1: Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo.
    echo 📥 Vui lòng cài đặt Python trước:
    echo    1. Truy cập: https://www.python.org/downloads/
    echo    2. Tải phiên bản Python 3.6 trở lên
    echo    3. Khi cài đặt, nhớ tick "Add Python to PATH"
    echo    4. Chạy lại file này sau khi cài đặt
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python !PYTHON_VERSION! đã được cài đặt
)

REM Chạy kiểm tra yêu cầu hệ thống chi tiết
echo.
echo 🔧 BƯỚC 2: Kiểm tra yêu cầu hệ thống...
if exist "src\system_check.py" (
    python src\system_check.py --gui
    if errorlevel 1 (
        echo.
        echo ❌ Hệ thống chưa đáp ứng một số yêu cầu!
        echo 🔧 Vui lòng khắc phục các vấn đề được liệt kê ở trên.
        echo.
        set /p continue="Bạn có muốn tiếp tục thiết lập không? (y/N): "
        if /i not "!continue!"=="y" (
            echo Thoát thiết lập.
            pause
            exit /b 1
        )
    ) else (
        echo ✅ Hệ thống đáp ứng tất cả yêu cầu
    )
) else (
    echo ⚠️ File src\system_check.py không tồn tại, bỏ qua kiểm tra
)

REM Thiết lập cấu trúc dự án
echo.
echo 📁 BƯỚC 3: Thiết lập cấu trúc dự án...
if exist "src\setup.py" (
    python src\setup.py all
    echo ✅ Đã thiết lập cấu trúc dự án hoàn chỉnh
) else (
    echo 📁 Tạo thư mục cơ bản...
    if not exist "output" mkdir output
    if not exist "data\input" mkdir "data\input"
    if not exist "data\filtered" mkdir "data\filtered"
    if not exist "data\wip" mkdir "data\wip"
    echo ✅ Đã tạo các thư mục cơ bản
)

REM Kiểm tra file chính
echo.
echo 📄 BƯỚC 4: Kiểm tra file ứng dụng...
if exist "src\bg3_xml_manager.py" (
    echo ✅ File ứng dụng chính đã có sẵn
) else (
    echo ❌ Không tìm thấy file src\bg3_xml_manager.py!
    echo.
    echo 📥 Vui lòng đảm bảo các file sau tồn tại:
    echo    - src\bg3_xml_manager.py (file ứng dụng chính)
    echo    - run_bg3_manager.bat (file chạy nhanh)
    echo    - README.md (hướng dẫn sử dụng)
    echo.
    pause
    exit /b 1
)

REM Tạo shortcut
echo.
echo 🔗 BƯỚC 5: Tạo shortcut...
set /p create_shortcut="Bạn có muốn tạo shortcut trên Desktop? (Y/n): "
if /i not "!create_shortcut!"=="n" (
    powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\BG3 XML Manager.lnk'); $Shortcut.TargetPath = '%CD%\run_bg3_manager.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = '%CD%\run_bg3_manager.bat,0'; $Shortcut.Description = 'Baldur''s Gate 3 XML Manager'; $Shortcut.Save()}"
    if not errorlevel 1 (
        echo ✅ Đã tạo shortcut trên Desktop
    ) else (
        echo ⚠️ Không thể tạo shortcut (không sao)
    )
)

REM Hoàn thành
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                       🎉 THIẾT LẬP HOÀN TẤT!                     ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ✅ BG3 XML Manager đã sẵn sàng sử dụng!
echo.
echo 📖 Hướng dẫn nhanh:
echo    1. Đặt file XML gốc vào thư mục data/input/
echo       - eng.xml: File tiếng Anh từ game
echo       - vie.xml: File tiếng Việt đã dịch
echo.
echo    2. Chạy ứng dụng:
echo       - Double-click "run_bg3_manager.bat"
echo       - Hoặc shortcut trên Desktop (nếu đã tạo)
echo.
echo    3. Xem hướng dẫn chi tiết trong README.md
echo.
echo 🚀 Cách chạy ứng dụng:
echo    [1] Chạy ngay bây giờ
echo    [2] Mở thư mục dự án
echo    [3] Xem README.md
echo    [0] Thoát
echo.

:menu
set /p choice="Chọn tùy chọn (0-3): "

if "!choice!"=="1" (
    echo.
    echo 🚀 Đang khởi động BG3 XML Manager...
    call run_bg3_manager.bat
) else if "!choice!"=="2" (
    echo.
    echo 📁 Mở thư mục dự án...
    explorer .
) else if "!choice!"=="3" (
    echo.
    echo 📖 Mở README.md...
    if exist "README.md" (
        notepad README.md
    ) else (
        echo ❌ File README.md không tồn tại
    )
) else if "!choice!"=="0" (
    echo.
    echo 👋 Cảm ơn bạn đã sử dụng BG3 XML Manager!
    echo Chúc bạn Việt hóa thành công! 🎮🇻🇳
) else (
    echo ❌ Lựa chọn không hợp lệ. Vui lòng chọn 0-3.
    goto menu
)

echo.
pause

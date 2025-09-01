@echo off
chcp 65001 >nul
title Baldur's Gate 3 XML Manager

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    🎮 Baldur's Gate 3 XML Manager                ║
echo ║                           Version 2.0                           ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

REM Kiểm tra Python
echo 🔍 Kiểm tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo.
    echo Vui lòng cài đặt Python từ: https://www.python.org/downloads/
    echo Đảm bảo chọn "Add Python to PATH" khi cài đặt.
    echo.
    pause
    exit /b 1
)

REM Chạy kiểm tra yêu cầu hệ thống
if exist "src\system_check.py" (
    echo 🔧 Kiểm tra yêu cầu hệ thống...
    python src\system_check.py --no-gui --wait
    if errorlevel 1 (
        echo.
        echo ❌ Hệ thống chưa đáp ứng yêu cầu!
        echo Vui lòng khắc phục các vấn đề trước khi tiếp tục.
        echo.
        pause
        exit /b 1
    )
    echo ✅ Hệ thống đáp ứng yêu cầu
    echo.
)

REM Thiết lập cấu trúc dự án
if exist "src\setup.py" (
    echo 📁 Thiết lập cấu trúc dự án...
    python src\setup.py setup >nul 2>&1
    echo ✅ Đã kiểm tra cấu trúc dự án
    echo.
)

REM Kiểm tra file ứng dụng
if not exist "src\bg3_xml_manager.py" (
    echo ❌ File src\bg3_xml_manager.py không tồn tại!
    echo.
    echo Vui lòng đảm bảo file src\bg3_xml_manager.py nằm trong thư mục src.
    echo.
    pause
    exit /b 1
)

REM Chạy ứng dụng
echo 🚀 Đang khởi động Baldur's Gate 3 XML Manager...
echo.
python src\bg3_xml_manager.py

REM Kiểm tra lỗi
if errorlevel 1 (
    echo.
    echo ❌ Có lỗi xảy ra khi chạy ứng dụng!
    echo.
    echo Vui lòng kiểm tra:
    echo - Python đã được cài đặt đúng cách
    echo - File src\bg3_xml_manager.py không bị lỗi
    echo - Thư viện tkinter đã được cài đặt
    echo.
    pause
) else (
    echo.
    echo ✅ Ứng dụng đã đóng thành công
)

pause

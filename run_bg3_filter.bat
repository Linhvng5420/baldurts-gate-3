@echo off
chcp 65001 >nul
echo ================================
echo   BG3 Simplified Filter Tool
echo ================================
echo.
echo Chỉ giữ lại:
echo - UI Text Filter + Technical Filter
echo - English Filter
echo.
echo Kết quả xuất ra 2 file:
echo - File _filtered: Chứa kết quả lọc
echo - File _remaining: File gốc đã xóa kết quả lọc
echo.
echo ================================
echo.

cd /d "%~dp0"

if not exist "src\bg3_filter.py" (
    echo ❌ Không tìm thấy file bg3_filter.py trong thư mục src
    echo Vui lòng kiểm tra lại đường dẫn.
    pause
    exit /b 1
)

echo 🚀 Khởi chạy BG3 Simplified Filter Tool...
echo.

python src\bg3_filter.py --gui

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Có lỗi xảy ra khi chạy ứng dụng.
    echo Mã lỗi: %ERRORLEVEL%
    echo.
    echo Đang thử chạy bằng python3...
    python3 src\bg3_filter.py --gui
    
    if !ERRORLEVEL! NEQ 0 (
        echo.
        echo ❌ Vẫn không thể chạy. Vui lòng kiểm tra:
        echo - Python đã được cài đặt và thêm vào PATH
        echo - Các thư viện cần thiết đã được cài đặt
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ✅ Hoàn thành!
pause

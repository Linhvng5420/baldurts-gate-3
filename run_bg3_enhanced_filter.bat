@echo off
chcp 65001 >nul
title BG3 Enhanced Filter Tool

echo ============================================
echo   BG3 Enhanced Filter Tool
echo   Công cụ lọc nâng cao cho Baldur's Gate 3
echo ============================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python không được tìm thấy. Vui lòng cài đặt Python 3.7+
    pause
    exit /b 1
)

:: Check if the enhanced filter script exists
if not exist "src\bg3_filter_enhanced.py" (
    echo ERROR: Không tìm thấy file bg3_filter_enhanced.py trong thư mục src
    pause
    exit /b 1
)

echo Các tùy chọn sử dụng:
echo.
echo 1. Lọc UI Text (tách giao diện người dùng)
echo 2. Lọc English-only (loại bỏ text chỉ tiếng Anh)
echo 3. Lọc Non-English (giữ lại text không phải tiếng Anh)
echo 4. Lọc Dialogue (tách đối thoại)
echo 5. Lọc Technical (tách text kỹ thuật)
echo 6. Lọc theo Context (phân loại theo nội dung)
echo 7. Lọc tất cả loại
echo 8. Chỉ phân tích file (không tạo output)
echo 9. Hiển thị help
echo.

set /p choice="Chọn tùy chọn (1-9): "

if "%choice%"=="1" goto ui_filter
if "%choice%"=="2" goto english_filter
if "%choice%"=="3" goto non_english_filter
if "%choice%"=="4" goto dialogue_filter
if "%choice%"=="5" goto technical_filter
if "%choice%"=="6" goto context_filter
if "%choice%"=="7" goto all_filter
if "%choice%"=="8" goto analyze_only
if "%choice%"=="9" goto show_help

echo Tùy chọn không hợp lệ!
pause
exit /b 1

:ui_filter
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang lọc UI text...
python src\bg3_filter_enhanced.py "%input_file%" --ui-text --verbose
goto end

:english_filter
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang lọc English-only...
python src\bg3_filter_enhanced.py "%input_file%" --english-only --verbose
goto end

:non_english_filter
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang lọc Non-English...
python src\bg3_filter_enhanced.py "%input_file%" --non-english --verbose
goto end

:dialogue_filter
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang lọc Dialogue...
python src\bg3_filter_enhanced.py "%input_file%" --dialogue --verbose
goto end

:technical_filter
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang lọc Technical...
python src\bg3_filter_enhanced.py "%input_file%" --technical --verbose
goto end

:context_filter
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang lọc theo Context...
python src\bg3_filter_enhanced.py "%input_file%" --by-context --verbose
goto end

:all_filter
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang lọc tất cả loại...
python src\bg3_filter_enhanced.py "%input_file%" --all --verbose
goto end

:analyze_only
set /p input_file="Nhập đường dẫn file XML: "
if not exist "%input_file%" (
    echo File không tồn tại: %input_file%
    pause
    exit /b 1
)
echo Đang phân tích file...
python src\bg3_filter_enhanced.py "%input_file%" --analyze-only --verbose
goto end

:show_help
python src\bg3_filter_enhanced.py --help
goto end

:end
echo.
echo Hoàn thành! Kiểm tra kết quả trong thư mục output/filtered
echo.
pause

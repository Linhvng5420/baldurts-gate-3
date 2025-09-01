@echo off
chcp 65001 > nul
title BG3 Enhanced Filter Tool

:: Kiểm tra Python đã được cài đặt chưa
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [31mLỗi: Không tìm thấy Python. Vui lòng cài đặt Python 3.x[0m
    echo Bạn có thể tải Python tại: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Kiểm tra và cài đặt các thư viện cần thiết
echo Đang kiểm tra các thư viện cần thiết...
pip install -r requirements.txt > nul 2>&1

:: Hiện menu chọn chế độ
:menu
cls
echo =======================================
echo   BG3 Enhanced Filter Tool
echo =======================================
echo.
echo  [1] Chạy với giao diện đồ họa (GUI)
echo  [2] Chạy với dòng lệnh (CLI)
echo  [3] Thoát
echo.
set /p choice="Vui lòng chọn (1-3): "

if "%choice%"=="1" (
    start pythonw src/bg3_filter_all.py --gui
) else if "%choice%"=="2" (
    python src/bg3_filter_all.py --cli
) else if "%choice%"=="3" (
    exit /b 0
) else (
    echo.
    echo [31mLựa chọn không hợp lệ. Vui lòng chọn lại.[0m
    timeout /t 2 > nul
    goto menu
)

pause

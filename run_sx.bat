@echo off
chcp 65001 >nul
echo Đang cài đặt các thư viện cần thiết...
pip install pyperclip
echo.
echo Khởi động ứng dụng sắp xếp XML...
python "D:\Games\Baldurt's Gate VH\baldurts-gate-3\src\App Sap Xep\sx.py"
pause

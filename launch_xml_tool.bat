@echo off
:: ====================================================================
:: Khởi chạy Công cụ xử lý XML - Baldur's Gate 3 Việt Hóa
:: ====================================================================
title Khoi chay XML Tool BG3

echo.
echo ========================================
echo   CONG CU XU LY XML - BALDUR'S GATE 3
echo ========================================
echo.

:: Kiểm tra yêu cầu hệ thống
echo [1/5] Kiem tra yeu cau he thong...

:: Kiểm tra hệ điều hành Windows
ver | findstr /i "windows" >nul
if errorlevel 1 (
    echo ❌ Loi: Chi ho tro he dieu hanh Windows
    pause
    exit /b 1
)
echo ✅ He dieu hanh: Windows

:: Lưu thư mục hiện tại
set "ORIGINAL_DIR=%CD%"

:: Chuyển đến thư mục gốc của project
cd /d "%~dp0"
echo ✅ Thu muc lam viec: %CD%

:: Kiểm tra Python virtual environment
echo.
echo [2/5] Kiem tra Python virtual environment...

set "VENV_PATH=%CD%\.venv"
set "PYTHON_EXE=%VENV_PATH%\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo ❌ Loi: Khong tim thay Python virtual environment
    echo    Duong dan mong doi: %PYTHON_EXE%
    echo.
    echo    Vui long chay setup_first_time.bat truoc tien
    pause
    exit /b 1
)
echo ✅ Python virtual environment: %VENV_PATH%

:: Kiểm tra phiên bản Python
echo.
echo [3/5] Kiem tra phien ban Python...
"%PYTHON_EXE%" --version
if errorlevel 1 (
    echo ❌ Loi: Khong the chay Python
    pause
    exit /b 1
)
echo ✅ Python dang hoat dong

:: Kiểm tra các thư viện cần thiết
echo.
echo [4/5] Kiem tra cac thu vien can thiet...

echo Dang kiem tra thu vien...
"%PYTHON_EXE%" -c "import tkinter; print('✅ tkinter')" 2>nul
if errorlevel 1 (
    echo ❌ Loi: Thu vien tkinter khong co san
    echo    Tkinter la thu vien GUI mac dinh cua Python
    pause
    exit /b 1
)

"%PYTHON_EXE%" -c "import re; print('✅ re')" 2>nul
if errorlevel 1 (
    echo ❌ Loi: Thu vien re khong co san
    pause
    exit /b 1
)

"%PYTHON_EXE%" -c "import xml.etree.ElementTree; print('✅ xml.etree.ElementTree')" 2>nul
if errorlevel 1 (
    echo ❌ Loi: Thu vien xml.etree.ElementTree khong co san
    pause
    exit /b 1
)

"%PYTHON_EXE%" -c "import threading; print('✅ threading')" 2>nul
if errorlevel 1 (
    echo ❌ Loi: Thu vien threading khong co san
    pause
    exit /b 1
)

"%PYTHON_EXE%" -c "import json; print('✅ json')" 2>nul
if errorlevel 1 (
    echo ❌ Loi: Thu vien json khong co san
    pause
    exit /b 1
)

:: Kiểm tra các thư viện bổ sung (không bắt buộc nhưng được khuyến nghị)
set "MISSING_LIBS="

"%PYTHON_EXE%" -c "import pyperclip; print('✅ pyperclip (clipboard support)')" 2>nul
if errorlevel 1 (
    echo ⚠️  Canh bao: Thu vien pyperclip khong co san (tinh nang clipboard se bi han che)
    set "MISSING_LIBS=%MISSING_LIBS% pyperclip"
)

"%PYTHON_EXE%" -c "import tkinterdnd2; print('✅ tkinterdnd2 (drag and drop support)')" 2>nul
if errorlevel 1 (
    echo ⚠️  Canh bao: Thu vien tkinterdnd2 khong co san (tinh nang drag and drop se bi han che)
    set "MISSING_LIBS=%MISSING_LIBS% tkinterdnd2"
)

"%PYTHON_EXE%" -c "import tqdm; print('✅ tqdm (progress bar)')" 2>nul
if errorlevel 1 (
    echo ⚠️  Canh bao: Thu vien tqdm khong co san (thanh tien trinh se bi han che)
    set "MISSING_LIBS=%MISSING_LIBS% tqdm"
)

:: Nếu có thư viện thiếu, hỏi user có muốn cài đặt không
if not "%MISSING_LIBS%"=="" (
    echo.
    echo ========================================
    echo   CAC THU VIEN BO SUNG DANG THIEU
    echo ========================================
    echo.
    echo Cac thu vien sau dang thieu:%MISSING_LIBS%
    echo.
    echo Cac thu vien nay khong bat buoc nhung se cai thien trai nghiem su dung:
    echo - pyperclip: Ho tro sao chep/dan tu clipboard
    echo - tkinterdnd2: Ho tro keo tha file vao ung dung
    echo - tqdm: Hien thi thanh tien trinh khi xu ly file lon
    echo.
    set /p "INSTALL_CHOICE=Ban co muon cai dat cac thu vien nay khong? (y/n): "
    
    if /i "%INSTALL_CHOICE%"=="y" (
        echo.
        echo 🔧 Dang cai dat cac thu vien bo sung...
        
        for %%i in (%MISSING_LIBS%) do (
            echo Dang cai dat %%i...
            "%VENV_PATH%\Scripts\pip.exe" install %%i
            if errorlevel 1 (
                echo ❌ Loi khi cai dat %%i
            ) else (
                echo ✅ Da cai dat thanh cong %%i
            )
        )
        
        echo.
        echo ✅ Hoan tat cai dat cac thu vien bo sung
        echo.
        pause
    ) else (
        echo.
        echo ℹ️  Bo qua cai dat cac thu vien bo sung
        echo   Ban co the cai dat sau bang lenh: pip install%MISSING_LIBS%
        echo.
    )
)

echo.
echo ✅ Kiem tra thu vien hoan tat

:: Kiểm tra file ứng dụng
echo.
echo [5/5] Kiem tra file ung dung...

set "APP_FILE=%CD%\src\XML-Tool-BG3\xml_tool_bg3.py"
if not exist "%APP_FILE%" (
    echo ❌ Loi: Khong tim thay file ung dung
    echo    Duong dan mong doi: %APP_FILE%
    pause
    exit /b 1
)
echo ✅ File ung dung: %APP_FILE%

:: Tạo thư mục output nếu chưa tồn tại
if not exist "%CD%\output" (
    mkdir "%CD%\output"
    echo ✅ Da tao thu muc output
) else (
    echo ✅ Thu muc output da ton tai
)

echo.
echo ========================================
echo   TAT CA CAC KIEM TRA DA HOAN TAT
echo ========================================
echo.
echo 🚀 Dang khoi chay Cong cu xu ly XML...
echo.

:: Khởi chạy ứng dụng
"%PYTHON_EXE%" "%APP_FILE%"

:: Kiểm tra mã thoát
if errorlevel 1 (
    echo.
    echo ❌ Ung dung da thoat voi loi
    echo    Ma loi: %errorlevel%
    echo.
    echo 💡 Goi y:
    echo    - Kiem tra lai cac thu vien da cai dat
    echo    - Chay setup_first_time.bat de cai dat lai
    echo    - Lien he ho tro ky thuat neu van gap van de
) else (
    echo.
    echo ✅ Ung dung da dong binh thuong
)

echo.
echo Nhan phim bat ky de thoat...
pause >nul

:: Quay về thư mục ban đầu
cd /d "%ORIGINAL_DIR%"

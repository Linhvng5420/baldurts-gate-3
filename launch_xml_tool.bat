@echo off
:: ====================================================================
:: Khởi chạy Công cụ xử lý XML - Baldur's Gate 3 Việt Hóa (Tự động Setup)
:: ====================================================================
title Khoi chay XML Tool BG3 - Auto Setup

echo.
echo ========================================
echo   CONG CU XU LY XML - BALDUR'S GATE 3
echo   (Automatic Setup and Launch)
echo ========================================
echo.

:: Lưu thư mục hiện tại
set "ORIGINAL_DIR=%CD%"

:: Chuyển đến thư mục gốc của project
cd /d "%~dp0"

:: Kiểm tra yêu cầu hệ thống
echo [1/7] Kiem tra yeu cau he thong...

:: Kiểm tra hệ điều hành Windows
ver | findstr /i "windows" >nul
if errorlevel 1 (
    echo ❌ Loi: Chi ho tro he dieu hanh Windows
    pause
    exit /b 1
)
echo ✅ He dieu hanh: Windows
echo ✅ Thu muc lam viec: %CD%

:: Kiểm tra Python cài đặt trên hệ thống
echo.
echo [2/7] Kiem tra Python he thong...

:: Định nghĩa yêu cầu phiên bản tối thiểu
set "MIN_PYTHON_VERSION=3.8"
echo 📋 App yeu cau: Python %MIN_PYTHON_VERSION% tro len

:: Thử tìm Python từ các nguồn khác nhau
set "SYSTEM_PYTHON="
set "PYTHON_VERSION="

:: Kiểm tra python3 trước
python3 --version >nul 2>&1
if not errorlevel 1 (
    set "SYSTEM_PYTHON=python3"
    for /f "tokens=2" %%v in ('python3 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    call echo ✅ Tim thay Python3: %%PYTHON_VERSION%%
    goto :python_found
)

:: Kiểm tra python
python --version >nul 2>&1
if not errorlevel 1 (
    set "SYSTEM_PYTHON=python"
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    call echo ✅ Tim thay Python: %%PYTHON_VERSION%%
    goto :python_found
)

:: Kiểm tra py launcher
py --version >nul 2>&1
if not errorlevel 1 (
    set "SYSTEM_PYTHON=py"
    for /f "tokens=2" %%v in ('py --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    call echo ✅ Tim thay Python Launcher: %%PYTHON_VERSION%%
    goto :python_found
)

echo ❌ Loi: Khong tim thay Python tren he thong
echo.
echo 💡 Vui long cai dat Python tu https://python.org
echo    - Chon phien ban Python 3.8 tro len
echo    - Tick chon "Add Python to PATH" khi cai dat
echo.
pause
exit /b 1

:python_found

:: Kiểm tra phiên bản Python có đáp ứng yêu cầu không
echo.
echo 🔍 Kiem tra phien ban Python...
call echo    - Python hien tai: Python %%PYTHON_VERSION%%
call echo    - Yeu cau toi thieu: Python %%MIN_PYTHON_VERSION%%

@REM :: Sử dụng Python để kiểm tra phiên bản
@REM %SYSTEM_PYTHON% -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>nul
@REM if errorlevel 1 (
@REM     echo ❌ Loi: Phien ban Python qua cu (can Python 3.8+)
@REM     call echo    Phien ban hien tai: %%PYTHON_VERSION%%
@REM     echo    Vui long cap nhat Python tai https://python.org
@REM     pause
@REM     exit /b 1
@REM )

@REM call echo ✅ Phien ban Python phu hop: %%PYTHON_VERSION%% (>= %%MIN_PYTHON_VERSION%%)

:: Kiểm tra và tạo Python virtual environment
echo.
echo [3/7] Kiem tra Python virtual environment...

set "VENV_PATH=%CD%\.venv"
set "PYTHON_EXE=%VENV_PATH%\Scripts\python.exe"
set "PIP_EXE=%VENV_PATH%\Scripts\pip.exe"

if not exist "%PYTHON_EXE%" (
    echo ⚠️  Khong tim thay virtual environment, dang tao moi...
    
    :: Tạo virtual environment mới
    echo 🔧 Tao Python virtual environment...
    %SYSTEM_PYTHON% -m venv "%VENV_PATH%"
    
    if not exist "%PYTHON_EXE%" (
        echo ❌ Loi: Khong the tao virtual environment
        echo    Vui long kiem tra lai Python installation
        pause
        exit /b 1
    )
    
    echo ✅ Da tao thanh cong virtual environment
    
    :: Cập nhật pip
    echo 🔧 Cap nhat pip...
    "%PYTHON_EXE%" -m pip install --upgrade pip
    
    if errorlevel 1 (
        echo ⚠️  Canh bao: Khong the cap nhat pip, nhung co the tiep tuc
    ) else (
        echo ✅ Da cap nhat pip thanh cong
    )
    
) else (
    echo ✅ Virtual environment da ton tai: %VENV_PATH%
)

:: Kiểm tra phiên bản Python trong venv
echo.
echo [4/7] Kiem tra phien ban Python...
"%PYTHON_EXE%" --version
if errorlevel 1 (
    echo ❌ Loi: Khong the chay Python trong virtual environment
    echo    Thu xoa thu muc .venv va chay lai script
    pause
    exit /b 1
)
echo ✅ Python trong virtual environment dang hoat dong

:: Kiểm tra và cài đặt các thư viện cần thiết
echo.
echo [5/7] Kiem tra va cai dat cac thu vien can thiet...

:: Danh sách các thư viện cần thiết
set "REQUIRED_LIBS=tkinter re xml.etree.ElementTree threading json"
set "OPTIONAL_LIBS=pyperclip tkinterdnd2 tqdm"

echo 🔍 Kiem tra cac thu vien co ban...

:: Kiểm tra thư viện cơ bản (thường có sẵn)
for %%i in (%REQUIRED_LIBS%) do (
    "%PYTHON_EXE%" -c "import %%i; print('✅ %%i')" 2>nul
    if errorlevel 1 (
        echo ❌ Loi: Thu vien %%i khong co san
        echo    Day la thu vien co ban cua Python, vui long kiem tra lai Python installation
        pause
        exit /b 1
    )
)

echo 🔍 Kiem tra va cai dat cac thu vien bo sung...

:: Kiểm tra và cài đặt thư viện bổ sung
set "INSTALL_NEEDED=0"
for %%i in (%OPTIONAL_LIBS%) do (
    "%PYTHON_EXE%" -c "import %%i; print('✅ %%i - da co san')" 2>nul
    if errorlevel 1 (
        echo ⚠️  %%i - chua cai dat, se cai dat tu dong
        set "INSTALL_NEEDED=1"
    )
)

if "%INSTALL_NEEDED%"=="1" (
    echo.
    echo 🔧 Dang cai dat cac thu vien bo sung...
    
    for %%i in (%OPTIONAL_LIBS%) do (
        "%PYTHON_EXE%" -c "import %%i" 2>nul
        if errorlevel 1 (
            echo 📦 Cai dat %%i...
            "%PIP_EXE%" install %%i --quiet
            if errorlevel 1 (
                echo ⚠️  Canh bao: Khong the cai dat %%i (se hoat dong voi chuc nang han che)
            ) else (
                echo ✅ Da cai dat thanh cong %%i
            )
        )
    )
    
    echo.
    echo ✅ Hoan tat cai dat cac thu vien bo sung
) else (
    echo ✅ Tat ca cac thu vien bo sung da duoc cai dat
)

:: Kiểm tra file ứng dụng
echo.
echo [6/7] Kiem tra file ung dung...

set "APP_FILE=%CD%\src\XML-Tool-BG3\xml_tool_bg3.py"
if not exist "%APP_FILE%" (
    echo ❌ Loi: Khong tim thay file ung dung
    echo    Duong dan mong doi: %APP_FILE%
    echo.
    echo 💡 Vui long kiem tra:
    echo    - File xml_tool_bg3.py co ton tai khong
    echo    - Duong dan thu muc src\XML-Tool-BG3\ co dung khong
    pause
    exit /b 1
)
echo ✅ File ung dung: %APP_FILE%

:: Tạo các thư mục cần thiết
echo.
echo [7/7] Chuan bi thu muc lam viec...

set "REQUIRED_DIRS=output input data"
for %%d in (%REQUIRED_DIRS%) do (
    if not exist "%CD%\%%d" (
        mkdir "%CD%\%%d"
        echo ✅ Da tao thu muc %%d
    ) else (
        echo ✅ Thu muc %%d da ton tai
    )
)

:: Kiểm tra cuối cùng - thử chạy Python script để đảm bảo mọi thứ hoạt động
echo.
echo 🧪 Kiem tra cuoi cung - thu nghiem chay ung dung...

"%PYTHON_EXE%" -c "import tkinter, threading, json, xml.etree.ElementTree; print('✅ All core libraries working correctly')" 2>nul
if errorlevel 1 (
    echo ❌ Loi: Co van de voi cac thu vien Python co ban
    echo    Vui long kiem tra lai installation
    pause
    exit /b 1
)

"%PYTHON_EXE%" -c "import pyperclip; print('✅ Clipboard support available')" 2>nul
if errorlevel 1 (
    echo ⚠️  Clipboard support limited
) 

"%PYTHON_EXE%" -c "import tkinterdnd2; print('✅ Drag and drop support available')" 2>nul
if errorlevel 1 (
    echo ⚠️  Drag and drop support limited
)

"%PYTHON_EXE%" -c "import tqdm; print('✅ Progress bar support available')" 2>nul
if errorlevel 1 (
    echo ⚠️  Progress bar support limited
)

echo.
echo ========================================
echo   SETUP HOAN TAT - KHOI CHAY UNG DUNG
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
    echo    - Kiem tra lai file xml_tool_bg3.py
    echo    - Kiem tra log loi phia tren
    echo    - Lien he ho tro ky thuat neu van gap van de
    echo.
    echo Nhan phim bat ky de thoat...
    pause >nul
) else (
    echo.
    echo ✅ Ung dung da dong binh thuong
)

:: Quay về thư mục ban đầu
cd /d "%ORIGINAL_DIR%"

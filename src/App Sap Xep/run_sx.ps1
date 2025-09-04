# PowerShell script để chạy ứng dụng XML Sorter
Write-Host "=== XML Content Sorter ===" -ForegroundColor Green
Write-Host "Đang kiểm tra môi trường Python..." -ForegroundColor Yellow

# Kiểm tra xem có virtual environment không
$venvPython = "D:/Games/Baldurt's Gate VH/baldurts-gate-3/.venv/Scripts/python.exe"
if (Test-Path $venvPython) {
    Write-Host "Sử dụng Python Virtual Environment" -ForegroundColor Green
    & $venvPython sx.py
} else {
    Write-Host "Sử dụng Python hệ thống" -ForegroundColor Yellow
    python sx.py
}

Write-Host "Nhấn Enter để thoát..." -ForegroundColor Cyan
Read-Host

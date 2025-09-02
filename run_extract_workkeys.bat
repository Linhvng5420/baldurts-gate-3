@echo off
chcp 65001 >nul
cd /d "d:\Games\Baldurt's Gate VH\baldurts-gate-3\src"
echo Running BG3 Workkeys Extractor...
echo.
echo | python extract_workkeys.py "d:\Games\Baldurt's Gate VH\baldurts-gate-3\data\wip\Package English Path8_4.116897358\english.xml"
echo.
echo Script completed. Press any key to exit...
pause >nul

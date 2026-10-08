@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo 找不到游戏运行环境，请先联系我重新配置。
    pause
    exit /b 1
)

".venv\Scripts\python.exe" main.py
echo.
echo 游戏已结束。按任意键关闭此窗口。
pause > nul

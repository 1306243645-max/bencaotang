@echo off
chcp 65001 >nul
title 本草堂 · AI 员工团队

cd /d "%~dp0"

echo.
echo ╔══════════════════════════════════════════════╗
echo ║      🌿 本草堂 · AI 员工团队启动中...       ║
echo ╚══════════════════════════════════════════════╝
echo.

echo [1/2] 检查 Python 环境...
call .venv\Scripts\python.exe --version
if %errorlevel% neq 0 (
    echo ❌ Python 环境未找到，请先运行: python -m venv .venv
    pause
    exit /b 1
)

echo.
echo [2/2] 启动 AI 员工早会...
echo.
call .venv\Scripts\python.exe agents\orchestrator.py --mode morning

echo.
echo ╔══════════════════════════════════════════════╗
echo ║  🌅 早会结束！AI员工团队已就绪              ║
echo ║                                            ║
echo ║  🎧 小堂(客服)   — 待命中                  ║
echo ║  ✍️ 文白(内容官) — 待命中                  ║
echo ║  💰 千帆(销售)   — 待命中                  ║
echo ║  📊 墨竹(运营)   — 待命中                  ║
echo ║                                            ║
echo ║  其他命令:                                 ║
echo ║  .venv\Scripts\python agents\orchestrator.py --mode today  ║
echo ║  .venv\Scripts\python agents\orchestrator.py --mode report ║
echo ║  .venv\Scripts\python agents\orchestrator.py --mode chat   ║
echo ╚══════════════════════════════════════════════╝
echo.
pause

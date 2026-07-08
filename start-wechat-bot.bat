@echo off
cd /d C:\Users\Admin\agent-workstation
echo ========================================
echo   BenCao Tang TCM Clinic · 微信剪贴板模式
echo ========================================
echo.
echo 使用方法:
echo   1. 在微信中复制收到的消息 (Ctrl+C)
echo   2. AI 自动分析并生成回复
echo   3. 在微信中粘贴回复 (Ctrl+V)
echo.
echo 按 Ctrl+C 退出
echo ========================================
echo.
.venv\Scripts\python.exe bots\wechat_bot.py --mode clipboard
pause

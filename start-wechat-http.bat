@echo off
cd /d C:\Users\Admin\agent-workstation
echo ========================================
echo   BenCao Tang TCM Clinic · 微信 HTTP 回调模式
echo ========================================
echo.
echo Webhook URL: http://localhost:9000/wechat
echo.
echo 适用于: 微信公众号 / 企业微信 / 第三方机器人平台
echo 按 Ctrl+C 退出
echo ========================================
echo.
.venv\Scripts\python.exe bots\wechat_bot.py --mode http --port 9000
pause

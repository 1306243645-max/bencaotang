@echo off
cd /d C:\Users\Admin\agent-workstation
echo ========================================
echo   妙手堂 · 智能体自动驾驶
echo ========================================
echo.
echo 即将自动生成 30 天全平台内容：
echo   微信公众号文章 x30
echo   抖音/视频号脚本 x30
echo   小红书图文 x30
echo   养生日签 x30
echo.
echo 预计耗时: 5-10 分钟
echo ========================================
echo.
.venv\Scripts\python.exe bots/auto_pilot.py --mode batch --days 30
echo.
echo 完成！打开 output\auto\ 查看生成的内容
pause

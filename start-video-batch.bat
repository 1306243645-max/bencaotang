@echo off
cd /d C:\Users\Admin\agent-workstation
echo ========================================
echo   BenCao Tang TCM Clinic · 批量生成短视频
echo ========================================
echo.
echo 将生成 5 条中医科普视频:
echo   1. 失眠为什么总在2-3点醒
echo   2. 饭后犯困不是懒是脾虚
echo   3. 手脚冰凉怎么办
echo   4. 口干喝水没用
echo   5. 澳洲超市里的中药食材
echo.
echo 输出目录: output\videos\
echo ========================================
echo.
.venv\Scripts\python.exe bots/video_maker.py --batch
echo.
echo 完成！打开 output\videos\ 查看视频
pause

@echo off
cd /d C:\Users\Admin\agent-workstation
echo ╔══════════════════════════════════════╗
echo ║   妙手堂 · 一键生成今日全部内容   ║
echo ╚══════════════════════════════════════╝
echo.
echo [1/4] 生成今日推广文案...
.venv\Scripts\python.exe bots/auto_pilot.py --mode today
echo.
echo [2/4] 生成动漫视频...
.venv\Scripts\python.exe -c "import sys;sys.path.insert(0,'.');from bots.anime_video import batch_anime;batch_anime()"
echo.
echo [3/4] 生成分享海报...
.venv\Scripts\python.exe -c "import sys;sys.path.insert(0,'.');from bots.share_poster import create_poster;create_poster('http://172.20.21.34:8501','山东妙手堂中医诊所','本草济世·仁心济世','扫码体验AI舌诊+体质自测+周易面诊+风水+问茶')"
echo.
echo [4/4] 打开成果文件夹...
explorer output\auto
explorer output\anime
explorer output\posters
echo.
echo ╔══════════════════════════════════════╗
echo ║  全部完成！文件夹已打开，开始发布  ║
echo ╚══════════════════════════════════════╝
echo.
echo 发布清单：
echo   1. 朋友圈 → 复制 output\auto\today_*.json 里的 wechat_post
echo   2. 视频号 → 上传 output\anime\ 里的动漫视频
echo   3. 小红书 → 复制 xiaohongshu 文案 + 配海报图
echo   4. 公众号 → 复制 wechat_post → 新建群发
echo.
pause

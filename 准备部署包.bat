@echo off
cd /d C:\Users\Admin\agent-workstation
echo ╔══════════════════════════════════════╗
echo ║   妙手堂 · 打包免费部署文件       ║
echo ╚══════════════════════════════════════╝
echo.
set DEPLOY_DIR=deploy_package

rmdir /s /q %DEPLOY_DIR% 2>nul
mkdir %DEPLOY_DIR%
mkdir %DEPLOY_DIR%\data\tcm
mkdir %DEPLOY_DIR%\web
mkdir %DEPLOY_DIR%\web\static

echo 复制核心文件...
copy streamlit_app.py %DEPLOY_DIR%\
copy requirements.txt %DEPLOY_DIR%\
copy README.md %DEPLOY_DIR%\

echo 复制知识库...
copy data\tcm\*.md %DEPLOY_DIR%\data\tcm\

echo 复制网站文件...
copy web\app.py %DEPLOY_DIR%\web\
copy web\static\orange_cat.png %DEPLOY_DIR%\web\static\ 2>nul
copy web\static\*.png %DEPLOY_DIR%\web\static\ 2>nul

echo.
echo ╔══════════════════════════════════════╗
echo ║  打包完成！                        ║
echo ║  文件夹: deploy_package\            ║
echo ╚══════════════════════════════════════╝
echo.
echo 下一步:
echo   方案A: 打开 https://huggingface.co/new-space
echo   方案B: 打开 https://dashboard.render.com
echo.
echo 把 deploy_package 里的文件拖到网页上传即可！

explorer %DEPLOY_DIR%
pause

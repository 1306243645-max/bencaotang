@echo off
chcp 65001 >nul
title 本草堂 · 永久隧道安装

cd /d "%~dp0"
echo ╔══════════════════════════════════════════════╗
echo ║   🌿 本草堂 · 永久公网隧道安装              ║
echo ║   装一次，永久生效，自动续连                 ║
echo ╚══════════════════════════════════════════════╝
echo.

:: 1. 下载 cloudflared
echo [1/3] 下载 cloudflared...
curl -L -o cloudflared.exe "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
if %errorlevel% neq 0 (
    echo ❌ 下载失败，请检查网络
    pause
    exit /b 1
)
echo ✅ 下载完成
echo.

:: 2. 启动隧道
echo [2/3] 启动隧道...
echo 注意：隧道会持续运行，看到 https://xxx.trycloudflare.com 就成功了
echo 按 Ctrl+C 可以停止
echo.
echo ═══════════════════════════════════════════════
cloudflared.exe tunnel --url http://localhost:8501

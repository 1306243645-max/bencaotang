"""简易公网隧道——通过 Cloudflare 免费隧道"""
import subprocess, sys, os

print("下载 cloudflared...")
os.system("curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe -o cloudflared.exe 2>nul")

# Alternative: just show current status
print("\n当前网站状态:")
print("  本机: http://localhost:8501")
print("  局域网: http://172.20.21.34:8501")
print()
print("推荐方案:")
print("1. 注册 ngrok 免费账号: https://dashboard.ngrok.com/signup")
print("2. 复制你的 authtoken")
print("3. 告诉我 token，帮你一键启动稳定隧道")
print()
print("ngrok 比 localtunnel 稳定 100 倍，不会断不会弹验证页")

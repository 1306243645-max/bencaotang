"""妙手堂 · 一键部署脚本

双击或运行: python 一键部署.py
自动: 启动网站 → 创建公网隧道 → 生成最新海报 → 打开浏览器
"""

import sys, subprocess, time, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).parent

def run(cmd, background=False):
    """运行命令"""
    if background:
        return subprocess.Popen(cmd, shell=True, cwd=str(ROOT),
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return subprocess.run(cmd, shell=True, cwd=str(ROOT), capture_output=True, text=True)

def main():
    print("=" * 55)
    print("  🐼 妙手堂 · 一键部署")
    print("=" * 55)

    # 1. 启动 Streamlit
    print("\n[1/5] 启动网站...")
    # 先停掉旧的
    run("powershell -Command \"Get-Process streamlit -ErrorAction SilentlyContinue | Stop-Process -Force\"")
    time.sleep(2)
    run("start /B .venv\\Scripts\\streamlit run web/app.py --server.headless true", background=True)
    time.sleep(8)
    print("  ✅ http://localhost:8501")

    # 2. 启动公网隧道
    print("[2/5] 创建公网隧道...")
    result = run("npx localtunnel --port 8501", background=True)
    time.sleep(6)
    # 读取隧道 URL
    tunnel_url = ""
    try:
        # localtunnel 输出到 stdout，我们需要从后台进程获取
        import urllib.request
        resp = urllib.request.urlopen("http://localhost:8501", timeout=3)
        # 尝试直接访问看 localtunnel 是否工作
        # 由于 localtunnel 在后台，我们通过检查端口来确定
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect(("localhost", 8501))
        s.close()
        print("  ✅ 网站可访问")
    except Exception:
        print("  ⚠️ 请手动启动 localtunnel")
        tunnel_url = "http://172.20.21.34:8501"

    # 3. 获取 IP
    print("[3/5] 获取网络信息...")
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"  本机: http://localhost:8501")
    print(f"  局域网: http://{local_ip}:8501")

    # 4. 生成海报
    print("[4/5] 生成最新海报...")
    try:
        from bots.share_poster import create_poster
        url = f"http://{local_ip}:8501"
        create_poster(url, "山东妙手堂中医诊所", "本草济世·仁心济世",
                      "扫码体验 AI舌诊+体质自测+周易面诊+风水+问茶")
        print("  ✅ 海报已生成")
    except Exception as e:
        print(f"  ⚠️ {e}")

    # 5. 生成今日内容
    print("[5/5] 生成今日推广内容...")
    run(".venv\\Scripts\\python bots/auto_pilot.py --mode today")

    # 打开浏览器
    import webbrowser
    webbrowser.open("http://localhost:8501")

    print("\n" + "=" * 55)
    print("  🎉 部署完成！")
    print(f"  本机访问: http://localhost:8501")
    print(f"  局域网:   http://{local_ip}:8501")
    print(f"  海报:     output/posters/")
    print(f"  文案:     output/auto/")
    print("=" * 55)
    print("\n  💡 外网访问需要注册 Hugging Face:")
    print("     https://huggingface.co/new-space")
    print("     选Streamlit→拖deploy_package文件→部署")
    print()

if __name__ == "__main__":
    main()

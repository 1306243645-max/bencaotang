"""本草堂 · 公众号自动发布系统

功能：读取每日生成的内容 → 创建公众号草稿 → 定时发布

使用前准备：
    1. 公众号后台 → 开发 → 基本配置
    2. 获取 AppID 和 AppSecret
    3. 填入下方的配置区域
    4. 公众号后台 → 开发 → 基本配置 → 填写服务器白名单 IP

启动：
    python bots/wechat_auto_post.py --mode draft    # 创建草稿
    python bots/wechat_auto_post.py --mode publish  # 发布草稿
    python bots/wechat_auto_post.py --mode auto     # 创建草稿+预览
"""

import sys, json, requests
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

# ══════════════ 在此填入公众号配置 ══════════════
APPID = "YOUR_APPID_HERE"           # 公众号后台获取
APPSECRET = "YOUR_APPSECRET_HERE"   # 公众号后台获取
# ═══════════════════════════════════════════════

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
DRAFT_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"
PUBLISH_URL = "https://api.weixin.qq.com/cgi-bin/freepublish/submit"


def get_token():
    """获取 access_token"""
    resp = requests.get(TOKEN_URL, params={
        "grant_type": "client_credential",
        "appid": APPID,
        "secret": APPSECRET,
    })
    data = resp.json()
    if "access_token" in data:
        return data["access_token"]
    raise Exception(f"获取token失败: {data}")


def get_today_content():
    """读取今日生成的内容"""
    today = datetime.now().strftime("%Y%m%d")
    path = Path("output/auto") / f"today_{today}.json"
    if not path.exists():
        print(f"[提示] 今日内容尚未生成，先运行: python bots/auto_pilot.py --mode today")
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    content_str = data.get("content", "")

    # 提取 wechat_post
    import re
    match = re.search(r'wechat_post.*?\"(.*?)\"', content_str, re.DOTALL)
    if match:
        text = match.group(1)
        text = text.replace('\\n', '\n')
        return {
            "title": data.get("topic", "本草堂每日养生"),
            "content": text,
            "source": data,
        }
    return None


def create_draft():
    """创建公众号草稿"""
    article = get_today_content()
    if not article:
        return

    token = get_token()
    draft = {
        "articles": [{
            "title": article["title"],
            "content": article["content"].replace('\n', '<br>'),
            "content_source_url": "http://172.20.21.34:8501",
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
        }]
    }

    resp = requests.post(
        DRAFT_URL,
        params={"access_token": token},
        json=draft
    )
    result = resp.json()
    if "media_id" in result:
        print(f"[成功] 草稿已创建! media_id: {result['media_id']}")
        return result["media_id"]
    else:
        print(f"[失败] {result}")
        return None


def publish_draft():
    """发布草稿"""
    token = get_token()

    # 先获取草稿列表
    list_url = "https://api.weixin.qq.com/cgi-bin/draft/batchget"
    resp = requests.post(list_url, params={"access_token": token}, json={
        "offset": 0, "count": 1, "no_content": 1
    })
    drafts = resp.json()
    if "item" not in drafts or not drafts["item"]:
        print("[提示] 没有草稿，先创建草稿")
        return

    media_id = drafts["item"][0]["media_id"]

    # 发布
    resp = requests.post(
        "https://api.weixin.qq.com/cgi-bin/freepublish/submit",
        params={"access_token": token},
        json={"media_id": media_id}
    )
    result = resp.json()
    if result.get("errcode") == 0:
        print(f"[成功] 已发布! publish_id: {result.get('publish_id')}")
    else:
        print(f"[失败] {result}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["draft","publish","auto"], default="auto")
    args = p.parse_args()

    if APPID == "YOUR_APPID_HERE":
        print("=" * 50)
        print("  请先配置 AppID 和 AppSecret！")
        print("=" * 50)
        print()
        print("获取方式：")
        print("1. 打开 https://mp.weixin.qq.com")
        print("2. 左侧菜单 → 开发 → 基本配置")
        print("3. 复制 AppID 和 AppSecret")
        print("4. 填入本文件顶部的 APPID 和 APPSECRET")
        print()
        print("⚠️ 如果是首次使用，还需要：")
        print("  - 设置 IP 白名单")
        print("  - 点击「启用」开发者密码")
    else:
        if args.mode == "draft":
            create_draft()
        elif args.mode == "publish":
            publish_draft()
        else:
            print("[1/2] 生成今日内容...")
            mid = create_draft()
            if mid:
                print("\n[2/2] 草稿已就绪，登录公众号后台手动发布")
                print("   或运行 publish 命令发布")

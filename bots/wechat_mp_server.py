"""妙手堂 · 微信公众号 AI 后台

对接微信公众号，实现 AI 智能自动回复。
审核通过后配置：
    公众号后台 → 开发 → 基本配置 → 服务器配置
    URL: https://你的域名/wechat
    Token: 自定义一个token

启动：python bots/wechat_mp_server.py --port 80
"""

import sys, hashlib, time, xml.etree.ElementTree as ET
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from flask import Flask, request
from agents.tcm_agent import create_tcm_agent

# 配置（公众号后台设置）
TOKEN = "miaoshou2026"

# 初始化 AI Agent
agent = create_tcm_agent()
print("[妙手堂] 公众号 AI 后台已就绪")

app = Flask(__name__)


def verify_signature(signature, timestamp, nonce):
    """验证微信服务器签名"""
    tmp_list = sorted([TOKEN, timestamp, nonce])
    tmp_str = "".join(tmp_list)
    return hashlib.sha1(tmp_str.encode()).hexdigest() == signature


def parse_message(xml_data):
    """解析微信 XML 消息"""
    root = ET.fromstring(xml_data)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg


def build_reply(to_user, from_user, content):
    """构建回复 XML"""
    return f"""<xml>
<ToUserName><![CDATA[{to_user}]]></ToUserName>
<FromUserName><![CDATA[{from_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{content}]]></Content>
</xml>"""


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        # 微信服务器验证
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")

        if verify_signature(signature, timestamp, nonce):
            return echostr
        return "Verification failed", 403

    else:
        # 接收用户消息
        xml_data = request.data.decode("utf-8")
        msg = parse_message(xml_data)

        msg_type = msg.get("MsgType", "")
        from_user = msg.get("FromUserName", "")
        to_user = msg.get("ToUserName", "")

        if msg_type == "text":
            user_text = msg.get("Content", "").strip()
            print(f"[消息] {user_text[:50]}...")

            # 用 AI Agent 回复
            try:
                resp = agent.chat(user_text)
                reply = resp.content[:600]  # 微信限制 2048 字符
            except Exception:
                reply = "抱歉，请稍后再试。或拨打 18254191315 咨询。"

        elif msg_type == "event":
            event = msg.get("Event", "")
            if event == "subscribe":
                reply = (
                    "🌿 感谢关注山东妙手堂中医诊所！\n\n"
                    "我是小妙，你的AI健康小助手✨\n\n"
                    "🔮 周易面诊 — 拍照分析体质\n"
                    "👅 AI舌诊 — 舌象智能分析\n"
                    "📋 体质自测 — 9种体质精准辨识\n"
                    "🍳 民间偏方 — 36个家传食疗方\n\n"
                    "👇 点击菜单开始体验\n"
                    "或直接回复：体质 / 预约 / 食谱 / 失眠"
                )
            else:
                reply = "欢迎回到妙手堂！回复任意关键词开始问诊。"
        else:
            reply = "请发送文字消息，小妙为你解答~"

        return build_reply(to_user, from_user, reply)


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=80)
    args = p.parse_args()
    app.run(host="0.0.0.0", port=args.port)

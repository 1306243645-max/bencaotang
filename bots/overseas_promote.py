"""本草堂 · 海外推广引擎 + 获利转化

每天自动生成：海外社媒文案 + 产品推广 + TikTok脚本
"""

import sys, json
from pathlib import Path
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))
from agents.base import BaseAgent

OUTPUT = Path(__file__).parent.parent / "output" / "overseas"
OUTPUT.mkdir(parents=True, exist_ok=True)

AGENT = BaseAgent(
    system="""你是本草堂海外营销专家。任务：
1. 生成英文+TikTok风格的中医科普内容
2. 每条内容包含产品推广（茶饮/体质报告/课程）
3. 用海外受众能理解的语言（不谈阴阳，说 balance/energy/wellness）
4. 短视频脚本要求快节奏、有吸引力、15-60秒
5. 输出JSON格式""",
    max_tokens=4096, max_tool_rounds=0
)

TOPICS = [
    "失眠调理 insomnia TCM",
    "手脚冰凉 cold hands feet remedy",
    "中医体质 constitution quiz",
    "穴位按摩 acupressure for headache",
    "秋季养生 autumn wellness",
    "菊花枸杞茶 benefits",
    "泡脚 foot bath TCM",
]

PRODUCTS = [
    {"name":"Chrysanthemum Tea","price":"$12","link":"Shop now"},
    {"name":"Sleep Foot Soak","price":"$15","link":"Order"},
    {"name":"Body Type Report","price":"$9.9","link":"Get yours"},
    {"name":"TCM Basics Course","price":"$29","link":"Learn"},
    {"name":"Herbal Soup Kit","price":"$25","link":"Buy"},
]

def generate_overseas_content():
    """生成海外推广内容"""
    today = datetime.now()
    topic = TOPICS[today.day % len(TOPICS)]
    product = PRODUCTS[today.day % len(PRODUCTS)]

    print(f"🌍 生成海外内容: {topic}")

    prompt = f"""Topic: {topic}
Product to promote: {product['name']} ({product['price']})

Generate:
1. TikTok script (15-60s, English, hook in first 3s)
2. Instagram caption (with 5 hashtags)
3. Facebook post (educational + soft sell)
4. YouTube Shorts title + description

All content should end with CTA: "Comment 'TCM' for free body type quiz"
Output as JSON with keys: tiktok_script, instagram_caption, facebook_post, youtube_shorts"""

    resp = AGENT.chat(prompt)
    content = {
        "date": today.strftime("%Y-%m-%d"),
        "topic": topic,
        "product": product,
        "content": resp.content,
    }
    path = OUTPUT / f"overseas_{today:%Y%m%d}.json"
    path.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {path}")
    return content

def generate_sales_pitch():
    """生成当日带货话术"""
    today = datetime.now()
    product = PRODUCTS[today.day % len(PRODUCTS)]
    prompt = f"""Write a short sales pitch for {product['name']} ({product['price']}).
Style: friendly, not pushy. Include a TCM health tip related to the product.
Chinese + English bilingual. Under 150 words."""
    resp = AGENT.chat(prompt)
    path = OUTPUT / f"sales_{today:%Y%m%d}.txt"
    path.write_text(resp.content, encoding="utf-8")
    return resp.content

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["content","sales","all"], default="all")
    args = p.parse_args()

    print("=" * 50)
    print("🌍 本草堂 · 海外推广引擎")
    print("=" * 50)

    if args.mode in ("content","all"):
        generate_overseas_content()
    if args.mode in ("sales","all"):
        pitch = generate_sales_pitch()
        print(f"\n💰 今日带货话术:\n{pitch[:300]}...")

    print(f"\n📁 输出目录: {OUTPUT}")

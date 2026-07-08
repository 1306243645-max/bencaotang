"""本草堂 · 智能体自动驾驶系统

按计划自动执行：每日内容生成 → 视频脚本 → 社媒文案 → 推送
使用：python bots/auto_pilot.py  或  双击 start-autopilot.bat
"""

import sys, json, time
from pathlib import Path
from datetime import datetime, timedelta
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base import BaseAgent, Tool

OUTPUT = Path(__file__).parent.parent / "output" / "auto"
_KB = Path(__file__).parent.parent / "data" / "tcm"
def _read(f): return (_KB / f).read_text(encoding="utf-8")

# ── 初始化 Agent ──────────────────────────────────────────

SYSTEM = """你是本草堂中医诊所的内容创作专家。你精通中医理论、五运六气、食疗养生。
你的任务是根据给定的内容计划，生成高质量的中医科普内容。

输出规则：
1. 每条内容 80-200 字
2. 语言通俗易懂，像朋友在聊天
3. 每条包含一个中医知识点 + 一个实用小建议
4. 结尾加上引流话术（微信搜本草堂免费体质自测）
5. 用 JSON 格式输出"""

agent = BaseAgent(system=SYSTEM, max_tokens=4096, max_tool_rounds=3)
for t_name in ["basics","diet_therapy","common_conditions","herbs","meridians","formulas","wuyunliuqi","symptom_checker"]:
    try:
        agent.add_tool(Tool(f"read_{t_name}", t_name, {"type":"object","properties":{},"required":[]}, lambda n=t_name: _read(f"{n}.md")))
    except Exception: pass

# ── 内容计划 ──────────────────────────────────────────────

WEEKLY_THEMES = [
    {"week":1, "theme":"睡眠养生","topics":["失眠的三种中医分型","肝火扰心如何调理","睡前穴位按摩","助眠食疗","为什么11点前要睡觉","心肾不交型失眠","一周睡眠改善计划"]},
    {"week":2, "theme":"脾胃调理","topics":["脾虚的5个信号","为什么少吃生冷","小米粥的养生搭配","足三里正确按法","四神汤家庭做法","吃多了怎么办","一周健脾计划"]},
    {"week":3, "theme":"女性健康","topics":["痛经分寒热","四物汤科普","经前烦躁怎么调","枸杞的正确吃法","更年期的中医调理","乳房胀痛按哪里","女性四季养生要点"]},
    {"week":4, "theme":"四季养生","topics":["春夏养阳秋冬养阴","泡脚的正确姿势","一天中的养生时辰","为什么要春捂秋冻","冬季进补指南","三伏天怎么过","24节气养生法"]},
]

# ── 自动化任务 ────────────────────────────────────────────

def generate_daily_content(day_offset=0):
    """生成指定日期偏移量的每日内容。day_offset=0 是今天，1 是明天..."""
    target_date = datetime.now() + timedelta(days=day_offset)
    week_idx = (day_offset // 7) % len(WEEKLY_THEMES)
    day_idx = day_offset % 7
    week = WEEKLY_THEMES[week_idx]
    topic = week["topics"][day_idx]

    print(f"📝 生成 Day {day_offset+1}: {target_date.strftime('%m/%d')} - {topic}")

    prompt = f"""请为「{week['theme']}」系列生成今日内容。主题：「{topic}」

请生成以下内容（JSON格式）：
{{
  "wechat_post": "微信公众号/朋友圈短文（150字）",
  "video_script": "1分钟短视频口播脚本（120字）",
  "xiaohongshu": "小红书图文文案+标题（100字+吸引人标题）",
  "daily_tip": "一句话养生日签（20字金句）",
  "hashtags": "3-5个相关标签"
}}

要求：
- 内容通俗易懂，像朋友聊天
- 包含1个中医知识点+1个实用建议
- 小红书标题要吸引眼球
- 结尾引流：微信搜「本草堂」免费体质自测"""

    resp = agent.chat(prompt)
    return {"date": target_date.strftime("%Y-%m-%d"), "week": week_idx+1, "theme": week["theme"], "topic": topic, "content": resp.content}

def batch_generate(days=30):
    """批量生成 N 天的内容。"""
    print("=" * 60)
    print(f"🚀 本草堂自动驾驶 · 批量生成 {days} 天内容")
    print("=" * 60)

    all_content = []
    for i in range(days):
        try:
            content = generate_daily_content(i)
            all_content.append(content)
            # 每条之间短暂休息
            if i < days - 1:
                time.sleep(2)
        except Exception as e:
            print(f"   ❌ Day {i+1} 失败: {e}")
            all_content.append({"date": f"Day{i+1}", "error": str(e)})

    # 保存
    OUTPUT.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT / f"content_batch_{datetime.now():%Y%m%d_%H%M}.json"
    output_file.write_text(json.dumps(all_content, ensure_ascii=False, indent=2), encoding="utf-8")

    # 同时生成易读的 Markdown 版本
    md_file = OUTPUT / f"content_batch_{datetime.now():%Y%m%d_%H%M}.md"
    md_lines = [f"# 本草堂 · 自动驾驶内容输出\n", f"生成时间: {datetime.now()}\n\n---\n"]
    for c in all_content:
        md_lines.append(f"## Day {all_content.index(c)+1}: {c.get('topic','?')} ({c.get('date','?')})")
        md_lines.append(f"\n{c.get('content','生成失败')}\n\n---\n")
    md_file.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"\n✅ 全部完成！")
    print(f"   JSON: {output_file}")
    print(f"   MD:   {md_file}")
    return all_content

def generate_todays_post():
    """生成今日内容并打印。适合定时任务调用。"""
    content = generate_daily_content(0)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    today_file = OUTPUT / f"today_{datetime.now():%Y%m%d}.json"
    today_file.write_text(json.dumps(content, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 今日内容已保存: {today_file}")
    print(f"\n{'='*40}")
    print(content["content"][:500])
    return content

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="本草堂 · 自动驾驶")
    p.add_argument("--mode", choices=["today","batch"], default="batch")
    p.add_argument("--days", type=int, default=30)
    args = p.parse_args()

    if args.mode == "today":
        generate_todays_post()
    else:
        batch_generate(args.days)

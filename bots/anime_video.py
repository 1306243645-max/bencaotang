"""本草堂 · 动漫视频生成器

古风小中医角色 + 漫画分镜 + 动画效果 + AI 配音
角色: 「小妙」— 本草堂可爱小中医学徒
"""

import sys, asyncio, math, random
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from edge_tts import Communicate
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, vfx

OUTPUT = Path(__file__).parent.parent / "output" / "anime"
W, H = 1080, 1920

# ── 动漫调色板 ────────────────────────────────────────────

class P:
    """Pastel anime palette"""
    BG_CREAM   = (255, 248, 240)
    BG_WARM    = (255, 242, 230)
    SKIN       = (255, 228, 210)
    CHEEK      = (255, 190, 180)
    HAIR_BROWN = (90, 55, 40)
    EYE_DARK   = (45, 35, 32)
    ROBE_GREEN = (140, 190, 160)
    ROBE_DARK  = (80, 130, 100)
    ACCENT_GOLD = (220, 180, 100)
    TEXT_DARK  = (55, 45, 40)
    TEXT_RED   = (200, 60, 50)
    SPARKLE    = (255, 220, 100)
    SAKURA     = (255, 180, 180)
    BUBBLE     = (255, 255, 252)
    PANEL_BG   = (255, 252, 248)
    SHADOW     = (230, 220, 210)

# ── 字体 ──────────────────────────────────────────────────

FONT_DIR = Path("C:/Windows/Fonts")
_font_cache = {}

def _font(size, bold=False):
    key = (bold, size)
    if key not in _font_cache:
        paths = [FONT_DIR/"msyhbd.ttc", FONT_DIR/"simhei.ttf", FONT_DIR/"msyh.ttc"]
        if not bold: paths = paths[1:]
        for p in paths:
            if p.exists():
                _font_cache[key] = ImageFont.truetype(str(p), size)
                return _font_cache[key]
        _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


# ═══════════════════════════════════════════════════════════
# Chibi Character: 「小妙」— 本草堂小中医
# ═══════════════════════════════════════════════════════════

def draw_chibi(draw, cx, cy, scale=1.0, face="smile", pose="stand"):
    """绘制 Q 版小中医角色。

    Args:
        draw: ImageDraw
        cx, cy: 角色中心坐标
        scale: 缩放
        face: smile / think / wow / explain
        pose: stand / point / hold_herb
    """
    s = scale
    # ── 身体（汉服袍子） ──
    body_top = cy - 40*s
    body_h = 200*s
    # 袍子主体
    draw.polygon([
        (cx-80*s, body_top), (cx+80*s, body_top),
        (cx+100*s, body_top+body_h), (cx-100*s, body_top+body_h),
    ], fill=P.ROBE_GREEN, outline=P.ROBE_DARK)

    # 交领（汉服领口）
    draw.polygon([
        (cx-30*s, body_top-10*s), (cx, body_top+30*s),
        (cx+30*s, body_top-10*s),
    ], fill=P.ROBE_DARK)

    # 腰带
    draw.rectangle([cx-75*s, body_top+80*s, cx+75*s, body_top+95*s], fill=P.ACCENT_GOLD)

    # ── 头 ──
    head_r = 55*s
    head_y = body_top - head_r + 15*s

    # 脸
    draw.ellipse([cx-head_r, head_y, cx+head_r, head_y+head_r*2], fill=P.SKIN, outline=P.SHADOW)

    # 腮红
    cheek_r = 12*s
    draw.ellipse([cx-40*s, head_y+30*s, cx-16*s, head_y+54*s], fill=P.CHEEK)
    draw.ellipse([cx+16*s, head_y+30*s, cx+40*s, head_y+54*s], fill=P.CHEEK)

    # ── 头发 ──
    # 刘海
    hair_top = head_y - 10*s
    draw.arc([cx-60*s, hair_top, cx, hair_top+80*s], 180, 270, fill=P.HAIR_BROWN, width=8)
    draw.arc([cx, hair_top, cx+60*s, hair_top+80*s], 270, 360, fill=P.HAIR_BROWN, width=8)
    # 发髻（丸子头）
    bun_y = hair_top - 20*s
    draw.ellipse([cx-25*s, bun_y-25*s, cx+25*s, bun_y+25*s], fill=P.HAIR_BROWN)
    # 发簪
    draw.line([cx-20*s, bun_y, cx+20*s, bun_y], fill=P.ACCENT_GOLD, width=4)
    draw.ellipse([cx+18*s, bun_y-8*s, cx+30*s, bun_y+8*s], fill=P.ACCENT_GOLD)

    # ── 五官 ──
    eye_y = head_y + 25*s
    # 眉毛
    brow_y = eye_y - 18*s
    if face == "wow":
        draw.arc([cx-35*s, brow_y-5*s, cx-5*s, brow_y+10*s], 0, 180, fill=P.EYE_DARK, width=3)
        draw.arc([cx+5*s, brow_y-5*s, cx+35*s, brow_y+10*s], 0, 180, fill=P.EYE_DARK, width=3)
    else:
        draw.line([cx-35*s, brow_y, cx-10*s, brow_y-3*s], fill=P.EYE_DARK, width=3)
        draw.line([cx+10*s, brow_y-3*s, cx+35*s, brow_y], fill=P.EYE_DARK, width=3)

    # 眼睛
    if face == "smile":
        draw.arc([cx-28*s, eye_y, cx-8*s, eye_y+16*s], 180, 360, fill=P.EYE_DARK, width=3)
        draw.arc([cx+8*s, eye_y, cx+28*s, eye_y+16*s], 180, 360, fill=P.EYE_DARK, width=3)
    elif face == "wow":
        draw.ellipse([cx-30*s, eye_y, cx-5*s, eye_y+22*s], fill=P.EYE_DARK)
        draw.ellipse([cx+5*s, eye_y, cx+30*s, eye_y+22*s], fill=P.EYE_DARK)
    elif face == "think":
        # 一只眼眯着
        draw.arc([cx-28*s, eye_y, cx-8*s, eye_y+16*s], 180, 360, fill=P.EYE_DARK, width=3)
        draw.ellipse([cx+5*s, eye_y, cx+30*s, eye_y+18*s], fill=P.EYE_DARK)
    else:  # explain
        draw.ellipse([cx-28*s, eye_y, cx-8*s, eye_y+18*s], fill=P.EYE_DARK)
        draw.ellipse([cx+8*s, eye_y, cx+28*s, eye_y+18*s], fill=P.EYE_DARK)

    # 嘴巴
    mouth_y = eye_y + 35*s
    if face == "smile":
        draw.arc([cx-12*s, mouth_y-8*s, cx+12*s, mouth_y+12*s], 0, 180, fill=P.TEXT_RED, width=3)
    elif face == "wow":
        draw.ellipse([cx-10*s, mouth_y, cx+10*s, mouth_y+18*s], fill=P.TEXT_RED)
    elif face == "think":
        draw.ellipse([cx-6*s, mouth_y+5*s, cx+6*s, mouth_y+16*s], fill=P.TEXT_RED)
    else:
        draw.line([cx-8*s, mouth_y+8*s, cx+8*s, mouth_y+8*s], fill=P.TEXT_RED, width=3)

    # ── 手 ──
    hand_y = body_top + 50*s
    if pose == "point":
        # 右手指向
        draw.ellipse([cx+80*s, hand_y, cx+130*s, hand_y+30*s], fill=P.SKIN, outline=P.SHADOW)
        draw.line([cx+130*s, hand_y+15*s, cx+160*s, hand_y-20*s], fill=P.SKIN, width=8)
    elif pose == "hold_herb":
        # 双手捧着草药
        draw.ellipse([cx-30*s, hand_y+20*s, cx+30*s, hand_y+50*s], fill=P.SKIN)
        # 草药叶子
        for a in [-30, -10, 10, 30]:
            leaf_x = cx + a
            draw.ellipse([leaf_x-8*s, hand_y-20*s, leaf_x+8*s, hand_y+10*s], fill=(130,180,120))
    else:
        draw.ellipse([cx-70*s, hand_y, cx-40*s, hand_y+30*s], fill=P.SKIN, outline=P.SHADOW)
        draw.ellipse([cx+40*s, hand_y, cx+70*s, hand_y+30*s], fill=P.SKIN, outline=P.SHADOW)

    # ── 腿/鞋 ──
    foot_y = body_top + body_h
    draw.ellipse([cx-40*s, foot_y-15*s, cx-10*s, foot_y+15*s], fill=(50,40,35))
    draw.ellipse([cx+10*s, foot_y-15*s, cx+40*s, foot_y+15*s], fill=(50,40,35))


# ═══════════════════════════════════════════════════════════
# 动漫效果
# ═══════════════════════════════════════════════════════════

def draw_sakura_petals(draw, n=15):
    """樱花花瓣飘落效果"""
    for _ in range(n):
        x = random.randint(0, W)
        y = random.randint(0, H)
        size = random.randint(6, 20)
        alpha = random.randint(60, 180)
        petal_color = (*P.SAKURA, alpha)
        # 简单椭圆花瓣
        draw.ellipse([x-size//2, y-size//4, x+size//2, y+size//4], fill=P.SAKURA)

def draw_sparkles(draw, cx, cy, n=8):
    """闪光星星效果"""
    for i in range(n):
        angle = (i / n) * 2 * math.pi + random.uniform(-0.2, 0.2)
        dist = random.randint(30, 100)
        x = cx + math.cos(angle) * dist
        y = cy + math.sin(angle) * dist
        size = random.randint(4, 12)
        # 四角星
        pts = []
        for j in range(4):
            a = (j / 4) * 2 * math.pi
            pts.append((x + math.cos(a)*size, y + math.sin(a)*size))
            a += math.pi/4
            pts.append((x + math.cos(a)*size*0.3, y + math.sin(a)*size*0.3))
        draw.polygon(pts, fill=P.SPARKLE)

def draw_energy_lines(draw, x1, y1, x2, y2, n=3):
    """动漫速度线"""
    for i in range(n):
        offset = (i - n//2) * 12
        alpha = 200 - abs(offset) * 10
        draw.line([(x1, y1+offset), (x2, y2+offset)], fill=(*P.ACCENT_GOLD, alpha), width=2)

def draw_speech_bubble(draw, x, y, w, h, text, pointing=(0, 0)):
    """漫画对话框"""
    # 气泡主体
    draw.rounded_rectangle([x, y, x+w, y+h], radius=20, fill=P.BUBBLE, outline=P.SHADOW, width=3)
    # 指向三角
    px, py = pointing
    draw.polygon([(x+w//2-15, y+h), (px, py), (x+w//2+15, y+h)], fill=P.BUBBLE, outline=P.SHADOW)

    # 文字
    lines = _wrap(draw, text, _font(36), w-40)
    ty = y + (h - len(lines)*44)//2
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=_font(36))
        tw = bbox[2]-bbox[0]
        draw.text((x+(w-tw)//2, ty), line, fill=P.TEXT_DARK, font=_font(36))
        ty += 44

def _wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if draw.textbbox((0,0), cur+ch, font=font)[2] < max_w:
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur: lines.append(cur)
    return lines

def draw_comic_panel(draw, x, y, w, h, char_pos, face, pose, text, panel_title=""):
    """绘制一个漫画分镜。

    char_pos: (cx, cy) 角色位置
    face: 表情
    pose: 姿势
    text: 对话文字
    """
    # 面板背景
    draw.rounded_rectangle([x, y, x+w, y+h], radius=16, fill=P.PANEL_BG, outline=P.SHADOW, width=3)

    # 标题
    if panel_title:
        draw.text((x+20, y+16), panel_title, fill=P.TEXT_RED, font=_font(28, True))

    # 画角色
    draw_chibi(draw, char_pos[0], char_pos[1], scale=1.1, face=face, pose=pose)

    # 对话框
    bubble_x = char_pos[0] + 80
    bubble_y = y + 40
    bubble_w = min(len(text)*24 + 40, w - (char_pos[0]-x) - 100)
    bubble_h = 80
    draw_speech_bubble(draw, bubble_x, bubble_y, bubble_w, bubble_h, text, (char_pos[0]+30, char_pos[1]-100))


# ═══════════════════════════════════════════════════════════
# 动漫场景创建
# ═══════════════════════════════════════════════════════════

def create_anime_scenes(script: dict) -> list:
    """根据脚本生成动漫场景序列。"""
    title = script.get("title", "")
    body = script.get("body", "")
    paragraphs = [p.strip() for p in body.split("\n") if p.strip()]

    scenes = []
    faces = ["smile", "explain", "think", "wow"]
    poses = ["stand", "point", "hold_herb", "stand"]

    # ── 封面 ──
    cover = Image.new("RGBA", (W, H), P.BG_CREAM)
    d = ImageDraw.Draw(cover)
    # 樱花背景
    draw_sakura_petals(d, 30)
    # 标题框
    d.rounded_rectangle([100, 400, W-100, 700], radius=30, fill=P.BUBBLE, outline=P.ACCENT_GOLD, width=4)
    title_lines = _wrap(d, title, _font(72, True), W-280)
    ty = 460
    for line in title_lines[:3]:
        bbox = d.textbbox((0,0), line, font=_font(72, True))
        tw = bbox[2]-bbox[0]
        d.text(((W-tw)//2, ty), line, fill=P.TEXT_DARK, font=_font(72, True))
        ty += 90
    # 小妙
    draw_chibi(d, W//2, 950, scale=1.5, face="smile", pose="stand")
    draw_sparkles(d, W//2, 850)
    # 副标题
    d.text((W//2, 1150), "本草堂中医诊所 · 动漫科普", fill=P.ACCENT_GOLD, font=_font(38), anchor="mt")
    d.text((W//2, 1220), "微信搜索「本草堂」免费体质自测", fill=P.TEXT_DARK, font=_font(30), anchor="mt")
    scenes.append(cover)

    # ── 内容分镜 ──
    for i, para in enumerate(paragraphs):
        scene = Image.new("RGBA", (W, H), P.BG_WARM)
        d = ImageDraw.Draw(scene)

        # 樱花花瓣
        draw_sakura_petals(d, 12)

        # 顶部装饰条
        d.rounded_rectangle([200, 30, W-200, 46], radius=8, fill=P.ACCENT_GOLD)

        # 标题区
        scene_title = title[:20] if i == 0 else f"知识卡 {i+1}"
        d.text((W//2, 85), scene_title, fill=P.TEXT_RED, font=_font(44, True), anchor="mt")

        # 角色 + 对话框组合
        char_x = 180
        char_y = 700
        face = faces[i % len(faces)]
        pose = poses[i % len(poses)]
        draw_chibi(d, char_x, char_y, scale=1.3, face=face, pose=pose)

        # 对话框
        bubble_x = 380
        bubble_y = 400
        bubble_w = W - 480
        para_lines = _wrap(d, para, _font(38), bubble_w - 60)
        bubble_h = len(para_lines) * 52 + 60
        bubble_h = max(bubble_h, 100)
        draw_speech_bubble(d, bubble_x, bubble_y, bubble_w, bubble_h, para,
                          (char_x+60, char_y-180))

        # 闪光效果（关键信息旁）
        if i % 2 == 0:
            draw_sparkles(d, W-200, 300, 5)

        # 页脚
        d.text((W//2, H-100), f"{i+1}/{len(paragraphs)}  本草堂 · 中医动漫科普", fill=P.SHADOW, font=_font(28), anchor="mt")

        scenes.append(scene)

    # ── 结尾 ──
    end = Image.new("RGBA", (W, H), P.BG_CREAM)
    d = ImageDraw.Draw(end)
    draw_sakura_petals(d, 40)
    draw_chibi(d, W//2, 500, scale=2.0, face="smile", pose="hold_herb")
    draw_sparkles(d, W//2, 300, 12)
    d.text((W//2, 800), "山东本草堂中医诊所", fill=P.TEXT_DARK, font=_font(60, True), anchor="mt")
    d.text((W//2, 900), "本草济世 · 仁心济世", fill=P.ACCENT_GOLD, font=_font(42), anchor="mt")
    cta_items = ["🌐 免费在线问诊", "👅 AI 舌诊分析", "📋 中医体质自测"]
    y = 1020
    for item in cta_items:
        d.text((W//2, y), item, fill=P.TEXT_DARK, font=_font(36), anchor="mt")
        y += 60
    d.text((W//2, 1200), "微信搜索「本草堂」", fill=P.TEXT_RED, font=_font(44, True), anchor="mt")
    d.text((W//2, 1280), "电话: 18254191315", fill=P.SHADOW, font=_font(30), anchor="mt")
    scenes.append(end)

    return scenes


# ═══════════════════════════════════════════════════════════
# TTS 语音 + 视频合成
# ═══════════════════════════════════════════════════════════

async def _tts(text, path):
    """生成语音并返回字幕数据 (word, start_time, end_time)。"""
    c = Communicate(text=text, voice="zh-CN-XiaoxiaoNeural", rate="+3%")
    subs = []
    async for chunk in c.stream():
        if chunk["type"] == "WordBoundary":
            subs.append({
                "text": chunk["text"],
                "start": chunk["offset"] / 1e7,  # 100ns → seconds
                "end": (chunk["offset"] + chunk["duration"]) / 1e7,
            })
    await c.save(path)
    return subs

def run_tts(text, path):
    return asyncio.run(_tts(text, path))

def compose_anime(scenes, audio_path, output_path):
    from moviepy import AudioFileClip, ImageClip, concatenate_videoclips, vfx

    audio = AudioFileClip(audio_path)
    total_dur = audio.duration
    n = len(scenes)
    fade = 0.4

    cover_t = min(5.0, total_dur * 0.2)
    end_t = min(5.0, total_dur * 0.25)
    content_t = max(1.5, (total_dur - cover_t - end_t - fade*(n-2)) / max(n-2, 1))

    time_map = [cover_t] + [content_t] * max(n-2, 1) + [end_t]

    clips = []
    for i, scene in enumerate(scenes):
        dur = time_map[i] if i < len(time_map) else content_t
        arr = np.array(scene.convert("RGB"))
        clip = ImageClip(arr, duration=dur)
        if i > 0:
            clip = clip.with_effects([vfx.FadeIn(fade)])
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    video = video.with_audio(audio)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    video.write_videofile(str(output_path), fps=24, codec="libx264", audio_codec="aac", logger=None)
    video.close()
    audio.close()


# ── 主流程 ────────────────────────────────────────────────

def make_anime(title: str, body: str, output_name: str = None):
    """生成动漫风科普视频。

    Args:
        title: 标题
        body: 正文
        output_name: 文件名
    """
    import time
    if not output_name:
        output_name = f"anime_{int(time.time()*1000)%100000}"

    script = {"title": title, "body": body}
    print(f"🎨 动漫视频: {title}")
    print("   1/3 绘制动漫场景...")
    scenes = create_anime_scenes(script)
    print(f"   ✅ {len(scenes)} 个分镜")

    print("   2/3 生成配音...")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    audio_path = OUTPUT / f"{output_name}.mp3"
    run_tts(body, str(audio_path))
    print("   ✅ 配音完成")

    print("   3/3 合成视频...")
    video_path = OUTPUT / f"{output_name}.mp4"
    compose_anime(scenes, str(audio_path), str(video_path))
    print(f"   ✅ {video_path}")
    return video_path


# ── 批量 ──────────────────────────────────────────────────

BATCH_ANIME = [
    {
        "title": "失眠为什么总在2-3点醒？",
        "body": "熬夜党注意啦！凌晨1到3点是肝经当令时间。如果总在这个点醒来，中医叫肝火扰心。压力大、爱生气、咖啡过量都是元凶。试试菊花茶替代咖啡，睡前按一按脚背上的太冲穴。11点前放下手机，让肝好好休息。想知道你的体质类型吗？来本草堂免费测一测。",
    },
    {
        "title": "秋天干燥咳嗽怎么办？",
        "body": "秋天一到就咳咳咳？这是秋燥伤肺的表现。肺最喜欢润润的，最怕干燥。三样润肺宝贝：雪梨炖冰糖、百合煮粥、银耳红枣汤。少吃辛辣油炸，多喝温水。每天按一按手腕上的太渊穴，效果更好哦。关注本草堂，每天一个中医小知识。",
    },
    {
        "title": "手脚冰凉有妙招",
        "body": "一到冬天手脚像冰块？别担心，阳虚和气郁都可能导致手脚凉。阳虚要温阳，多吃羊肉生姜肉桂。气郁要运动，让气血流通起来。每天泡脚加艾叶和生姜，暖暖的好舒服。想知道你是哪种体质？来本草堂免费自测。",
    },
    {
        "title": "每天学一个穴位：足三里",
        "body": "足三里是脾胃第一保健大穴。位置很好找，膝盖外侧凹陷下四指宽，小腿骨外侧一指宽处。每天按揉五分钟，健脾养胃、补气血、强体质。坚持一个月，你会发现胃口好了、人也有精神了。关注本草堂，带你认识更多养生穴位。",
    },
    {
        "title": "枸杞的正确打开方式",
        "body": "枸杞几乎人人都在吃，但90%的人吃错了。开水泡枸杞会破坏营养，正确方法是温水泡或者直接嚼着吃。每天15到30粒就够啦，吃多了反而上火。枸杞配菊花养肝明目，配红枣补气血，配山药健脾胃。来本草堂测测体质，看看你适不适合吃枸杞。",
    },
]

def batch_anime():
    print("=" * 60)
    print("🎨 本草堂 · 动漫科普视频批量生成")
    print("=" * 60)
    for i, s in enumerate(BATCH_ANIME, 1):
        print(f"\n[{i}/{len(BATCH_ANIME)}]")
        try:
            make_anime(s["title"], s["body"])
        except Exception as e:
            print(f"   ❌ {e}")
    print(f"\n✅ 完成 → {OUTPUT}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("-t","--title")
    p.add_argument("-b","--body")
    p.add_argument("--batch", action="store_true")
    args = p.parse_args()

    if args.batch:
        batch_anime()
    elif args.title and args.body:
        make_anime(args.title, args.body)
    else:
        print("用法: python bots/anime_video.py -t '标题' -b '正文'")
        print("批量: python bots/anime_video.py --batch")

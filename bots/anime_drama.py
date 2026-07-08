"""本草堂 · 中医文化动画短剧生成器

生成故事化中医科普视频短剧：
- 每集60-90秒
- 妙妙主角+师父
- 中医知识+传统文化
- 动漫风格+配音
"""

import sys, asyncio, math, random, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from edge_tts import Communicate
from datetime import datetime

OUT = Path(__file__).parent.parent / "output" / "drama"
W, H = 720, 1280
FD = Path("C:/Windows/Fonts")

# ═══════════ 场景配置 ═══════════
SCENES = {
    "temple": {"bg": (240, 225, 200), "name": "古寺"},
    "garden": {"bg": (200, 230, 200), "name": "药园"},
    "night":  {"bg": (30, 30, 60), "name": "月夜"},
    "market": {"bg": (255, 240, 220), "name": "市集"},
}

def ff(size, bold=False):
    for p in sorted(FD.glob("*.tt*"), key=lambda x: x.name):
        if bold and 'bold' in p.name.lower(): return ImageFont.truetype(str(p), size)
    for p in [FD/"simhei.ttf", FD/"msyh.ttc"]:
        if p.exists(): return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

# ═══════════ 绘制妙妙猫 ═══════════
def draw_panda(d, cx, cy, scale=1.0, pose="stand", face="smile"):
    s = scale
    body_y = cy - 30*s
    # 身体-白色椭圆
    d.ellipse([cx-50*s, body_y+25, cx+50*s, body_y+165*s], fill=(250,248,245))
    d.ellipse([cx-48*s, body_y+30, cx+48*s, body_y+155*s], fill=(255,252,250))
    # 大圆头
    head_r = 58*s
    head_y = cy - head_r - 25*s
    d.ellipse([cx-head_r, head_y, cx+head_r, head_y+head_r*2], fill=(255,253,250))
    # 三角形耳朵
    d.polygon([(cx-50*s, head_y+25), (cx-70*s, head_y-30), (cx-35*s, head_y+5)], fill=(255,248,245))
    d.polygon([(cx-52*s, head_y+18), (cx-65*s, head_y-18), (cx-40*s, head_y+5)], fill=(255,210,210))
    d.polygon([(cx+50*s, head_y+25), (cx+70*s, head_y-30), (cx+35*s, head_y+5)], fill=(255,248,245))
    d.polygon([(cx+52*s, head_y+18), (cx+65*s, head_y-18), (cx+40*s, head_y+5)], fill=(255,210,210))
    # 大圆眼
    eye_y = head_y + 25*s
    for ex in [cx-22*s, cx+22*s]:
        d.ellipse([ex-20*s, eye_y-14*s, ex+20*s, eye_y+14*s], fill=(255,255,255), outline=(180,200,220), width=int(2*s))
        d.ellipse([ex-11*s, eye_y-7*s, ex+11*s, eye_y+7*s], fill=(100,180,220))
        d.ellipse([ex-4*s, eye_y-3*s, ex+4*s, eye_y+3*s], fill=(20,40,60))
        d.ellipse([ex-8*s, eye_y-7*s, ex-5*s, eye_y-6*s], fill=(255,255,255))
    # 粉色小三角鼻
    d.polygon([(cx-4*s, eye_y+8*s), (cx+4*s, eye_y+8*s), (cx, eye_y+14*s)], fill=(255,180,180))
    # 小嘴
    d.arc([cx-6*s, eye_y+14*s, cx, eye_y+24*s], 0, 180, fill=(220,180,180), width=int(2*s))
    d.arc([cx, eye_y+14*s, cx+6*s, eye_y+24*s], 0, 180, fill=(220,180,180), width=int(2*s))
    # 粉色腮红
    for bx in [cx-50*s, cx+50*s]:
        d.ellipse([bx-14*s, eye_y+6*s, bx+14*s, eye_y+20*s], fill=(255,200,200,int(80*s)))
    # 胡须
    for side in [-1, 1]:
        bx = cx + side*30*s
        for i in range(3):
            dy = eye_y+12*s + i*6*s
            d.line([(bx, dy), (bx+side*35*s, dy-3)], fill=(220,220,230), width=2)
    # 小爪子
    hand_y = body_y + 50*s
    d.ellipse([cx-35*s, hand_y, cx-10*s, hand_y+28*s], fill=(255,252,250))
    d.ellipse([cx+10*s, hand_y, cx+35*s, hand_y+28*s], fill=(255,252,250))
    # 粉色肉垫
    for px in [cx-22*s, cx+22*s]:
        d.ellipse([px-5*s, hand_y+10*s, px+5*s, hand_y+20*s], fill=(255,200,200,int(120*s)))

# ═══════════ 绘制师父 ═══════════
def draw_master(d, cx, cy, scale=1.0):
    s = scale
    body_y = cy - 60*s
    d.ellipse([cx-80*s, body_y, cx+80*s, body_y+180*s], fill=(160, 50, 40))
    d.ellipse([cx-70*s, body_y+15, cx+70*s, body_y+160*s], fill=(180, 60, 50))
    # 白胡子
    d.ellipse([cx-30*s, cy-70*s, cx+30*s, cy+10*s], fill=(255, 220, 190))
    # 白眉
    d.line([(cx-35*s, cy-85*s), (cx-15*s, cy-75*s)], fill=(240, 240, 240), width=4)
    d.line([(cx+15*s, cy-75*s), (cx+35*s, cy-85*s)], fill=(240, 240, 240), width=4)
    # 眼睛——慈祥
    d.arc([cx-25*s, cy-60*s, cx-5*s, cy-45*s], 180, 360, fill=(60, 40, 30), width=3)
    d.arc([cx+5*s, cy-60*s, cx+25*s, cy-45*s], 180, 360, fill=(60, 40, 30), width=3)
    # 手杖
    d.line([(cx+70*s, body_y+30), (cx+90*s, body_y+170)], fill=(120, 80, 50), width=5)
    d.ellipse([cx+85*s, body_y+20, cx+95*s, body_y+40], fill=(180, 130, 80))

# ═══════════ 场景创建 ═══════════
def create_scene(scene_type, title, dialogue, speaker="妙妙"):
    img = Image.new("RGBA", (W, H), SCENES.get(scene_type, SCENES["temple"])["bg"])
    d = ImageDraw.Draw(img)

    # 顶部标题栏
    d.rectangle([0, 0, W, 120], fill=(30, 20, 10, 180))
    f_title = ff(42, True)
    d.text((W//2, 60), f"第{title}集", fill=(220, 200, 160), font=f_title, anchor="mm")

    # 角色
    if speaker == "师父":
        draw_master(d, W//2, 750, 0.9)
    else:
        draw_panda(d, W//2-50, 750, 0.9, "stand", "smile")

    # 对话框——漫画风
    lines = _wrap(d, dialogue, ff(36), W-240)
    bubble_h = len(lines) * 52 + 80
    bubble_y = 1050 - bubble_h//2
    d.rounded_rectangle([100, bubble_y, W-100, bubble_y+bubble_h], radius=20,
                       fill=(255, 255, 250), outline=(180, 160, 140), width=3)
    # 三角
    d.polygon([(W//2-15, bubble_y+bubble_h), (W//2, bubble_y+bubble_h+30), (W//2+15, bubble_y+bubble_h)], fill=(255, 255, 250))

    ty = bubble_y + 40
    for line in lines:
        bbox = d.textbbox((0,0), line, font=ff(36))
        tw = bbox[2]-bbox[0]
        d.text(((W-tw)//2, ty), line, fill=(40, 30, 20), font=ff(36))
        ty += 52

    # 装饰——花瓣
    for _ in range(8):
        x = random.randint(100, W-100)
        y = random.randint(200, 900)
        d.ellipse([x-3, y-5, x+3, y+5], fill=(255, 200, 180, 80))

    # 底部
    d.rectangle([0, H-80, W, H], fill=(30, 20, 10, 200))
    d.text((W//2, H-45), "本草堂 · 妙妙中医短剧", fill=(200, 180, 150), font=ff(28), anchor="mm")

    return img


def _wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if draw.textbbox((0,0), cur+ch, font=font)[2] < max_w: cur += ch
        else: lines.append(cur); cur = ch
    if cur: lines.append(cur)
    return lines


# ═══════════ 剧本库 ═══════════
SCRIPTS = [
    {
        "title": "失眠的秘密",
        "scenes": [
            ("night", "月夜难眠", "师父，我晚上总是睡不着，脑子里像放电影一样。这是为什么呢？", "妙妙"),
            ("temple", "师父解惑", "肝藏魂，心藏神。白天想太多，肝火烧到心，自然睡不着。来，泡杯菊花茶，让肝冷静下来。", "师父"),
            ("garden", "学以致用", "原来是这样！那我每天睡前喝菊花茶，不刷手机，肝火降下来，就能睡个好觉了！", "妙妙"),
        ]
    },
    {
        "title": "脾胃的诉说",
        "scenes": [
            ("market", "贪吃的妙妙", "师父，我刚吃了三碗冰粉、两串烧烤，现在肚子好胀啊！", "妙妙"),
            ("temple", "师父训诫", "脾喜燥恶湿，胃喜温恶寒。你这一肚子冰冷油腻，脾胃怎么受得了？去煮碗生姜陈皮水！", "师父"),
            ("garden", "妙妙觉悟", "以后不吃冰的了！师父说脾胃是后天之本，气血生化之源，我得好好养着～", "妙妙"),
        ]
    },
    {
        "title": "五运六气的奥秘",
        "scenes": [
            ("temple", "仰望星空", "师父，为什么同样的方子，不同年份效果不一样呢？", "妙妙"),
            ("night", "师父讲道", "天有五行御五位，人有五脏应五运。每年运气不同，天地之气在变，治病也要顺天应时。这就是五运六气。", "师父"),
            ("garden", "融会贯通", "原来天地人是一体的！2026水运太过，寒气偏重，怪不得师父今年多加生姜和肉桂！", "妙妙"),
        ]
    },
    {
        "title": "茶中有道",
        "scenes": [
            ("garden", "采药", "师父，您为什么每天喝的茶都不一样呢？", "妙妙"),
            ("temple", "茶即药也", "春天升发喝花茶，夏天清热喝绿茶，秋天润燥喝白茶，冬天温补喝红茶。茶即是药，对症才有效。", "师父"),
            ("market", "妙妙卖茶", "本草堂五运六气体质茶，一人一方，春喝花，夏喝绿，秋喝白，冬喝红。扫描海报二维码免费测体质～", "妙妙"),
        ]
    },
    {
        "title": "经脉的秘密",
        "scenes": [
            ("night", "妙妙好奇", "师父师父，您说人体有经络，可我怎么看不见呢？", "妙妙"),
            ("temple", "师父点穴", "你按一下脚背上的太冲穴。疼不疼？这就是肝经在说话。经脉虽看不见，但就像河道，堵了就会痛。", "师父"),
            ("garden", "顿悟", "通则不痛，痛则不通！每天按揉经络，就像给身体里的河道做清理！", "妙妙"),
        ]
    },
]


# ═══════════ TTS + 视频合成 ═══════════
async def tts(text, path):
    c = Communicate(text=text, voice="zh-CN-XiaoxiaoNeural", rate="+5%")
    await c.save(path)

def gen_audio(text, path):
    asyncio.run(tts(text, path))

def make_drama(script_index=0):
    script = SCRIPTS[script_index % len(SCRIPTS)]
    print(f"🎬 动画短剧: {script['title']}")
    OUT.mkdir(parents=True, exist_ok=True)

    scenes = []
    full_text = ""
    for i, (scene_type, title, dialogue, speaker) in enumerate(script["scenes"]):
        print(f"  场景{i+1}: {title}")
        full_text += dialogue + " "
        scenes.append(create_scene(scene_type, f"{script['title']}·{title}", dialogue, speaker))

    # 生成配音
    name = f"drama_{script['title'].replace(' ','_')}"
    audio_path = OUT / f"{name}.mp3"
    print(f"  配音: {name}")
    gen_audio(full_text[:500], str(audio_path))  # 限制长度

    # 合成视频
    from moviepy import AudioFileClip, ImageClip, concatenate_videoclips, vfx
    audio = AudioFileClip(str(audio_path))
    dur = audio.duration
    per_scene = dur / len(scenes)

    clips = []
    for scene in scenes:
        arr = np.array(scene.convert("RGB"))
        clip = ImageClip(arr, duration=per_scene)
        clips.append(clip)

    video = concatenate_videoclips(clips, method="chain").with_audio(audio)
    video_path = OUT / f"{name}.mp4"
    video.write_videofile(str(video_path), fps=12, codec="libx264", audio_codec="aac", logger=None)
    print(f"✅ {video_path}")
    return video_path


def batch_drama():
    print("=" * 55)
    print("  🎬 本草堂 · 中医文化动画短剧批量生成")
    print("=" * 55)
    for i in range(len(SCRIPTS)):
        try: make_drama(i)
        except Exception as e: print(f"  ❌ 第{i+1}集: {e}")
    print(f"\n✅ 全部完成 → {OUT}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--batch", action="store_true", help="批量生成全部5集")
    p.add_argument("--episode", type=int, default=0, help="生成第N集(0-4)")
    args = p.parse_args()
    if args.batch: batch_drama()
    else: make_drama(args.episode)

"""妙手堂 · 分享海报生成器 — 生成精美宣传海报供社交分享"""

import sys, io, base64
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

import qrcode
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

OUTPUT = Path(__file__).parent.parent / "output" / "posters"
W, H = 1080, 1920
FONT_DIR = Path("C:/Windows/Fonts")

def _font(size, bold=False):
    paths = [FONT_DIR/"msyhbd.ttc", FONT_DIR/"simhei.ttf", FONT_DIR/"msyh.ttc"]
    if not bold: paths = paths[1:]
    for p in paths:
        if p.exists(): return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

def create_poster(url: str, title: str = "山东妙手堂中医诊所",
                  subtitle: str = "本草济世 · 仁心济世",
                  cta: str = "扫码免费体验 AI 舌诊 + 体质自测",
                  output_name: str = None):
    """生成一张分享海报。

    Args:
        url: 二维码链接
        title: 主标题
        subtitle: 副标题
        cta: 行动号召
        output_name: 文件名
    """
    img = Image.new("RGBA", (W, H), (255, 248, 240))
    d = ImageDraw.Draw(img)

    # 顶部渐变背景
    for y in range(600):
        r = int(45 + y * 0.02)
        g = int(90 + y * 0.02)
        b = int(60 + y * 0.02)
        d.line([(0,y), (W,y)], fill=(r,g,b))

    # 装饰圆环
    d.ellipse([W//2-160, 80, W//2+160, 400], outline=(255,255,255,60), width=3)
    d.ellipse([W//2-120, 120, W//2+120, 360], outline=(255,255,255,40), width=2)

    # Logo 圆
    d.ellipse([W//2-80, 140, W//2+80, 300], fill=(82, 183, 136))
    d.text((W//2, 220), "妙手堂", fill="white", font=_font(38, True), anchor="mm")

    # 标题
    f_title = _font(68, True)
    lines = _wrap(d, title, f_title, W-160)
    y = 450
    for line in lines[:3]:
        bbox = d.textbbox((0,0), line, font=f_title)
        tw = bbox[2]-bbox[0]
        d.text(((W-tw)//2 + 3, y+3), line, fill=(0,0,0,40), font=f_title)
        d.text(((W-tw)//2, y), line, fill=(45,90,60), font=f_title)
        y += 90

    # 副标题
    f_sub = _font(42)
    d.text((W//2, y+20), subtitle, fill=(82,183,136), font=f_sub, anchor="mt")

    # 特色列表
    features = [
        "🌿 三代中医传承，正宗中医诊疗",
        "🤖 AI 舌诊分析，秒出体质报告",
        "📋 九种体质自测，精准养生指导",
        "🍲 30道食疗食谱，用身边食材调理",
        "💆 穴位按摩指导，在家就能做",
        "📞 18254191315 · 微信同号",
    ]
    f_feat = _font(38)
    y = 650
    for feat in features:
        d.text((200, y), feat, fill=(60,50,40), font=f_feat)
        y += 65

    # 二维码区域
    qr_size = 320
    qr_x = (W - qr_size) // 2
    qr_y = 1150

    # 白色背景
    d.rounded_rectangle([qr_x-30, qr_y-30, qr_x+qr_size+30, qr_y+qr_size+30],
                        radius=20, fill=(255,255,255), outline=(82,183,136), width=3)

    qr_content = url  # 妙手堂网站链接
    qr = qrcode.make(qr_content)
    qr_img = qr.resize((qr_size, qr_size))
    img.paste(qr_img, (qr_x, qr_y))

    # CTA
    f_cta = _font(34)
    d.text((W//2, qr_y+qr_size+60), cta, fill=(82,183,136), font=f_cta, anchor="mt")

    # 底部
    d.text((W//2, H-100), f"山东妙手堂中医诊所 · {datetime.now().year}", fill=(180,170,155), font=_font(26), anchor="mt")

    # 保存
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if not output_name:
        output_name = f"poster_{datetime.now().strftime('%Y%m%d_%H%M')}"
    path = OUTPUT / f"{output_name}.png"
    img.save(str(path))
    print(f"✅ 海报已生成: {path}")
    return path

def _wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if draw.textbbox((0,0), cur+ch, font=font)[2] < max_w:
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur: lines.append(cur)
    return lines

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://172.20.21.34:8501")
    p.add_argument("--title", default="山东妙手堂中医诊所")
    p.add_argument("--subtitle", default="本草济世 · 仁心济世")
    p.add_argument("--cta", default="扫码免费体验 AI 舌诊 + 体质自测")
    args = p.parse_args()
    create_poster(args.url, args.title, args.subtitle, args.cta)

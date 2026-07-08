"""本草堂 · 宋式美学海报"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import qrcode, sys
from datetime import datetime
sys.stdout.reconfigure(encoding="utf-8")

OUT = Path(__file__).parent.parent / "output" / "posters"
W, H = 1080, 1920
FD = Path("C:/Windows/Fonts")

def ff(size, bold=False):
    for p in sorted(FD.glob("*.tt*"), key=lambda x: x.name):
        if bold and 'bold' in p.name.lower():
            return ImageFont.truetype(str(p), size)
    for p in [FD/"simhei.ttf", FD/"msyh.ttc"]:
        if p.exists(): return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()

def create(url: str):
    OUT.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (W, H), (240, 235, 248))
    d = ImageDraw.Draw(img)

    # ═══ 淡雅背景——紫雾渐变 ═══
    for y in range(H):
        r = int(245 - y * 0.006)
        g = int(242 - y * 0.008)
        b = int(250 - y * 0.004)
        d.line([(0, y), (W, y)], fill=(max(210,r), max(200,g), max(225,b)))

    # ═══ 极简装饰——细线 ═══
    # 顶部留白区
    d.line([(180, 200), (W-180, 200)], fill=(130, 100, 180), width=1)
    d.line([(220, 210), (W-220, 210)], fill=(140, 110, 190, 150), width=1)

    # ═══ 标题——宋体清雅 ═══
    f_title = ff(80, True)
    title = "本 草 堂"
    bb = d.textbbox((0, 0), title, font=f_title)
    tw = bb[2] - bb[0]
    d.text(((W-tw)//2, 280), title, fill=(55, 35, 95), font=f_title)

    # ═══ 副标题——淡墨 ═══
    f_sub = ff(36)
    d.text((W//2, 370), "本 草 济 世  ·  仁 心 济 世", fill=(110, 80, 160), font=f_sub, anchor="mm")

    # ═══ 英文 ═══
    f_en = ff(22)
    d.text((W//2, 415), "BEN CAO TANG  ·  SINCE 1980s", fill=(130, 100, 185), font=f_en, anchor="mm")

    # ═══ 印章 ═══
    seal_x, seal_y = W - 250, 80
    d.rounded_rectangle([seal_x, seal_y, seal_x+140, seal_y+140], radius=8,
                       outline=(200, 120, 120), width=2)
    d.text((seal_x+70, seal_y+50), "本草堂", fill=(200, 120, 120), font=ff(30, True), anchor="mm")
    d.text((seal_x+70, seal_y+95), "中医世家", fill=(200, 120, 120), font=ff(18), anchor="mm")

    # ═══ 六大服务卡片——宋式素雅 ═══
    svcs = [
        ("AI 问诊", "智能辨证 · 个性化方案"),
        ("舌诊 · 面诊", "五行面型 · 五色辨证"),
        ("一人一茶", "五运六气 · 专属茶方"),
        ("体质测试", "免费自测 · 精准辨识"),
        ("民间偏方", "36个家传食疗小方"),
    ]

    card_start_y = 540
    card_w = 440
    card_h = 130
    gap_x = 40
    gap_y = 30
    left_m = (W - 2*card_w - gap_x) // 2

    for i, (title, desc) in enumerate(svcs):
        col = i % 2
        row = i // 2
        if i == 4:  # 最后一个居中
            col, row = 0, 2
            x = (W - card_w) // 2
        else:
            x = left_m + col * (card_w + gap_x)
        y = card_start_y + row * (card_h + gap_y)

        # 卡片底板
        d.rounded_rectangle([x, y, x+card_w, y+card_h], radius=12,
                           fill=(238, 232, 250), outline=(145, 115, 190), width=2)

        # 序号圆形
        d.ellipse([x+35, y+25, x+85, y+75], fill=(100, 60, 160))
        d.text((x+60, y+50), f"0{i+1}", fill=(255, 250, 250), font=ff(32, True), anchor="mm")

        # 标题
        d.text((x+110, y+40), title, fill=(45, 25, 80), font=ff(34, True), anchor="lm")

        # 描述
        d.text((x+110, y+75), desc, fill=(130, 110, 170), font=ff(24), anchor="lm")

        # 底部装饰线
        d.line([(x+100, y+105), (x+card_w-40, y+105)], fill=(145, 115, 190, 120), width=1)

    # ═══ 名句 ═══
    quote_y = card_start_y + 3 * (card_h + gap_y) + 60
    f_quote = ff(30)
    d.text((W//2, quote_y), "「上医治未病」", fill=(110, 80, 160), font=f_quote, anchor="mm")
    f_src = ff(22)
    d.text((W//2, quote_y+45), "——《黄帝内经》", fill=(140, 120, 190), font=f_src, anchor="mm")

    # ═══ 网址展示 ═══
    url_y = quote_y + 130
    f_cta = ff(32, True)
    d.text((W//2, url_y), "访 问 网 站", fill=(45, 25, 80), font=f_cta, anchor="mm")

    # 域名框
    d.rounded_rectangle([140, url_y+35, W-140, url_y+155], radius=14,
                       fill=(248, 246, 252), outline=(155, 142, 196), width=3)
    f_domain = ff(38, True)
    d.text((W//2, url_y+70), "本草堂.icu", fill=(60, 40, 100), font=f_domain, anchor="mm")
    f_url = ff(26)
    d.text((W//2, url_y+108), "bore.pub:21672", fill=(140, 125, 165), font=f_url, anchor="mm")
    d.text((W//2, url_y+138), "微信浏览器直接打开", fill=(160, 150, 175), font=ff(22), anchor="mm")

    # ═══ 底部 ═══
    bot_y = url_y + 240
    d.line([(120, bot_y), (W-120, bot_y)], fill=(140, 110, 190), width=1)
    d.text((W//2, bot_y+45), "山东本草堂中医诊所", fill=(50, 25, 90), font=ff(32, True), anchor="mm")
    d.text((W//2, bot_y+95), "三代传承 · 正宗中医   |   微信搜「本草堂」", fill=(110, 80, 160), font=ff(24), anchor="mm")

    # ═══ 底部极简装饰 ═══
    y = bot_y + 140
    for i in range(2):
        d.line([(W//2-80, y+i*6), (W//2+80, y+i*6)], fill=(140, 110, 190, 100-i*50), width=2-i)

    path = OUT / f"poster_song_{datetime.now():%Y%m%d_%H%M}.png"
    img.save(str(path))
    # 同时保存到桌面
    desktop = Path.home() / "Desktop" / f"本草堂海报_{datetime.now():%Y%m%d_%H%M}.png"
    img.save(str(desktop))
    print(f"✅ 项目: {path}")
    print(f"✅ 桌面: {desktop}")
    return path

if __name__ == "__main__":
    u = sys.argv[1] if len(sys.argv) > 1 else "https://legal-eels-find.loca.lt"
    create(u)

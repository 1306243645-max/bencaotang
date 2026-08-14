"""妙手堂 · 视频剪辑工具

功能：加字幕 / 加背景音乐 / 裁剪 / 合并 / 加文字水印 / 封面

使用：
    python bots/video_editor.py --help
    python bots/video_editor.py add-subtitle -i input.mp4 -t "字幕文本"
    python bots/video_editor.py add-music -i input.mp4 -m music.mp3
    python bots/video_editor.py trim -i input.mp4 --start 2 --end 30
    python bots/video_editor.py merge -i vid1.mp4 vid2.mp4 -o merged.mp4
    python bots/video_editor.py add-watermark -i input.mp4 -w "妙手堂"
"""

import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoFileClip, AudioFileClip, concatenate_videoclips,
    TextClip, CompositeVideoClip, vfx, ColorClip,
)

OUTPUT_DIR = Path(__file__).parent.parent / "output" / "edited"
W, H = 1080, 1920

FONT = None
for f in [Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/simhei.ttf")]:
    if f.exists():
        FONT = str(f)
        break


# ═══════════════════════════════════════════════════════════
# 字幕工具
# ═══════════════════════════════════════════════════════════

def add_subtitle(input_path: str, text: str, output_path: str = None):
    """在视频底部添加字幕。

    Args:
        input_path: 输入视频路径
        text: 字幕文本（可用 | 分隔每段字幕）
        output_path: 输出路径
    """
    video = VideoFileClip(input_path)
    segments = [s.strip() for s in text.split("|") if s.strip()]
    seg_dur = video.duration / max(len(segments), 1)

    clips = []
    for i, seg in enumerate(segments):
        # 字幕背景条
        txt_clip = TextClip(
            text=seg, font=FONT or "Arial", font_size=38,
            color="white", stroke_color="black", stroke_width=2,
            method="label", text_align="center",
        )
        bar = ColorClip(
            size=(int(txt_clip.w + 80), int(txt_clip.h + 40)),
            color=(0, 0, 0, 128),
        )
        txt_on_bar = CompositeVideoClip([
            bar.with_position("center"),
            txt_clip.with_position("center"),
        ], size=(txt_clip.w + 80, txt_clip.h + 40))

        subclip = video.subclipped(i * seg_dur, min((i + 1) * seg_dur, video.duration))
        final = CompositeVideoClip([
            subclip,
            txt_on_bar.with_position(("center", H - 200)),
        ]).with_duration(seg_dur)

        clips.append(final)

    result = concatenate_videoclips(clips, method="compose")
    result = result.with_audio(video.audio)

    out = output_path or _out(input_path, "_subbed")
    result.write_videofile(out, fps=24, codec="libx264", audio_codec="aac", logger=None)
    result.close(); video.close()
    return out


# ═══════════════════════════════════════════════════════════
# 背景音乐
# ═══════════════════════════════════════════════════════════

def add_music(input_path: str, music_path: str, volume: float = 0.3, output_path: str = None):
    """添加背景音乐。

    Args:
        input_path: 输入视频
        music_path: 背景音乐文件
        volume: 音乐音量 (0~1)
        output_path: 输出路径
    """
    video = VideoFileClip(input_path)
    music = AudioFileClip(music_path)

    # 循环音乐到视频长度
    if music.duration < video.duration:
        repeats = int(video.duration / music.duration) + 1
        music = concatenate_videoclips([ColorClip((1,1)).with_audio(music)] * repeats).audio
    music = music.subclipped(0, video.duration)

    # 混音
    mixed = video.audio.with_effects([lambda a: a * (1 - volume)]) + music.with_effects([lambda a: a * volume])
    result = video.with_audio(mixed)

    out = output_path or _out(input_path, "_music")
    result.write_videofile(out, fps=24, codec="libx264", audio_codec="aac", logger=None)
    result.close(); video.close()
    return out


# ═══════════════════════════════════════════════════════════
# 裁剪
# ═══════════════════════════════════════════════════════════

def trim(input_path: str, start: float = 0, end: float = None, output_path: str = None):
    """裁剪视频片段。

    Args:
        input_path: 输入视频
        start: 开始时间（秒）
        end: 结束时间（秒），不指定则到结尾
    """
    video = VideoFileClip(input_path)
    end = end or video.duration
    result = video.subclipped(start, min(end, video.duration))

    out = output_path or _out(input_path, "_trimmed")
    result.write_videofile(out, fps=24, codec="libx264", audio_codec="aac", logger=None)
    result.close(); video.close()
    return out


# ═══════════════════════════════════════════════════════════
# 合并
# ═══════════════════════════════════════════════════════════

def merge(input_paths: list, output_path: str = None):
    """合并多个视频。

    Args:
        input_paths: 输入视频路径列表
        output_path: 输出路径
    """
    clips = [VideoFileClip(p) for p in input_paths]
    result = concatenate_videoclips(clips, method="compose")

    out = output_path or _out("merged", "_merged")
    result.write_videofile(out, fps=24, codec="libx264", audio_codec="aac", logger=None)
    for c in clips: c.close()
    result.close()
    return out


# ═══════════════════════════════════════════════════════════
# 水印
# ═══════════════════════════════════════════════════════════

def add_watermark(input_path: str, text: str = "妙手堂", output_path: str = None):
    """在视频右上角添加文字水印。

    Args:
        input_path: 输入视频
        text: 水印文字
        output_path: 输出路径
    """
    video = VideoFileClip(input_path)

    wm = TextClip(
        text=f"  {text}  ",
        font=FONT or "Arial",
        font_size=36,
        color=(255, 215, 0, 180),
        stroke_color=(0, 0, 0, 100),
        stroke_width=1,
        method="label",
    ).with_duration(video.duration).with_position((W - 260, 40))

    result = CompositeVideoClip([video, wm])

    out = output_path or _out(input_path, "_watermarked")
    result.write_videofile(out, fps=24, codec="libx264", audio_codec="aac", logger=None)
    result.close(); video.close()
    return out


# ═══════════════════════════════════════════════════════════
# 一键美化（字幕+音乐+水印）
# ═══════════════════════════════════════════════════════════

def enhance(input_path: str, subtitle_text: str, music_path: str = None,
            watermark: str = "妙手堂", output_path: str = None):
    """一键美化：加字幕 + 水印 + 可选背景音乐。

    Args:
        input_path: 输入视频
        subtitle_text: 字幕文本（用 | 分隔）
        music_path: 背景音乐路径（可选）
        watermark: 水印文字
        output_path: 输出路径
    """
    print(f"🎬 一键美化: {input_path}")
    tmp = input_path

    # 1. 加字幕
    print("   1/3 添加字幕...")
    tmp = add_subtitle(tmp, subtitle_text, _tmp("sub"))
    print(f"   ✅ 字幕完成")

    # 2. 加音乐
    if music_path and Path(music_path).exists():
        print("   2/3 添加背景音乐...")
        tmp = add_music(tmp, music_path, volume=0.25, output_path=_tmp("music"))
        print(f"   ✅ 音乐完成")

    # 3. 加水印
    print("   {}/3 添加水印...".format("3" if music_path else "2"))
    out = output_path or _out(input_path, "_enhanced")
    add_watermark(tmp, watermark, out)
    print(f"   ✅ 水印完成")

    # 清理临时文件
    if tmp != input_path and Path(tmp).exists():
        Path(tmp).unlink()

    print(f"\n✅ 最终输出: {out}")
    return out


# ── 辅助 ──────────────────────────────────────────────────

def _out(input_path: str, suffix: str) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    name = Path(input_path).stem
    return str(OUTPUT_DIR / f"{name}{suffix}.mp4")

def _tmp(tag: str) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    import time
    return str(OUTPUT_DIR / f"_tmp_{tag}_{int(time.time()*1000)%100000}.mp4")


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="妙手堂 · 视频剪辑工具")
    sp = p.add_subparsers(dest="cmd")

    # 加字幕
    p1 = sp.add_parser("add-subtitle")
    p1.add_argument("-i", required=True)
    p1.add_argument("-t", "--text", required=True, help="字幕文本，用 | 分隔段落")
    p1.add_argument("-o", "--output")

    # 加音乐
    p2 = sp.add_parser("add-music")
    p2.add_argument("-i", required=True)
    p2.add_argument("-m", "--music", required=True)
    p2.add_argument("--volume", type=float, default=0.3)
    p2.add_argument("-o", "--output")

    # 裁剪
    p3 = sp.add_parser("trim")
    p3.add_argument("-i", required=True)
    p3.add_argument("--start", type=float, default=0)
    p3.add_argument("--end", type=float)
    p3.add_argument("-o", "--output")

    # 合并
    p4 = sp.add_parser("merge")
    p4.add_argument("-i", nargs="+", required=True)
    p4.add_argument("-o", "--output")

    # 水印
    p5 = sp.add_parser("add-watermark")
    p5.add_argument("-i", required=True)
    p5.add_argument("-w", "--watermark", default="妙手堂")
    p5.add_argument("-o", "--output")

    # 一键美化
    p6 = sp.add_parser("enhance")
    p6.add_argument("-i", required=True)
    p6.add_argument("-t", "--text", required=True)
    p6.add_argument("-m", "--music")
    p6.add_argument("-w", "--watermark", default="妙手堂")
    p6.add_argument("-o", "--output")

    args = p.parse_args()

    if args.cmd == "add-subtitle":
        print(f"✅ {add_subtitle(args.i, args.text, args.output)}")
    elif args.cmd == "add-music":
        print(f"✅ {add_music(args.i, args.music, args.volume, args.output)}")
    elif args.cmd == "trim":
        print(f"✅ {trim(args.i, args.start, args.end, args.output)}")
    elif args.cmd == "merge":
        print(f"✅ {merge(args.i, args.output)}")
    elif args.cmd == "add-watermark":
        print(f"✅ {add_watermark(args.i, args.watermark, args.output)}")
    elif args.cmd == "enhance":
        print(f"✅ {enhance(args.i, args.text, args.music, args.watermark, args.output)}")
    else:
        p.print_help()

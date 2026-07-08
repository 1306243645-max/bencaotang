"""文件操作工具。"""

from pathlib import Path


def read_file(path: str) -> str:
    """读取文件内容。"""
    return Path(path).read_text(encoding="utf-8")


def write_file(path: str, content: str) -> None:
    """写入文件内容。"""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

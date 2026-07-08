"""联网搜索工具 — 基于 DuckDuckGo (ddgs)，带容错。"""

from ddgs import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    """搜索网络并返回格式化结果。

    Args:
        query: 搜索关键词
        max_results: 最大返回数量 (默认 5)

    Returns:
        格式化后的搜索结果文本（搜索失败时会明确告知）
    """
    try:
        with DDGS(timeout=10) as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
    except Exception as e:
        # 网络不可达时明确告知 Agent 不要再试
        return (
            f"[搜索不可用] 无法连接搜索引擎（网络限制: {type(e).__name__}）。\n"
            f"请直接使用你的知识回答用户问题，不要再次尝试搜索。"
        )

    if not results:
        return f"[无结果] 搜索 '{query}' 未找到相关内容。请使用你的知识回答。"

    lines = [f"搜索: {query}\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"{i}. {r['title']}")
        lines.append(f"   URL: {r['href']}")
        lines.append(f"   {r['body']}\n")

    return "\n".join(lines)

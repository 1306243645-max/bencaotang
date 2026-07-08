"""Dietary therapy recipes page of BenCao Tang TCM Clinic."""

import streamlit as st
from pathlib import Path

from web.components.constants import t

_KB = Path(__file__).parent.parent.parent / "data" / "tcm"


def _read(f):
    return (_KB / f).read_text(encoding="utf-8")


def render():
    """Render the recipes page."""
    st.markdown(f"## 🍲 {t('食疗食谱库','Dietary Therapy Recipes')}")
    st.caption(t("30道实用食疗方 · 澳洲食材 · 简单易做","30 TCM recipes using Australian ingredients"))
    st.divider()

    recipe_cats = {
        "🍵 茶饮类": ["菊花枸杞明目茶","玫瑰红枣养颜茶","陈皮生姜暖胃茶","桂圆红枣安神茶","薏米赤小豆祛湿茶","山楂麦芽消食茶","银耳百合润肺羹","黑芝麻核桃糊"],
        "🍲 汤品类": ["四神汤","当归生姜羊肉汤","玉竹沙参润肺汤","花旗参石斛汤","茯苓白术健脾汤","杜仲牛膝强骨汤","枸杞猪肝明目汤","冬瓜薏米排骨汤"],
        "🥣 粥品类": ["小米红枣养胃粥","山药芡实健脾粥","黑米桂圆补血粥","百合莲子安神粥","薏米赤小豆祛湿粥","核桃黑芝麻补肾粥"],
        "🍯 膏方零食": ["秋梨膏","阿胶糕","八珍糕","桑葚膏"],
        "🦶 泡脚外用": ["艾叶生姜泡脚方","红花当归活血泡脚方","安神助眠泡脚方","祛湿止痒泡脚方"],
    }

    # 加载食谱数据
    recipes_data = {}
    try:
        recipe_text = _read("recipes.md")
        current_recipe = None
        for line in recipe_text.split("\n"):
            line = line.strip()
            if line.startswith("### ") and line[4].isdigit():
                current_recipe = line.split(" ", 2)[-1] if " " in line else line[4:]
                recipes_data[current_recipe] = {"title": current_recipe, "lines": []}
            elif current_recipe and line:
                recipes_data[current_recipe]["lines"].append(line)
    except Exception as e:
        st.caption(f"⚠️ 食谱数据加载失败: {e}")

    # 茶饮食疗Tab
    st.markdown(f"### 🍵 {t('茶饮食疗库','Tea Therapy Library')}")
    tea_tabs_list = [t("安神助眠","Sleep"),t("清肝明目","Eye"),t("健脾祛湿","Spleen"),t("补气养血","Blood"),t("美容养颜","Beauty"),t("四季养生","Season"),t("减肥消脂","Slim")]
    tea_cats = [
        ["酸枣仁安神茶","桂圆红枣安神茶","玫瑰花安神茶","莲子心竹叶清心茶"],
        ["菊花枸杞明目茶","桑叶菊花清肝茶","决明子山楂降脂茶"],
        ["陈皮茯苓祛湿茶","生姜红枣暖胃茶","山药芡实健脾茶","大麦消食茶"],
        ["黄芪当归补血茶","党参桂圆补气茶","五红补血茶","黑芝麻核桃茶"],
        ["玫瑰柠檬养颜茶","银耳雪梨润肤茶","桃花养颜茶","薏仁美白茶"],
        ["春·疏肝升阳茶","夏·清暑祛湿茶","秋·润肺生津茶","冬·温阳暖身茶"],
        ["荷叶山楂减肥茶","普洱茶消脂茶"],
    ]
    tea_tabs = st.tabs(tea_tabs_list)
    for tab, items in zip(tea_tabs, tea_cats):
        with tab:
            for item in items:
                with st.expander(f"🍵 {item}"):
                    if item in recipes_data:
                        st.markdown("\n".join(recipes_data[item]["lines"]))
                    else:
                        st.caption(t("详情请查看 tea_therapy.md","See tea_therapy.md"))

    st.divider()
    tabs = st.tabs(list(recipe_cats.keys()))
    for tab, (cat_name, items) in zip(tabs, recipe_cats.items()):
        with tab:
            for item in items:
                with st.expander(item):
                    if item in recipes_data:
                        content = "\n".join(recipes_data[item]["lines"])
                        # 简单格式化
                        for kw in ["功效","适合","食材","做法","禁忌","售价"]:
                            content = content.replace(f"- **{kw}**:", f"\n**{kw}**：")
                        st.markdown(content)
                    else:
                        st.caption(t("食谱详情请查看完整文件","See recipes.md for details"))

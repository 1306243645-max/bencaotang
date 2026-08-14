"""AI consultation page of BenCao Tang TCM Clinic (chat, tongue, face, fengshui, tea, quiz tabs)."""

import json
from pathlib import Path
from datetime import datetime

import streamlit as st

from web.components.constants import t, CONSTITUTION_QUIZ


def render():
    """Render the AI consultation page with all its tabs."""
    tab_names = [t("💬 智能问诊","💬 Chat"), t("👅 舌诊分析","👅 Tongue"), t("🔮 面诊分析","🔮 Face"), t("🏔️ 风水咨询","🏔️ Feng Shui"), t("🍵 问茶","🍵 Tea"), t("📋 体质自测","📋 Quiz")]
    tab_chat, tab_tongue, tab_mianxiang, tab_fengshui, tab_teapres, tab_quiz = st.tabs(tab_names)

    # --- 智能问诊 ---
    with tab_chat:
        if not st.session_state.messages:
            st.markdown(f"### {t('欢迎使用妙手堂 AI 问诊','Welcome to BenCao Tang AI')}")
            st.markdown(t(
                "我是妙手堂的 AI 健康顾问。选择下方模板或直接描述症状，即刻辨证分析。\n\n⚠️ 本 AI 提供健康教育信息，不替代医生诊断。",
                "I'm the BenCao Tang AI health advisor. Select a template or describe your symptoms.\n\n⚠️ Educational info only."
            ))

            # 模板分类选择
            q_templates = {
                t("😴 睡眠问题","😴 Sleep"): [
                    ("入睡困难多梦易醒","入睡困难，多梦易醒，心慌健忘，是什么中医证型？怎么调理？"),
                    ("凌晨1-3点准时醒","每天凌晨1-3点准时醒，醒来口干口苦，烦躁，中医怎么看？"),
                    ("半夜醒+盗汗","睡着后半夜总醒，手心脚心发热，盗汗，口干，是什么阴虚？"),
                ],
                t("🍽️ 消化问题","🍽️ Digestion"): [
                    ("饭后腹胀乏力","饭后腹胀，浑身乏力，大便稀不成形，是什么脾胃问题？"),
                    ("胃酸烧心","胃酸反流烧心，打嗝，吃什么都不消化，中医怎么调理？"),
                    ("便秘","长期便秘，大便干结如羊粪，口干，吃什么能改善？"),
                ],
                t("👩 女性健康","👩 Women"): [
                    ("痛经怕冷","月经痛，喜暖怕冷，血色暗有血块，得热痛减，怎么调理？"),
                    ("经前烦躁","月经前乳房胀痛，烦躁易怒，情绪波动大，中医怎么疏肝？"),
                    ("更年期潮热","更年期一阵阵发热出汗，心烦失眠，口干，怎么滋阴？"),
                ],
                t("💪 体质调理","💪 Body"): [
                    ("总是疲劳","总是感觉很累，说话都没力气，稍微活动就出汗，怎么补气？"),
                    ("手脚冰凉","一年四季手脚冰凉，特别怕冷，是什么阳虚？怎么调理？"),
                    ("脸油长痘","脸上爱出油长痘，口苦口臭，大便粘滞，是什么湿热？"),
                ],
                t("🌿 养生咨询","🌿 Wellness"): [
                    ("体质测试请求","我想知道自己是哪种中医体质，帮我分析一下。我的出生年份是____"),
                    ("夏季养生","三伏天怎么养生？清热祛湿有什么好方法？推荐什么茶饮？"),
                    ("日常茶饮推荐","根据我的体质，推荐一款日常喝的养生茶。我平时容易____"),
                ],
                t("🎓 留学生","🎓 Student"): [
                    ("熬夜救急","我是留学生经常熬夜赶due，喝咖啡失眠口干，平价调理方法？"),
                    ("考试焦虑","留学生考试压力大焦虑紧张，中医有什么简单缓解方法？"),
                    ("外卖胃","留学生天天外卖，胃不舒服腹胀便秘，超市能买到的调理方法？"),
                ],
            }

            template_tabs = st.tabs(list(q_templates.keys()))
            for tab, (cat_name, questions) in zip(template_tabs, q_templates.items()):
                with tab:
                    cols = st.columns(len(questions))
                    for i, (label, prompt) in enumerate(questions):
                        with cols[i]:
                            if st.button(label, use_container_width=True, key=f"qtpl_{cat_name}_{i}"):
                                st.session_state.messages.append({"role": "user", "content": prompt})
                                st.rerun()

        # 舌诊快拍——相机+上传双入口
        tongue_col1, tongue_col2 = st.columns([1, 1])
        with tongue_col1:
            tongue_camera = st.camera_input(
                t("📷 拍照舌象","📷 Take Tongue Photo"),
                key="tongue_camera", label_visibility="visible"
            )
            tongue_file = tongue_camera
        with tongue_col2:
            tongue_upload = st.file_uploader(
                t("📁 或上传舌象照片","📁 Or upload photo"),
                type=["jpg","jpeg","png","webp"], key="tongue_chat", label_visibility="visible"
            )
            if tongue_upload:
                tongue_file = tongue_upload

        if tongue_file:
            # 预览
            c_preview, c_btn = st.columns([1, 1])
            with c_preview:
                st.image(tongue_file, width=200, caption=t("舌象预览","Preview"))
            with c_btn:
                if st.button(t("🔍 分析舌象并加入问诊","🔍 Analyze & Consult"), use_container_width=True, type="primary"):
                    with st.spinner(t("AI分析舌象中...","Analyzing tongue...")):
                        tp = t("从中医角度分析舌象：舌色舌形苔色苔质。简短回复。","TCM tongue analysis: color shape coating. Brief.")
                        resp = st.session_state.agent.chat(tp)
                        st.session_state.messages.append({"role": "user", "content": "📸 [上传了舌象照片]"})
                        st.session_state.messages.append({"role": "assistant", "content": f"👅 舌诊结果：{resp.content}"})
                        st.success(t("舌象已分析！请继续描述症状","Tongue analyzed! Continue"))
                        st.rerun()

        for msg in st.session_state.messages:
            avatar = "🧑" if msg["role"] == "user" else "🐼"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        if prompt := st.chat_input(t("描述你的症状...","Describe your symptoms...")):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🧑"):
                st.markdown(prompt)
            with st.chat_message("assistant", avatar="🐼"):
                try:
                    with st.spinner(t("辨证分析中...","Analyzing pattern...")):
                        # 构建对话历史传给 Agent
                        history = []
                        for m in st.session_state.messages[:-1]:  # 不包括刚发的这条
                            role = "user" if m["role"] == "user" else "assistant"
                            history.append({"role": role, "content": m["content"]})
                        resp = st.session_state.agent.chat(prompt, history=history if history else None)
                        st.markdown(resp.content)
                        st.session_state.tool_count += len(resp.tool_calls or [])
                        # 显示工具调用统计
                        if resp.tool_calls:
                            st.caption(f"📚 调用了 {len(resp.tool_calls)} 个知识库")
                except Exception as e:
                    st.error(f"错误: {type(e).__name__}: {e}")
                    import traceback
                    st.code(traceback.format_exc())
            st.session_state.messages.append({"role": "assistant", "content": resp.content if 'resp' in dir() else '系统出错，请重试'})

        if st.session_state.messages:
            st.divider()
            if st.button(t("🔄 新对话","🔄 New Chat"), use_container_width=True):
                st.session_state.messages = []
                st.session_state.tool_count = 0
                st.rerun()

    # --- 舌诊分析 ---
    with tab_tongue:
        st.markdown(f"### 👅 {t('妙手堂 · AI舌诊','BenCao Tang · AI Tongue Dx')}")

        # 拍摄指南
        with st.expander(t("📸 如何拍一张合格的舌象照片？","📸 How to take a good tongue photo"), expanded=True):
            guide_cols = st.columns(4)
            with guide_cols[0]:
                st.markdown(f"**1️⃣ {t('光线','Light')}**\n{t('自然光，面向窗户','Natural light, face window')}")
            with guide_cols[1]:
                st.markdown(f"**2️⃣ {t('角度','Angle')}**\n{t('舌头自然伸出，不要用力','Relax tongue, extend naturally')}")
            with guide_cols[2]:
                st.markdown(f"**3️⃣ {t('禁止','Avoid')}**\n{t('不美颜不滤镜，不用闪光灯','No filter, no flash')}")
            with guide_cols[3]:
                st.markdown(f"**4️⃣ {t('时机','Timing')}**\n{t('早上刷牙前拍最准','Best: morning before brushing')}")

        st.divider()

        # 上传区
        tongue_file = st.file_uploader(
            t("📸 上传舌象照片","📸 Upload tongue photo"),
            type=["jpg","jpeg","png","webp"], key="tongue"
        )

        if tongue_file:
            c_i, c_b = st.columns([1, 1])
            with c_i:
                st.image(tongue_file, use_container_width=True, caption=t("舌象照片","Tongue Photo"))
            with c_b:
                if st.button(t("🔍 开始AI舌诊分析","🔍 Start AI Analysis"), use_container_width=True, type="primary"):
                    with st.spinner(t("AI分析中...","AI analyzing...")):
                        prompt = t(
                            """请从中医角度专业分析这张舌象照片，按以下结构输出：

## 👅 舌象四维分析
| 维度 | 判断 | 说明 |
|------|------|------|
| 舌色 | ___ | 淡白/淡红/红/绛红/紫暗 |
| 舌形 | ___ | 胖大/瘦薄/齿痕/裂纹/正常 |
| 苔色 | ___ | 白/黄/灰黑 |
| 苔质 | ___ | 薄/厚/腻/剥落/正常 |

## 🎯 综合辨证
根据舌象判断可能的证型（1-2个）

## 🍵 调理建议
- 食疗推荐
- 茶饮推荐
- 穴位按摩

## ⚠️ 免责声明""",
                            """TCM tongue photo analysis. Output:

## 👅 Tongue Analysis (4 Dimensions)
- Body Color: ___
- Body Shape: ___
- Coating Color: ___
- Coating Texture: ___

## 🎯 Pattern Diagnosis

## 🍵 Recommendations
- Diet
- Tea
- Acupressure

## ⚠️ Disclaimer"""
                        )
                        resp = st.session_state.agent.chat(prompt)
                        st.markdown(resp.content)
                        st.session_state.messages.append({"role": "user", "content": "👅 [舌象照片]"})
                        st.session_state.messages.append({"role": "assistant", "content": resp.content})
                        st.session_state.tool_count += len(resp.tool_calls or [])

        # 舌象知识速查
        st.divider()
        st.markdown(f"#### {t('📚 舌诊知识速查','📚 Quick Reference')}")
        ref_cols = st.columns(4)
        ref_data = [
            ("淡白舌", t("气血虚/阳虚","Qi-Blood Deficiency"), "🩸"),
            ("红舌", t("实热证","Heat Pattern"), "🔥"),
            ("齿痕舌", t("脾虚湿盛","Spleen Qi Deficiency"), "💧"),
            ("黄腻苔", t("湿热内蕴","Damp-Heat"), "🌡️"),
        ]
        for i, (key, val, icon) in enumerate(ref_data):
            with ref_cols[i]:
                st.markdown(f"{icon} **{key}**\n*{val}*")

    # --- 体质自测 ---
    with tab_quiz:
        st.markdown(f"### 📋 {t('中医体质自测','TCM Constitution Self-Test')}")

        # 说明区域
        with st.expander(t("🧪 什么是体质自测？","🧪 What is this test?"), expanded=False):
            st.markdown(t("""
            **中医将人体分为9种体质**，每种体质在饮食、运动、易患病倾向都有不同。

            这个自测基于中华中医药学会《中医体质分类与判定》标准，通过9组简单问题帮你找到自己的体质类型。

            - ⏱️ 耗时：2 分钟
            - 📊 结果：你的体质雷达图 + AI 个性化调理方案
            - 🎯 后续：根据体质推荐茶饮、食疗、穴位

            **评分标准**：1=从不 2=偶尔 3=有时 4=经常 5=总是
            """, """
            **TCM identifies 9 body constitution types.** Each has different dietary needs, exercise preferences, and health tendencies.

            Based on the official TCM Constitution Classification standard with 9 simple questions.

            - ⏱️ Time: 2 minutes
            - 📊 Result: Your constitution profile + AI wellness plan
            - 🎯 Follow-up: Personalized tea, diet, and acupressure

            **Scale**: 1=Never 2=Rarely 3=Sometimes 4=Often 5=Always
            """))

        st.divider()
        st.caption(t("评分：1=从不 2=偶尔 3=有时 4=经常 5=总是","Scale: 1=Never 2=Rarely 3=Sometimes 4=Often 5=Always"))

        scores = {}
        ctype_keys = list(CONSTITUTION_QUIZ.keys())
        ctype_emojis = {
            "平和质": "😊", "气虚质": "😴", "阳虚质": "🥶",
            "阴虚质": "🔥", "痰湿质": "💧", "湿热质": "🌡️",
            "气郁质": "😟", "血瘀质": "🟣", "特禀质": "🤧",
        }

        # 用两列布局紧凑展示
        for idx, ctype in enumerate(ctype_keys):
            qs = CONSTITUTION_QUIZ[ctype]
            emoji = ctype_emojis.get(ctype, "📋")
            st.markdown(f"**{emoji} {ctype}**")
            cols = st.columns(len(qs))
            vals = []
            for i, q in enumerate(qs):
                safe_key = f"qz_{idx}_{i}"
                with cols[i]:
                    vals.append(st.select_slider(
                        q, [1, 2, 3, 4, 5], 3,
                        key=safe_key, label_visibility="collapsed"
                    ))
            scores[ctype] = vals

        st.divider()

        c_a, c_b, c_c = st.columns([2, 2, 3])
        with c_a:
            if st.button(t("📊 查看我的体质","📊 View My Results"), use_container_width=True, type="primary"):
                results = {ct: round(sum(v)/len(v), 1) for ct, v in scores.items()}
                sorted_r = sorted(results.items(), key=lambda x: x[1], reverse=True)
                top = sorted_r[0]
                second = sorted_r[1] if len(sorted_r) > 1 else None

                st.divider()
                st.balloons()

                # 主打体质大卡片
                emoji = ctype_emojis.get(top[0], "📋")
                st.markdown(f"""
                <div style="text-align:center;padding:2rem;background:linear-gradient(135deg,#EDE8F5,#F5F2FA);border-radius:16px;border:2px solid #B5A8D4;margin-bottom:1rem;">
                    <div style="font-size:3rem;">{emoji}</div>
                    <h2 style="color:#3C2864;margin:0.3rem 0;">{t('你的体质：','Your Constitution: ')}{top[0]}</h2>
                    <p style="font-size:1.2rem;color:#666;">{t('得分','Score')}: {top[1]}/5</p>
                </div>
                """, unsafe_allow_html=True)

                # 雷达图式的进度条
                st.markdown(f"#### {t('📊 九种体质对比','📊 All 9 Types Comparison')}")
                for ct, sc in sorted_r:
                    ratio = sc / 5.0
                    color = "#2d6a4f" if sc >= 3.5 else ("#e67e22" if sc >= 2.5 else "#999")
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;margin:0.3rem 0;">
                        <span style="width:70px;font-size:0.85rem;">{ct}</span>
                        <div style="flex:1;height:18px;background:#eee;border-radius:9px;overflow:hidden;">
                            <div style="width:{ratio*100}%;height:100%;background:{color};border-radius:9px;"></div>
                        </div>
                        <span style="width:40px;text-align:right;font-weight:bold;">{sc}</span>
                    </div>
                    """, unsafe_allow_html=True)

                # AI 分析
                top_types = [f"{ct}:{s}" for ct, s in sorted_r if s >= 3.0]
                with st.spinner(t("🤖 AI正在生成你的体质调理方案...","🤖 AI generating your wellness plan...")):
                    resp = st.session_state.agent.chat(f"""
用户刚完成中医体质自测，结果如下：
主要体质：{top[0]}（{top[1]}/5）
次要体质：{second[0]}（{second[1]}/5）{f'存在' if second else ''}
完整排名：{', '.join(top_types)}

请用生活化的语言给出个性化调理方案。严格按以下格式输出：

## 🎯 你的体质画像
用1-2句通俗比喻形容这个体质的特点（比如「你就像一个火力不足的小火炉」）

## 📋 体质特点
3个最典型的表现

## 🍳 食疗方案
- 推荐食材（3-5种，优先超市常见食材）
- 禁忌食物（3种）
- 1个简单食疗方（含克数+做法）

## 💆 穴位按摩
2个关键穴位（含取穴方法+按摩技巧+时长）

## 🍵 茶饮推荐
1款匹配体质的茶（含配方+冲泡方法）

## 🏃 运动建议
适合的运动类型和强度

## ⚠️ 注意事项
2条关键提醒

格式简洁，用emoji分段，易于阅读。""")
                    st.markdown(resp.content)

                st.session_state.messages.append({"role": "user", "content": f"📋 体质自测完成: {top[0]}({top[1]}/5)"})
                st.session_state.messages.append({"role": "assistant", "content": resp.content})

        with c_b:
            if st.button(t("🔄 全部重置","🔄 Reset All"), use_container_width=True):
                for ci in range(len(ctype_keys)):
                    for i in range(3):
                        st.session_state.pop(f"qz_{ci}_{i}", None)
                st.rerun()

        with c_c:
            st.info(t(
                "💡 **提示**：如实填写更准确。选择与平时最符合的感觉，不是偶尔出现的情况。",
                "💡 **Tip**: Answer honestly. Pick what feels most usual — not occasional feelings."
            ))

    # --- 金锁玉关风水咨询 ---
    with tab_fengshui:
        st.markdown(f"### 🏔️ {t('金锁玉关 · 风水咨询','Jin Suo Yu Guan Feng Shui')}")
        st.caption(t("八卦砂水法 · 二十四山向 · 家居风水诊断","8-Trigram Sand-Water Method"))

        feng_col1, feng_col2 = st.columns([1, 1])
        with feng_col1:
            feng_type = st.selectbox(t("咨询类型","Type"), [
                t("家居风水","Home"),t("办公室风水","Office"),t("健康风水","Health"),t("事业财运","Career")
            ], key="feng_type")
            feng_issue = st.selectbox(t("主要问题","Main Issue"), [
                t("睡眠不好","Poor Sleep"),t("事业不顺","Career Issues"),t("家人健康","Family Health"),
                t("财运不佳","Financial"),t("孩子学业","Children Studies"),t("人际关系","Relationships"),
                t("综合诊断","General Check")
            ], key="feng_issue")
        with feng_col2:
            feng_dir = st.text_input(t("房屋朝向（如坐北朝南）","House Direction"), placeholder=t("例如：坐北朝南","e.g. North-South"), key="feng_dir")
            feng_desc = st.text_area(t("房屋布局描述","Layout Description"), placeholder=t("例如：西北方是厨房，正南是落地窗，正东是卫生间...","e.g. NW=kitchen, S=window, E=bathroom..."), key="feng_desc", height=100)

        if st.button(t("🏔️ 风水诊断","🏔️ Feng Shui Analysis"), use_container_width=True, type="primary"):
            if feng_dir or feng_desc:
                with st.spinner(t("金锁玉关分析中...","Analyzing Feng Shui...")):
                    prompt = f"""用户咨询金锁玉关风水：
类型={feng_type}，问题={feng_issue}
朝向={feng_dir or '未提供'}，布局={feng_desc or '未提供'}

请用 read_fengshui 知识库进行分析：

1. 🧭 八卦砂水诊断（逐方位分析砂水是否得位）
2. ⚠️ 找出问题方位（砂水反位的地方）
3. 🩺 对应的健康/运势影响
4. 🔧 具体化解方案（每个问题方位给出可操作的化解方法）
5. 📋 综合风水评分和改进建议"""
                    resp = st.session_state.agent.chat(prompt)
                    st.markdown(resp.content)
                    st.session_state.messages.append({"role": "user", "content": f"🏔️ 风水咨询：{feng_type}"})
                    st.session_state.messages.append({"role": "assistant", "content": resp.content})
            else:
                st.warning(t("请至少填写房屋朝向或布局描述","Please fill in at least direction or layout"))

    # --- 问茶（五运六气茶饮处方）---
    with tab_teapres:
        st.markdown(f"### 🍵 {t('五运六气 · 一人一茶','Personalized Tea Rx')}")
        st.caption(t("出生体质 + 当前节气 + 所在地域 → 今日专属茶方","Birth constitution + Solar term + Location = Your Tea"))

        tea_col1, tea_col2 = st.columns([1, 1])
        with tea_col1:
            from datetime import datetime as _dt
            tea_birth = st.date_input(
                t("出生日期","Birth Date"),
                value=_dt(1990, 6, 15),
                min_value=_dt(1940, 1, 1),
                max_value=_dt(2026, 12, 31),
                key="tea_birth"
            )
        with tea_col2:
            tea_location = st.selectbox(t("所在地","Location"), [
                t("北方（黄河以北）","North"),t("南方（长江以南）","South"),
                t("东部沿海","East Coast"),t("西部高原","West"),t("中部（中原）","Central"),
                t("东北","Northeast"),t("西南","Southwest"),t("海外·澳洲","Australia")
            ], key="tea_loc")
            today = _dt.now()
            st.info(f"📅 {t('今日','Today')}: {today.strftime('%Y年%m月%d日')}")
            st.caption(t("💡 出生月日定位六气时段，体质分析更精准","Birth MD → Qi phase, more precise"))

        if st.button(t("🍵 生成今日专属茶方","🍵 Generate My Tea"), use_container_width=True, type="primary"):
            with st.spinner(t("正在推算您的专属茶方...","Creating your tea prescription...")):
                prompt = f"""用户信息：
- 出生日期：{tea_birth.year}年{tea_birth.month}月{tea_birth.day}日
- 所在地：{tea_location}
- 当前日期：{today.strftime('%Y-%m-%d')}

请用 read_personalized_tea 知识库，结合毛小妹五运六气和人体气象站理论，为这个用户生成「一人一方」专属茶饮处方。

注意：
- 出生月日能更精准判断司天/在泉的影响权重
- 生于上半年受司天影响大，下半年受在泉影响大
- 月日落在不同节气（初之气到终之气）影响不同

输出格式：
1. 🎯 先天运气体质分析（根据出生年月日推算，含岁运+司天在泉权重）
2. 📅 当前节气影响（自动判断当前属于哪个节气）
3. 🌍 地域调和茶材
4. 🍵 **今日专属茶方**（含具体配方克数+泡法）
5. 💪 功效说明
6. ⚠️ 禁忌提醒"""
                resp = st.session_state.agent.chat(prompt)
                st.markdown(resp.content)
                st.session_state.messages.append({"role": "user", "content": f"🍵 问茶：{tea_birth.year}年{tea_birth.month}月{tea_birth.day}日生，{tea_location}"})
                st.session_state.messages.append({"role": "assistant", "content": resp.content})

    # --- 面诊分析 ---
    with tab_mianxiang:
        st.markdown(f"### 🔮 {t('周易面诊分析','Zhouyi Face Reading')}")
        st.info(t("📸 自然光正面照，不美颜，可以看到全脸","📸 Natural light, front-facing photo, no filter"))

        face_col1, face_col2 = st.columns([1, 1])
        with face_col1:
            face_type = st.selectbox(t("你的面型（对着镜子看）","Face Shape"),
                [t("方形（国字脸）","Square"),t("长形（长脸）","Long"),t("圆形（满月脸）","Round"),
                 t("三角形（甲字脸）","Triangle"),t("梯形（由字脸）","Trapezoid")])
            face_color = st.selectbox(t("整体面色","Complexion"),
                [t("正常红润","Normal"),t("偏青","Bluish"),t("偏红","Reddish"),
                 t("偏黄","Yellowish"),t("偏白","Pale"),t("偏黑/暗","Dark")])
            mian_areas = st.multiselect(t("面部异常区域（多选）","Problem Areas"),
                [t("额头痘痘/红赤","Forehead"),t("眉心发红","Between brows"),
                 t("鼻头发红","Nose tip"),t("两颧潮红","Cheek flush"),
                 t("眼眶暗沉","Dark circles"),t("下巴反复长痘","Chin acne"),
                 t("太阳穴青筋","Temple veins"),t("嘴唇苍白","Pale lips")])

        with face_col2:
            mian_age = st.number_input(t("年龄","Age"), 15, 90, 30)
            mian_sleep = st.selectbox(t("睡眠质量","Sleep"), [t("好","Good"),t("一般","OK"),t("差","Poor")])
            mian_stress = st.selectbox(t("压力程度","Stress"), [t("低","Low"),t("中","Medium"),t("高","High")])

            if st.button(t("🔮 周易面诊分析","🔮 Analyze Face"), use_container_width=True, type="primary"):
                with st.spinner(t("面诊分析中...","Analyzing face...")):
                    prompt = f"""请用周易面相结合中医望诊进行分析：

用户信息：面型={face_type}，面色={face_color}，年龄={mian_age}岁
面部问题：{', '.join(mian_areas) if mian_areas else '无明显异常'}
睡眠={mian_sleep}，压力={mian_stress}

请给出：
1. 🎭 五行面型分析（面型对应五行+体质倾向）
2. 🎨 五色诊分析（面色对应脏腑问题）
3. 🗺️ 面部区域分析（每个异常区域对应的脏腑问题）
4. 📋 综合面诊结论
5. 🍳 对应调理建议（食疗+穴位+生活方式）
6. ⚠️ 附免责声明

使用 read_mianxiang 知识库。"""
                    resp = st.session_state.agent.chat(prompt)
                    st.markdown(resp.content)
                    st.session_state.messages.append({"role": "user", "content": f"🔮 面诊分析：面型{face_type}，面色{face_color}"})
                    st.session_state.messages.append({"role": "assistant", "content": resp.content})

    # 侧栏统计
    with st.sidebar:
        st.divider()
        st.metric(t("消息","Msgs"), len(st.session_state.messages)//2)
        st.metric(t("知识库调用","KB Uses"), st.session_state.tool_count)

        # 引流磁铁
        st.divider()
        st.markdown(f"#### 🎁 {t('免费领体质报告','Free Report')}")
        lead_email = st.text_input(t("输入邮箱获取完整体质报告","Email for free report"), key="lead_email")
        if st.button(t("📩 发送报告","📩 Send Report"), use_container_width=True, type="primary"):
            if lead_email and "@" in lead_email and st.session_state.messages:
                # 保存线索
                lead_file = Path(__file__).parent.parent.parent / "output" / "leads.jsonl"
                lead_file.parent.mkdir(exist_ok=True)
                with open(lead_file, "a", encoding="utf-8") as f:
                    json.dump({"email": lead_email, "time": datetime.now().isoformat()}, f, ensure_ascii=False)
                    f.write("\n")
                st.success(t("✅ 报告已发送！请查收邮箱","✅ Report sent! Check your inbox"))
            elif not lead_email:
                st.error(t("请输入邮箱","Enter email"))
            else:
                st.error(t("请先进行问诊再领取报告","Chat first then get report"))

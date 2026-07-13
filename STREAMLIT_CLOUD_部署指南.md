# 本草堂 · Streamlit Cloud 部署指南

> 5 分钟部署，永久在线，免费

---

## 第一步：创建 GitHub 仓库

1. 打开 https://github.com → 登录（没有就注册一个）
2. 右上角 + → **New repository**
3. Repository name: `bencaotang`
4. 选 **Public**
5. **不要**勾选 "Add a README file"
6. 点击 **Create repository**

---

## 第二步：推送代码

在终端运行（替换 `你的用户名`）：

```bash
cd C:\Users\Admin\agent-workstation
git remote add origin https://github.com/你的用户名/bencaotang.git
git branch -M main
git add -A
git commit -m "deploy to streamlit cloud"
git push -u origin main
```

---

## 第三步：部署到 Streamlit Cloud

1. 打开 https://share.streamlit.io
2. 用 GitHub 账号登录
3. 点击 **New app**
4. 选择仓库 → `你的用户名/bencaotang`
5. Branch: `main`
6. Main file path: `streamlit_app.py`
7. 点击 **Deploy**

---

## 第四步：配置 Secrets

部署后会提示配置 Secrets。在 App Settings → Secrets 中添加：

```
ANTHROPIC_AUTH_TOKEN = sk-7fe50f7f8088400ebd7dbba8fd243da9
ANTHROPIC_BASE_URL = https://api.deepseek.com/anthropic
ANTHROPIC_DEFAULT_MODEL = deepseek-v4-pro
```

---

## 部署后

你的网站地址：`https://bencaotang.streamlit.app`

- ✅ 永久在线，不关机
- ✅ 自动 HTTPS
- ✅ 免费

---

## 可选：绑定本草堂.icu

在阿里云 DNS 解析中，用「显性URL」转发：
- 记录值：`https://bencaotang.streamlit.app`

---

有问题随时问。

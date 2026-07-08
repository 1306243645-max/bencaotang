# 本草堂 · Streamlit Cloud 免费部署指南

> 免费！永久域名！全球访问！

---

## 第一步：创建 GitHub 仓库（5分钟）

1. 打开 https://github.com → 注册/登录
2. 点击右上角「+」→「New repository」
3. 填写：
   - Repository name: `bencaotang`
   - Description: 山东本草堂中医诊所 - AI中医问诊平台
   - 选择 Public（公开）
   - ⚠️ 不要勾选 Add README
4. 点击「Create repository」

## 第二步：推送代码（2分钟）

复制下面命令，在终端里逐行执行：

```bash
cd C:\Users\Admin\agent-workstation

# 初始化 git
git init
git add .
git commit -m "本草堂中医诊所上线"

# 推送到 GitHub（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/bencaotang.git
git branch -M main
git push -u origin main
```

## 第三步：部署到 Streamlit Cloud（3分钟）

1. 打开 https://share.streamlit.io
2. 点击「Sign in with GitHub」
3. 授权登录
4. 点击「New app」
5. 选择：
   - Repository: `YOUR_USERNAME/bencaotang`
   - Branch: `main`
   - Main file path: `streamlit_app.py`
6. 点击「Deploy」

## 第四步：获取免费域名

部署成功后，你的网址是：
```
https://bencaotang.streamlit.app
```

这个网址：
- ✅ 永久有效
- ✅ 全球可访问
- ✅ 免费 HTTPS
- ✅ 自动更新（推代码即更新）

---

## 部署后

1. 把新网址发给我，我更新所有海报和二维码
2. 任何人扫海报二维码，全球都能打开本草堂！

---

## ⚠️ 注意事项

- 知识库文件较大（16个MD+24个PDF），首次部署可能需要5-10分钟
- 每次修改代码后 `git push`，网站自动更新
- 免费版有内存限制，但足够正常使用

"""妙手堂 OSS 一键初始化 — 创建 Bucket + 设置静态网站托管
只需运行一次。之后每次 git push 会自动通过 GitHub Actions 部署。
"""

import os
import sys
import hashlib
import hmac
import base64
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from xml.etree import ElementTree as ET


def oss_sign(access_id, access_secret, method, bucket, object_key="",
             headers=None, params=None, region="oss-cn-zhangjiakou"):
    """生成 OSS Authorization 头"""
    date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    content_type = headers.get("Content-Type", "") if headers else ""

    # Canonicalized OSS Headers
    oss_headers = ""
    if headers:
        for k in sorted(headers.keys()):
            kl = k.lower()
            if kl.startswith("x-oss-"):
                oss_headers += f"{kl}:{headers[k]}\n"

    # Canonicalized Resource
    resource = f"/{bucket}/{object_key}" if object_key else f"/{bucket}/"
    if params:
        qs = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        resource += f"?{qs}"

    string_to_sign = f"{method}\n\n{content_type}\n{date}\n{oss_headers}{resource}"

    signature = base64.b64encode(
        hmac.new(access_secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    ).decode()

    return f"OSS {access_id}:{signature}", date


def oss_request(access_id, access_secret, method, bucket, object_key="",
                headers=None, params=None, body=None, region="cn-zhangjiakou"):
    """发送 OSS REST API 请求"""
    auth, date = oss_sign(access_id, access_secret, method, bucket,
                          object_key, headers, params, f"oss-{region}")

    host = f"{bucket}.oss-{region}.aliyuncs.com"
    path = f"/{object_key}" if object_key else "/"
    if params:
        path += "?" + urllib.parse.urlencode(params)
    url = f"https://{host}{path}"

    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Date", date)
    req.add_header("Authorization", auth)
    req.add_header("Host", host)

    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def main():
    print("=" * 60)
    print("  🌿 妙手堂 · OSS 一键初始化")
    print("=" * 60)

    # 获取凭证
    access_id = os.getenv("ALIBABA_ACCESS_KEY_ID") or input("AccessKey ID: ").strip()
    access_secret = os.getenv("ALIBABA_ACCESS_KEY_SECRET") or input("AccessKey Secret: ").strip()

    if not access_id or not access_secret:
        print("\n❌ 需要阿里云 AccessKey 凭证")
        print("   设置环境变量或运行脚本时输入")
        return 1

    region = "cn-zhangjiakou"
    bucket_name = "miaoshoutang"

    print(f"\n📍 Region: {region}")
    print(f"📦 Bucket: {bucket_name}")

    # ── Step 1: 创建 Bucket ──
    print("\n📦 Step 1: 创建 OSS Bucket...")

    # PUT /{bucket} 创建 bucket
    # 需要 x-oss-acl 头设置权限
    status, body, _ = oss_request(
        access_id, access_secret, "PUT", bucket_name,
        headers={"x-oss-acl": "public-read"},
        region=region
    )

    if status == 200:
        print("  ✓ Bucket 已存在或创建成功")
    elif status == 409:
        print("  ✓ Bucket 已存在（409 Conflict = 已创建）")
    else:
        print(f"  ✗ 创建失败 (HTTP {status}): {body.decode()[:500]}")
        return 1

    # ── Step 2: 设置静态网站托管 ──
    print("\n🌐 Step 2: 设置静态网站托管...")

    website_config = """<?xml version="1.0" encoding="UTF-8"?>
<WebsiteConfiguration>
  <IndexDocument>
    <Suffix>index.html</Suffix>
  </IndexDocument>
  <ErrorDocument>
    <Key>404.html</Key>
  </ErrorDocument>
</WebsiteConfiguration>"""

    status, body, _ = oss_request(
        access_id, access_secret, "PUT", bucket_name,
        params={"website": ""},
        body=website_config.encode(),
        headers={"Content-Type": "application/xml"},
        region=region
    )

    if status == 200:
        print("  ✓ 静态网站托管已启用")
    else:
        print(f"  ⚠️  设置返回 HTTP {status}: {body.decode()[:300]}")

    # ── Step 3: 上传首页 ──
    print("\n📤 Step 3: 上传 index.html...")

    try:
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
        with open(html_path, "rb") as f:
            html = f.read()

        status, body, _ = oss_request(
            access_id, access_secret, "PUT", bucket_name,
            object_key="index.html",
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "x-oss-object-acl": "public-read",
                "Cache-Control": "max-age=3600",
            },
            body=html,
            region=region
        )

        if status == 200:
            print(f"  ✓ index.html 上传成功 ({len(html)} bytes)")
        else:
            print(f"  ⚠️  上传返回 HTTP {status}")
    except FileNotFoundError:
        print("  ⊘ index.html 未找到，跳过")

    # ── Done ──
    print("\n" + "=" * 60)
    print("  ✅ OSS 初始化完成！")
    print("=" * 60)
    print(f"""
  📍 OSS 网站地址:
     http://{bucket_name}.oss-{region}.aliyuncs.com/

  🔧 绑定自定义域名 妙手堂.icu:
     1. 打开阿里云 OSS 控制台 → {bucket_name} → 域名管理
     2. 绑定域名: 妙手堂.icu
     3. 到 DNS 控制台添加 CNAME 记录:
        记录类型: CNAME
        主机记录: @
        记录值: {bucket_name}.oss-{region}.aliyuncs.com

  🤖 GitHub Actions 自动部署已就绪
     在 GitHub Secrets 中添加:
     - ALIBABA_ACCESS_KEY_ID
     - ALIBABA_ACCESS_KEY_SECRET
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())

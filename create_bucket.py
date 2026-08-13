"""创建 OSS Bucket 并设置静态网站托管"""
import sys, os, hashlib, hmac, base64, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

BUCKET = "miaoshoutang"
REGION = "cn-zhangjiakou"
WORKSPACE = Path(__file__).parent


def get_server_offset():
    """从阿里云服务器获取时间，计算本地时钟偏移量（分钟）"""
    from datetime import timedelta
    from email.utils import parsedate_to_datetime
    try:
        url = f"https://{BUCKET}.oss-{REGION}.aliyuncs.com/"
        req = urllib.request.Request(url, method="HEAD")
        resp = urllib.request.urlopen(req, timeout=10)
        server_date = resp.headers.get("Date", "")
        server_t = parsedate_to_datetime(server_date)
        local_t = datetime.now(timezone.utc)
        offset = (server_t - local_t).total_seconds() / 60
        return offset
    except urllib.error.HTTPError as e:
        # 404 也会带 Date 头，从中取服务器时间
        server_date = e.headers.get("Date", "")
        try:
            server_t = parsedate_to_datetime(server_date)
            local_t = datetime.now(timezone.utc)
            offset = (server_t - local_t).total_seconds() / 60
            return offset
        except Exception:
            return None
    except Exception:
        return None


def oss_request(access_id, access_secret, method, path="", headers=None, body=None, query=""):
    """发送 OSS REST API 请求"""
    from datetime import timedelta
    offset = get_server_offset() or 0
    adjusted = datetime.now(timezone.utc) + timedelta(minutes=offset + 1)
    date = adjusted.strftime("%a, %d %b %Y %H:%M:%S GMT")

    # 构造 OSS 规范头
    oss_headers = ""
    for k in sorted((headers or {}).keys()):
        kl = k.lower()
        if kl.startswith("x-oss-"):
            oss_headers += f"{kl}:{headers[k]}\n"

    # 构造资源路径
    resource = f"/{BUCKET}/"
    if path:
        resource += path
    if query:
        resource += f"?{query}"

    # 获取 Content-Type
    content_type = (headers or {}).get("Content-Type", "")

    string_to_sign = f"{method}\n\n{content_type}\n{date}\n{oss_headers}{resource}"
    signature = base64.b64encode(
        hmac.new(access_secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    ).decode()
    auth = f"OSS {access_id}:{signature}"

    host = f"{BUCKET}.oss-{REGION}.aliyuncs.com"
    url = f"https://{host}/{path}"
    if query:
        url += f"?{query}"

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
    # 从环境变量、凭证文件或 stdin 读取凭证
    access_id = os.getenv("ALIBABA_ACCESS_KEY_ID")
    access_secret = os.getenv("ALIBABA_ACCESS_KEY_SECRET")

    cred_file = WORKSPACE / ".aliyun_creds"
    if (not access_id or not access_secret) and cred_file.exists():
        lines = cred_file.read_text().strip().splitlines()
        if len(lines) >= 2:
            access_id, access_secret = lines[0].strip(), lines[1].strip()

    if not access_id:
        access_id = input("AccessKey ID: ").strip()
    if not access_secret:
        access_secret = input("AccessKey Secret: ").strip()

    if not access_id or not access_secret:
        print("[ERROR] 需要阿里云 AccessKey 凭证")
        return 1

    print(f"[Region] {REGION}")
    print(f"[Bucket] {BUCKET}")

    # Step 1: 确保 Bucket 存在
    print("\n[Step 1] Checking bucket...")
    status, _, _ = oss_request(access_id, access_secret, "HEAD")
    if status == 404:
        # Bucket 不存在，创建（不设置 ACL）
        status, body, _ = oss_request(access_id, access_secret, "PUT")
        if status == 200:
            print("  [OK] Bucket created")
        else:
            print(f"  [FAIL] 创建失败 (HTTP {status}): {body.decode()[:400]}")
            return 1
    elif status == 200:
        print("  [OK] Bucket already exists")
    else:
        print(f"  [WARN] Bucket check HTTP {status}")

    # Step 1b: 设置 Bucket ACL 为公共读
    print("\n[ACL] Setting bucket public-read...")
    status, body, _ = oss_request(
        access_id, access_secret, "PUT",
        headers={"x-oss-acl": "public-read"},
        query="acl"
    )
    if status == 200:
        print("  [OK] Bucket 公共读已开启")
    else:
        print(f"  [FAIL] ACL 设置失败 (HTTP {status}): {body.decode()[:400]}")

    # --- Step 2: 设置静态网站托管 ---
    print("\n[WEB] Step 2: 设置静态网站托管...")
    config = """<?xml version="1.0" encoding="UTF-8"?>
<WebsiteConfiguration>
  <IndexDocument><Suffix>index.html</Suffix></IndexDocument>
  <ErrorDocument><Key>404.html</Key></ErrorDocument>
</WebsiteConfiguration>"""
    status, body, _ = oss_request(
        access_id, access_secret, "PUT",
        headers={"Content-Type": "application/xml"},
        body=config.encode(),
        query="website"
    )
    if status == 200:
        print("  [OK] 静态网站托管已启用")
    else:
        print(f"  [WARN]  HTTP {status}: {body.decode()[:300]}")

    # --- Step 3: 上传 index.html ---
    print("\n[UPLOAD] Step 3: 上传首页...")
    html_path = WORKSPACE / "index.html"
    if html_path.exists():
        html = html_path.read_bytes()
        status, body, _ = oss_request(
            access_id, access_secret, "PUT",
            path="index.html",
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Cache-Control": "max-age=3600",
            },
            body=html,
        )
        if status == 200:
            print(f"  [OK] index.html 上传成功 ({len(html)} bytes)")
        else:
            print(f"  [FAIL] 上传失败 (HTTP {status}): {body.decode()[:300]}")
    else:
        print("  [SKIP] index.html 未找到")

    # --- Step 4: 上传其他文件 ---
    other_files = ["404.html", "robots.txt", "sitemap.xml"]
    for f in other_files:
        fp = WORKSPACE / f
        if fp.exists():
            ct = "text/html; charset=utf-8" if f.endswith(".html") else \
                 "text/plain; charset=utf-8" if f.endswith(".txt") else \
                 "application/xml; charset=utf-8"
            status, _, _ = oss_request(
                access_id, access_secret, "PUT",
                path=f,
                headers={
                    "Content-Type": ct,
                },
                body=fp.read_bytes(),
            )
            print(f"  {'[OK]' if status == 200 else '[FAIL] HTTP '+str(status)} {f}")

    # --- Done ---
    print("\n" + "=" * 60)
    print("  [DONE] OSS 部署完成！")
    print("=" * 60)
    print(f"""
  [LOC] OSS 网站地址:
     http://{BUCKET}.oss-{REGION}.aliyuncs.com/

  [CONFIG] 绑定自定义域名 妙手堂.icu (xn--cksv0b2zp.icu):
     1. OSS 控制台 → {BUCKET} → 域名管理 → 绑定域名
     2. DNS 控制台添加 CNAME 记录:
        记录类型: CNAME  主机: @  值: {BUCKET}.oss-{REGION}.aliyuncs.com
     3. 如果使用 CDN 加速: CDN 控制台 → 添加域名 → 源站选 OSS
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())

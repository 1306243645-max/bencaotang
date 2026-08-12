"""妙手堂官网 — 部署到阿里云 OSS 静态网站托管
用法: python deploy_oss.py
需要设置环境变量:
  ALIBABA_CLOUD_ACCESS_KEY_ID
  ALIBABA_CLOUD_ACCESS_KEY_SECRET
"""

import os
import sys
import time
import json
import hmac
import hashlib
import base64
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from urllib.parse import quote, urlencode
from pathlib import Path


# ── 配置 ──────────────────────────────────────────────
ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
REGION = "cn-zhangjiakou"     # 张家口（离山东近，延迟低）
BUCKET_NAME = "miaoshoutang"  # OSS bucket 名称（需全局唯一，如不行可加随机后缀）
DOMAIN = "妙手堂.icu"          # 要绑定的域名
SITE_DIR = Path(__file__).parent  # 网站文件所在目录

# 要上传的文件列表
FILES_TO_UPLOAD = [
    "index.html",
    "site/index.html",
]

# ── 阿里云 API 签名 ───────────────────────────────────
# 参考: https://help.aliyun.com/document_detail/31951.html


def percent_encode(s):
    """RFC 3986 编码"""
    if isinstance(s, str):
        s = s.encode("utf-8")
    res = []
    for byte in s:
        if (0x30 <= byte <= 0x39 or  # 0-9
            0x41 <= byte <= 0x5A or  # A-Z
            0x61 <= byte <= 0x7A or  # a-z
            byte in (0x2D, 0x2E, 0x5F, 0x7E)):  # - . _ ~
            res.append(chr(byte))
        else:
            res.append(f"%{byte:02X}")
    return "".join(res)


def sign_request(method, params, access_key_secret):
    """生成 HMAC-SHA1 签名"""
    # 1. 构造规范化查询字符串
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    canonicalized = "&".join(
        f"{percent_encode(k)}={percent_encode(str(v))}" for k, v in sorted_params
    )
    # 2. 构造待签名字符串
    string_to_sign = f"{method}&{percent_encode('/')}&{percent_encode(canonicalized)}"
    # 3. 计算签名
    key = (access_key_secret + "&").encode("utf-8")
    signature = hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha1)
    return base64.b64encode(signature.digest()).decode("utf-8")


def call_api(service, action, extra_params=None, method="GET", body=None):
    """调用阿里云 OpenAPI"""
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    nonce = str(int(time.time() * 1000))

    params = {
        "Format": "JSON",
        "Version": "2019-05-17" if service == "oss" else "2015-01-09",
        "AccessKeyId": ACCESS_KEY_ID,
        "SignatureMethod": "HMAC-SHA1",
        "Timestamp": timestamp,
        "SignatureVersion": "1.0",
        "SignatureNonce": nonce,
        "Action": action,
    }
    if extra_params:
        params.update(extra_params)

    signature = sign_request(method, params, ACCESS_KEY_SECRET)
    params["Signature"] = signature

    # 构造 URL（OSS API 用特定 endpoint）
    if service == "oss":
        # 用各地域的 OSS endpoint
        url = f"https://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com/"

    qs = urlencode(params)
    full_url = f"{url}?{qs}" if service != "oss" else url

    print(f"  → {method} {action}")
    req = Request(full_url, data=body, method=method)
    req.add_header("Content-Type", "application/json")

    try:
        resp = urlopen(req, timeout=30)
        result = json.loads(resp.read().decode("utf-8"))
        return result
    except Exception as e:
        print(f"  ✗ API 调用失败: {e}")
        return None


# ── OSS 操作（使用 oss2 SDK 风格，但用纯 REST API）──

def ensure_bucket():
    """确保 OSS bucket 存在并启用静态网站托管"""
    print(f"\n📦 检查 OSS Bucket: {BUCKET_NAME}")

    # 获取 bucket 信息（测试是否存在）
    url = f"https://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com/"
    req = Request(url, method="HEAD")
    try:
        urlopen(req, timeout=10)
        print(f"  ✓ Bucket 已存在")
        return True
    except Exception as e:
        if "404" in str(e) or "NoSuchBucket" in str(e):
            print(f"  Bucket 不存在，需要在控制台创建")
            print(f"  请前往: https://oss.console.aliyun.com/bucket")
            print(f"  创建 Bucket:")
            print(f"    名称: {BUCKET_NAME}")
            print(f"    地域: {REGION}")
            print(f"    读写权限: 公共读")
            return False
        else:
            # 可能是权限/网络问题
            print(f"  ⚠️  无法访问 Bucket: {e}")
            return False


def upload_file(local_path, object_key, content_type="text/html"):
    """上传单个文件到 OSS"""
    file_path = SITE_DIR / local_path
    if not file_path.exists():
        print(f"  ⊘ 跳过（文件不存在）: {local_path}")
        return False

    content = file_path.read_bytes()

    # OSS PutObject 请求
    url = f"https://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com/{quote(object_key, safe='/')}"

    # 构造 OSS 签名
    date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    string_to_sign = f"PUT\n\n{content_type}\n{date}\n/{BUCKET_NAME}/{object_key}"
    signature = base64.b64encode(
        hmac.new(
            ACCESS_KEY_SECRET.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()
    ).decode("utf-8")

    req = Request(url, data=content, method="PUT")
    req.add_header("Content-Type", content_type)
    req.add_header("Content-Length", str(len(content)))
    req.add_header("Date", date)
    req.add_header(
        "Authorization",
        f"OSS {ACCESS_KEY_ID}:{signature}",
    )
    # 公共读 ACL
    req.add_header("x-oss-object-acl", "public-read")

    try:
        urlopen(req, timeout=30)
        print(f"  ✓ 上传: {local_path} → /{object_key}")
        return True
    except Exception as e:
        print(f"  ✗ 上传失败 {local_path}: {e}")
        return False


def set_bucket_website():
    """设置静态网站托管"""
    url = f"https://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com/?website"

    config = """
    <WebsiteConfiguration>
        <IndexDocument>
            <Suffix>index.html</Suffix>
        </IndexDocument>
        <ErrorDocument>
            <Key>404.html</Key>
        </ErrorDocument>
    </WebsiteConfiguration>
    """

    date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    string_to_sign = (
        f"PUT\n\napplication/xml\n{date}\n/{BUCKET_NAME}/?website"
    )
    signature = base64.b64encode(
        hmac.new(
            ACCESS_KEY_SECRET.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()
    ).decode("utf-8")

    req = Request(url, data=config.encode("utf-8"), method="PUT")
    req.add_header("Content-Type", "application/xml")
    req.add_header("Date", date)
    req.add_header("Authorization", f"OSS {ACCESS_KEY_ID}:{signature}")

    try:
        urlopen(req, timeout=30)
        print(f"  ✓ 静态网站托管已启用")
        print(f"  ✓ 访问地址: https://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com/")
        return True
    except Exception as e:
        print(f"  ✗ 设置失败: {e}")
        return False


def set_bucket_acl():
    """设置 Bucket 为公共读"""
    url = f"https://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com/?acl"

    date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    string_to_sign = (
        f"PUT\n\n\n{date}\n/{BUCKET_NAME}/?acl"
    )
    signature = base64.b64encode(
        hmac.new(
            ACCESS_KEY_SECRET.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()
    ).decode("utf-8")

    req = Request(url, data=b"", method="PUT")
    req.add_header("Date", date)
    req.add_header("Authorization", f"OSS {ACCESS_KEY_ID}:{signature}")
    req.add_header("x-oss-acl", "public-read")

    try:
        urlopen(req, timeout=30)
        print(f"  ✓ Bucket ACL 已设为公共读")
        return True
    except Exception as e:
        print(f"  ✗ ACL 设置失败: {e}")
        return False


# ── 主流程 ─────────────────────────────────────────────

def main():
    global ACCESS_KEY_ID, ACCESS_KEY_SECRET

    print("=" * 55)
    print("  🌿 妙手堂官网 · OSS 部署工具")
    print("=" * 55)

    # 检查凭证
    if not ACCESS_KEY_ID:
        ACCESS_KEY_ID = input("AccessKey ID: ").strip()
    if not ACCESS_KEY_SECRET:
        ACCESS_KEY_SECRET = input("AccessKey Secret: ").strip()

    if not ACCESS_KEY_ID or not ACCESS_KEY_SECRET:
        print("\n❌ 缺少阿里云 AccessKey 凭证")
        print("   获取方式: 阿里云控制台 → RAM 访问控制 → 用户 → 创建AccessKey")
        print("   或者设置环境变量:")
        print("     set ALIBABA_CLOUD_ACCESS_KEY_ID=your_id")
        print("     set ALIBABA_CLOUD_ACCESS_KEY_SECRET=your_secret")
        return 1

    print(f"\n📍 Region: {REGION}")
    print(f"📦 Bucket: {BUCKET_NAME}")
    print(f"🌍 Domain: {DOMAIN}")

    # Step 1: 确保 Bucket 存在
    if not ensure_bucket():
        print("\n" + "=" * 55)
        print("📋 请先在阿里云控制台手动创建 Bucket：")
        print("   1. 打开 https://oss.console.aliyun.com/bucket")
        print("   2. 点击「创建 Bucket」")
        print(f"   3. Bucket 名称: {BUCKET_NAME}")
        print(f"   4. 地域: {REGION}")
        print("   5. 读写权限: 公共读")
        print("   6. 创建完成后重新运行此脚本")
        print("=" * 55)
        return 1

    # Step 2: 设置 ACL
    print("\n🔓 设置 Bucket 权限...")
    set_bucket_acl()

    # Step 3: 上传文件
    print("\n📤 上传网站文件...")
    for f in FILES_TO_UPLOAD:
        # 对于 site/index.html，上传到根目录时用不同的 object key
        if f == "site/index.html":
            upload_file(f, "index.html", "text/html; charset=utf-8")
        elif f == "index.html":
            upload_file(f, "index.html", "text/html; charset=utf-8")

    # Step 4: 启用静态网站托管
    print("\n🌐 设置静态网站托管...")
    set_bucket_website()

    # Step 5: 打印结果
    print("\n" + "=" * 55)
    print("  ✅ 部署完成！")
    print("=" * 55)
    print(f"""
  📍 OSS 默认域名:
     http://{BUCKET_NAME}.oss-{REGION}.aliyuncs.com/

  🔧 下一步：绑定自定义域名 {DOMAIN}
     1. 打开 OSS 控制台 → Bucket → 域名管理
     2. 绑定域名: {DOMAIN}
     3. 如果开启 CDN 加速（推荐）:
        打开 CDN 控制台 → 添加域名 → 源站选 OSS
     4. 到阿里云 DNS 控制台添加 CNAME 记录:
        主机记录: @
        记录类型: CNAME
        记录值: {BUCKET_NAME}.oss-{REGION}.aliyuncs.com
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())

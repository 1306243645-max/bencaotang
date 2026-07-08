"""邮件发送工具 — 基于 smtplib，支持 QQ / 163 / Gmail / Outlook 等。"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# 常见邮箱 SMTP 配置
_SMTP_CONFIGS = {
    "qq":      ("smtp.qq.com",       587),
    "163":     ("smtp.163.com",      465),
    "126":     ("smtp.126.com",      465),
    "gmail":   ("smtp.gmail.com",    587),
    "outlook": ("smtp.office365.com", 587),
    "yahoo":   ("smtp.mail.yahoo.com", 587),
}


def _get_smtp_config(email: str) -> tuple[str, int]:
    """根据邮箱地址推断 SMTP 服务器。"""
    domain = email.split("@")[-1].lower()
    for key, cfg in _SMTP_CONFIGS.items():
        if key in domain:
            return cfg
    return ("smtp." + domain.rsplit(".", 1)[0] + ".com", 587)


def send_email(
    to: str,
    subject: str,
    body: str,
    cc: str = "",
    bcc: str = "",
    html: bool = False,
) -> str:
    """发送邮件。

    Args:
        to: 收件人，多个用逗号分隔
        subject: 邮件主题
        body: 邮件正文
        cc: 抄送（可选）
        bcc: 密送（可选）
        html: 正文是否为 HTML 格式（默认纯文本）

    Returns:
        发送结果描述

    环境变量配置（在 .env 中设置）:
        EMAIL_SENDER=your_email@example.com
        EMAIL_PASSWORD=your_app_password
        EMAIL_SMTP_HOST=smtp.example.com   (可选，自动推断)
        EMAIL_SMTP_PORT=587                (可选，自动推断)
    """
    sender = os.getenv("EMAIL_SENDER", "")
    password = os.getenv("EMAIL_PASSWORD", "")

    if not sender or not password:
        return (
            "[邮件未发送] 请在 .env 中配置 EMAIL_SENDER 和 EMAIL_PASSWORD。\n"
            "常见邮箱的 APP 密码获取方式:\n"
            "  - QQ邮箱: 设置 → 账户 → POP3/SMTP 服务 → 生成授权码\n"
            "  - 163邮箱: 设置 → POP3/SMTP/IMAP → 开启 → 新增授权码\n"
            "  - Gmail: 设置 → 安全性 → 两步验证 → 应用专用密码\n"
            "  - Outlook: 安全 → 双重验证 → 应用密码"
        )

    host = os.getenv("EMAIL_SMTP_HOST", "")
    port = int(os.getenv("EMAIL_SMTP_PORT", "0"))

    if not host:
        host, port = _get_smtp_config(sender)

    try:
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = cc
        subtype = "html" if html else "plain"
        msg.attach(MIMEText(body, subtype, "utf-8"))

        all_recipients = [addr.strip() for addr in to.split(",")]
        if cc:
            all_recipients += [addr.strip() for addr in cc.split(",")]
        if bcc:
            all_recipients += [addr.strip() for addr in bcc.split(",")]

        with smtplib.SMTP(host, port, timeout=15) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, all_recipients, msg.as_string())

        return f"邮件已发送 → 收件人: {to}, 主题: {subject}"
    except Exception as e:
        return f"[邮件发送失败] {type(e).__name__}: {e}\nSMTP: {host}:{port}"

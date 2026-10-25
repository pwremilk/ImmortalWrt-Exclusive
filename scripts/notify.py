#!/usr/bin/env python3
"""NanoMuse TG 推送（固件编译结果卡片）— 风格对齐 komari.py 卡片规范"""
import json
import os
import time
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.environ["NANOMUSE_TG_TOKEN"]
CHAT = os.environ.get("NANOMUSE_CHAT", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "")
RUN = os.environ.get("GITHUB_RUN_ID", "")
TAG = os.environ.get("FW_TAG", "")
CONCLUSION = os.environ.get("BUILD_CONCLUSION", "failure")

PHOTO_URL = "https://raw.githubusercontent.com/pwremilk/Loon-Script/main/icon/report-header.jpg"
ACG_API = "https://api.pwremilk.com/pc.php"


def post(method, payload):
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/{method}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("tg error:", e.read().decode()[:200])
        return {"ok": False}


def random_photo():
    for _ in range(5):
        try:
            req = urllib.request.Request(
                ACG_API + "?return=json",
                headers={"User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                u = json.loads(r.read()).get("url")
                if u and u.startswith("http"):
                    return u
        except Exception:
            time.sleep(1)
    return PHOTO_URL


def main():
    if not CHAT:
        print("NANOMUSE_CHAT not set, skip push")
        return
    if CONCLUSION == "success":
        head = "🔨 <b>固件编译</b>"
        body = (f"✅ <b>成功</b>   ImmortalWrt-{TAG}\n"
                "• BIOS + EFI 双镜像已发布\n"
                f"• BIOS 虚拟机刷不带 -efi 的那个")
        btn = {"text": "▸ 下载固件", "url": f"https://github.com/{REPO}/releases/tag/ImmortalWrt-{TAG}"}
    else:
        head = "🔨 <b>固件编译</b>"
        body = f"🔴 <b>失败</b>   ImmortalWrt-{TAG}"
        btn = {"text": "▸ 看日志", "url": f"https://github.com/{REPO}/actions/runs/{RUN}"}
    ts = datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M UTC+8")
    html = f'{head}\n<blockquote>{body}</blockquote>\n🕐 {ts}'
    markup = {"inline_keyboard": [[btn]]}

    photo = random_photo()
    for p in (photo, PHOTO_URL):
        r = post("sendPhoto", {"chat_id": CHAT, "photo": p, "caption": html,
                               "parse_mode": "HTML", "reply_markup": markup})
        if r.get("ok"):
            return
        if p == PHOTO_URL:
            break
    post("sendMessage", {"chat_id": CHAT, "text": html.replace("<b>", "").replace("</b>", "")
                         .replace("<blockquote>", "——").replace("</blockquote>", "——"),
                         "reply_markup": markup})


if __name__ == "__main__":
    main()

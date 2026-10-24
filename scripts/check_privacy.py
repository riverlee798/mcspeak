#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_privacy.py —— mcspeak 仓库隐私体检 / 脱敏工具。

用法：
  python scripts/check_privacy.py            # 只扫描并报告
  python scripts/check_privacy.py --fix      # 扫描 + 就地脱敏 samples 与索引

检查项：
  TOKEN      疑似 MCP Token / Bearer / 32+ 位十六进制串
  ORDER_ID   完整订单号（连续 15 位以上数字）
  PAY_ID     支付单号
  PAY_URL    支付链接
  PICKUP     真实取餐码（3~6 位纯数字，仅在三件套字段名里）
  PHONE      中国大陆手机号
  IDCARD     身份证号
  EMAIL      邮箱

注意：门店地址、店名属公开营业信息，不脱敏；餐品编码（productCode）也不脱敏。
"""

import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = [
    # 真正的密钥/令牌：只在明确的字段名或 Bearer 后出现才算
    ("TOKEN",    re.compile(r"(?i)(?:mcd[_-]?mcp[_-]?token|api[_-]?key|client[_-]?secret)\s*[:=]\s*[\"']?([A-Za-z0-9._\-]{12,})")),
    ("BEARER",   re.compile(r"(?i)bearer\s+([A-Za-z0-9._\-]{20,})")),
    ("ORDER_ID", re.compile(r'"orderId"\s*:\s*"(\d{15,})"')),
    ("PAY_ID",   re.compile(r'"payId"\s*:\s*"(\d{10,})"')),
    ("PAY_URL",  re.compile(r'"payH5Url"\s*:\s*"([^"]+)"')),
    ("PICKUP",   re.compile(r'"pickupCode"\s*:\s*"(\d{3,6})"')),
    ("COUPON_ID",   re.compile(r'"couponId"\s*:\s*"([A-Fa-f0-9]{16,})"')),
    ("COUPON_CODE", re.compile(r"\b(MCD[0-9A-Z]{10,})\b")),
    ("PHONE",    re.compile(r"(?<!\d)(1[3-9]\d{9})(?!\d)")),
    ("IDCARD",   re.compile(r"(?<!\d)(\d{17}[\dXx])(?!\d)")),
    ("EMAIL",    re.compile(r"[\w.+-]+@[\w-]+\.[\w.]{2,}")),
]

# 脱敏后的占位值（保持字段可解析）
REPLACE = {
    "orderId": "1030000000000000000000000001",
    "payId": "1110000000000000000001",
    "payH5Url": "https://example.invalid/pay?orderId=REDACTED",
    "pickupCode": "00000",
    "couponId": "C0FFEE0000000000C0FFEE0000000000",
}

SKIP_DIRS = {".git", "__pycache__", "node_modules"}
SCAN_EXT = {".json", ".md", ".html", ".py", ".txt", ".yml", ".yaml", ".example"}

# 脱敏后自己留下的占位值，不算命中
SAFE = {
    "C0FFEE0000000000C0FFEE0000000000", "MCD000000000000000",
    "1030000000000000000000000001", "1110000000000000000001", "00000", "12345",
}


def is_safe(val):
    if val in SAFE or val.startswith("https://example.invalid") or val.startswith("13****"):
        return True
    # 脱敏占位：1030…0001 / 1110…0001 系列
    return bool(re.fullmatch(r"1(?:03|11)0{18,}\d{1,3}", val))


def iter_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext in SCAN_EXT or fn == "mcp-config.example.json":
                yield os.path.join(base, fn)


def scan():
    report = []
    for path in iter_files():
        try:
            text = open(path, encoding="utf-8").read()
        except Exception:
            continue
        for name, rx in PATTERNS:
            for m in rx.finditer(text):
                val = m.group(1) if m.groups() else m.group(0)
                if is_safe(val):
                    continue
                report.append((name, os.path.relpath(path, ROOT), val[:48]))
    return report


def fix_samples():
    """对 references/samples/*.json 与 references/*.md 做就地脱敏。"""
    changed = []
    targets = sorted(glob.glob(os.path.join(ROOT, "references", "samples", "*.json")))
    targets += sorted(glob.glob(os.path.join(ROOT, "references", "*.md")))
    targets += sorted(glob.glob(os.path.join(ROOT, "*.md")))
    for path in targets:
        raw = open(path, encoding="utf-8").read()
        new = raw
        for key, rep in REPLACE.items():
            new = re.sub(r'("%s"\s*:\s*")[^"]*(")' % key, lambda m: m.group(1) + rep + m.group(2), new)
        # 文档里裸写的 couponCode / couponId
        new = re.sub(r"\bMCD[0-9A-Z]{10,}\b", "MCD000000000000000", new)
        new = re.sub(r"\b[A-F0-9]{32}\b(?=[^)]{0,40}(?:coupon|券))", "C0FFEE0000000000C0FFEE0000000000", new)
        # 手机号
        new = re.sub(r"(?<!\d)1[3-9](\d{9})(?!\d)", lambda m: "13****" + m.group(1)[-4:], new)
        if path.endswith(".md"):
            # 文档散文里的裸订单号/支付单号（18 位以上连续数字）
            def _num(m):
                v = m.group(0)
                return v if v.startswith("1110000000000000000") else "1030000000000000000000000001"
            new = re.sub(r"(?<!\d)\d{18,}(?!\d)", _num, new)
            # 反引号里的真实取餐码（5 位）
            new = re.sub(r"`(\d{5})`", "`00000`", new)
        if new != raw:
            open(path, "w", encoding="utf-8").write(new)
            changed.append(os.path.relpath(path, ROOT))
    # 索引里的订单号
    idx = os.path.join(ROOT, "references", "samples", "00-index.md")
    if os.path.exists(idx):
        raw = open(idx, encoding="utf-8").read()
        new = re.sub(r"(?<!\d)(10[0-9]{6})[0-9]{12,}(\d{4})(?!\d)", r"\1…\2", raw)
        if new != raw:
            open(idx, "w", encoding="utf-8").write(new)
            if "references/samples/00-index.md" not in changed:
                changed.append("references/samples/00-index.md")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true")
    a = ap.parse_args()

    before = scan()
    if a.fix:
        ch = fix_samples()
        print("已脱敏文件：")
        for c in ch:
            print("  -", c)
        after = scan()
    else:
        after = before

    print("\n剩余命中（%d 条）：" % len(after))
    if not after:
        print("  ✅ 干净：未发现 Token / 订单号 / 支付信息 / 取餐码 / 手机号 / 身份证 / 邮箱")
    else:
        for name, path, val in after[:60]:
            print("  [%s] %s  %s" % (name, path, val))
        if len(after) > 60:
            print("  … 其余 %d 条省略" % (len(after) - 60))
    return 0 if not after else 1


if __name__ == "__main__":
    sys.exit(main())

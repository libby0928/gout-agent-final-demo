#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
痛风智能体 Demo 一致性自检脚本 (lint-demo)
============================================

用途：
    把《痛风智能体Demo设计规范_AI执行版.md》里「可机器判定」的固定规则
    转成可重复运行的检查，替代每次改 Demo 都靠人工复述确认。
    改完任意 Demo 文件后跑一次，快速发现违反硬规则的地方。

运行：
    python3 design-system/lint-demo.py [文件或目录 ...]
    不传参时默认扫描 demos/ 与根目录 *.html。

检查范围（v2，5 类硬规则）：
    [A] 快速建档字段洁癖：只应含 姓名/性别/手机号，不应出现
        病种/年龄/身份证 等额外字段（针对快速建档表单区域）。
    [B] 禁用词：建档进度 / 报告解读 / AI诊室 / 等待医生确认(主按钮) /
        扫码签到 / 选择病种(必填) 等规范明确禁用的表达。
    [C] 图标规范：正式操作控件不得用单字占位图标（夹/期/单/医/药/尿/肾
        等作 <button>/<i>/class 含 icon 的元素文本），不得出现 emoji 图标。
    [D] 素材稳定性：不得引用临时路径（Downloads / 临时截图 / 个人本机
        路径 / 未入库 InCall 素材 / 外链易失图），应来自 assets/ 或内嵌。
    [E] 文档一致性：扫描 docs/ 下 md 文档，核对「逻辑基线」版本戳是否缺失/
        落后（方法 4 映射表），以及文档示例是否出现 [B] 禁用词（文档错词会
        传导到 Demo）。仅对 .md 生效，HTML 走 A~D。

输出：
    每个文件列出 [ERROR]/[WARN] 行号与说明；末尾汇总通过/问题数。
    退出码 0 = 无 ERROR；1 = 有 ERROR（可接 CI / 提交前钩子）。

注意：
    本脚本只覆盖「可机器判定」的硬规则。语义级检查（如阿福式氛围、
    同页入口去重、对话节奏）仍需人工或后续增强。规则源以
    docs/03-原型与规范/痛风智能体Demo设计规范_AI执行版.md 与
    docs/04-项目沉淀/INDEX.md 逻辑基线为准。
"""

import os
import re
import sys
import html

# ---------- 规则定义 ----------

# [A] 快速建档额外字段关键词（出现即疑似违规，需结合上下文）
BUILD_EXTRA_FIELDS = ["年龄", "身份证", "病种选择", "选择病种", "病种*"]

# [B] 禁用词（规范明确禁止的表达）
BANNED_PHRASES = {
    "建档进度": "应使用「档案完整度」",
    "报告解读": "应使用「上传报告」",
    "AI诊室": "不应作为独立模块/入口",
    "扫码签到": "应统一为「扫码就诊」",
    "等待医生确认": "患者端主按钮不应为「等待医生确认」",
}

# [C] 单字占位图标：作为按钮/图标元素唯一文本时的单字（业务编号/首字头像除外，靠元素类型判断）
SINGLE_CHAR_ICON_RE = re.compile(
    r"<(button|i|span|a)\b[^>]*\bclass=\"[^\"]*(icon|ui-icon|tab|nav)[^\"]*\"[^>]*>([一-龥])\s*</\1>",
    re.IGNORECASE,
)
# 语义型 emoji（规范禁止作功能图标占位）：麦克风/机器人/灯泡/手机/日历/沙漏 等
# 不含：纯装饰箭头(→↑▾⌄)、几何符号、字体图标私用区字符(♙ 等国际象棋符号属 icon-font 渲染)
SEMANTIC_EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\u231A\u231B\u23F0\u23F1\u23F2\u23F3"
    "\U0001F4F1\U0001F4C5\U0001F4C6\U0001F4DD\U0001F3A4\U0001F916\U0001F4E2\U0001F4AC"
    "\U0001F4A1\U0001F517]"
)

# [D] 临时/易失素材路径（非 VERBOSE，避免 * 量词误解析）
TEMP_PATH_RE = re.compile(
    r"""(?:src|href)\s*=\s*["'](?:\.{0,2}/)?"""
    r"""(?:/Users/|C:/|/home/|/tmp/|/Downloads/|Downloads/"""
    r"""|[^"']*?/临时|[^"']*?/temp/|[^"']*?截图|[^"']*?Playwright|[^"']*?playwright"""
    r"""|https?://(?!assets\.|localhost|raw\.github))""",
    re.IGNORECASE,
)


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def lint_file(path: str):
    issues = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception as e:
        return [("ERROR", 0, f"无法读取文件: {e}")]

    # 跳过 <script> 块：JS 代码里的 emoji/字符串不影响 UI 展示，不应被 UI 规范检查
    raw = re.sub(r"<script\b[^>]*>.*?</script>", "", raw, flags=re.DOTALL | re.IGNORECASE)
    lines = raw.splitlines()

    for idx, line in enumerate(lines, start=1):
        # [A] 快速建档额外字段
        # 规则本意：禁止「快速建档表单」出现姓名/性别/手机号以外的字段。
        # 已建档患者的「档案详情」(profile-form-card / profile-field 容器) 展示年龄/身份证/病案号是合规的，
        # 故仅在非档案详情行才报警；命中档案详情容器则跳过。
        in_profile_detail = ("profile-form-card" in line or "profile-field" in line
                             or "profile-two-col" in line)
        if not in_profile_detail:
            for kw in BUILD_EXTRA_FIELDS:
                if kw in line:
                    issues.append(("WARN", idx, f"[A] 快速建档疑似出现额外字段「{kw}」，确认是否在快速建档表单区域"))

        # [B] 禁用词
        for phrase, fix in BANNED_PHRASES.items():
            if phrase in line:
                issues.append(("ERROR", idx, f"[B] 禁用词「{phrase}」— {fix}"))

        # [C] 单字占位图标
        for m in SINGLE_CHAR_ICON_RE.finditer(line):
            ch = m.group(3)
            issues.append(("ERROR", idx, f"[C] 单字占位图标「{ch}」用作图标，应使用 SVG/CSS 图形"))

        # [C] 语义型 emoji 图标
        # icon font（class 含 ui-icon 或 aria-hidden 的元素内字符）属字体图标，非 emoji 占位，跳过避免误报。
        is_icon_font = ("ui-icon" in line or "aria-hidden" in line)
        if not is_icon_font:
            for em in SEMANTIC_EMOJI_RE.finditer(line):
                issues.append(("WARN", idx, f"[C] 出现语义 emoji「{em.group()}」作图标，确认非功能图标占位"))

        # [D] 临时路径
        for m in TEMP_PATH_RE.finditer(line):
            issues.append(("ERROR", idx, f"[D] 疑似引用临时/易失素材路径：{m.group(0)[:60]}"))

    return issues


# ---------- [E] 文档一致性检查 ----------

# 文档头部应声明的基线版本戳（方法 4 映射表要求每份沉淀文档标注）
BASELINE_STAMP_RE = re.compile(r"遵守逻辑基线\s*[vV]?(\d+(?:\.\d+)?)|基线版本\s*[vV]?(\d+(?:\.\d+)?)", re.IGNORECASE)
# INDEX 逻辑基线映射表里的"最近核对"日期列，落后此天数视为待复核
BASELINE_MAX_AGE_DAYS = 7


def _today():
    import datetime
    return datetime.date.today()


def lint_doc(path: str):
    """检查 docs/ 下的 md 文档一致性（[E] 类）。"""
    issues = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception as e:
        return [("ERROR", 0, f"无法读取文件: {e}")]

    lines = raw.splitlines()
    head = "\n".join(lines[:40])  # 只看头部 40 行声明区

    # [E-1] 版本戳缺失：沉淀文档（项目沉淀/原型规范类）应声明遵守基线版本
    is_settlement = ("项目沉淀" in path or "原型与规范" in path or "产品需求" in path)
    if is_settlement and not BASELINE_STAMP_RE.search(head):
        rel = os.path.relpath(path)
        issues.append(("WARN", 1, f"[E] 文档未声明「遵守逻辑基线 vX」版本戳，建议头部加一行声明，便于跨端一致性核查（{rel}）"))

    # [E-2] 文档示例出现 [B] 禁用词（错词会传导到 Demo）
    # 豁免：① 规范文件里"定义禁用词清单/反面示例"的段落本就在描述禁止项，属合规；
    #       ② 一行同时含否定语境词（禁止/不应/不得/避免/不要/禁止出现）时，视为规则说明而非违规示例。
    NEG_CTX = ("禁止", "不应", "不得", "避免", "不要", "禁止出现", "禁用", "反面", "NOT", "不可")
    is_rule_def_doc = ("Demo设计规范" in path or "复用规则" in path or "AI执行版" in path)
    for ln, line in enumerate(lines, start=1):
        # 跳过"禁用词定义表"区域：出现"禁用词"三字且本行在列举，通常同段已在说明规则
        if "禁用词" in line and ("：" in line or ":" in line or "清单" in line):
            continue
        has_neg = any(w in line for w in NEG_CTX)
        if has_neg:
            continue  # 否定语境下提到禁用词 = 规则说明，豁免
        for phrase, fix in BANNED_PHRASES.items():
            if phrase in line:
                # 规范定义文件整体豁免（其职责就是定义这些禁用项）
                if is_rule_def_doc:
                    continue
                issues.append(("WARN", ln, f"[E] 文档出现禁用词「{phrase}」— {fix}（文档示例错词易传导至 Demo）"))

    # [E-3] INDEX 映射表"最近核对"列过期（仅对 INDEX.md 自身）
    if os.path.basename(path) == "INDEX.md":
        today = _today()
        for ln, line in enumerate(lines, start=1):
            m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if m and "最近核对" not in line and "登记日期" not in line:
                continue
            if "最近核对" in line:
                dm = re.search(r"(\d{4}-\d{2}-\d{2})", line)
                if dm:
                    try:
                        d = datetime.date.fromisoformat(dm.group(1))
                        age = (today - d).days
                        if age > BASELINE_MAX_AGE_DAYS:
                            issues.append(("WARN", ln, f"[E] 逻辑基线映射表该行「最近核对」已 {age} 天未更新（>{BASELINE_MAX_AGE_DAYS}天），建议复核同步落点"))
                    except Exception:
                        pass

    return issues


def main(argv):
    roots = argv[1:] if len(argv) > 1 else None
    if not roots:
        here = os.path.dirname(os.path.abspath(__file__))
        repo = os.path.dirname(here)
        roots = [
            os.path.join(repo, "demos", "患者端"),
            os.path.join(repo, "demos", "医生端"),
            os.path.join(repo, "*.html"),
            os.path.join(repo, "docs"),  # v2 新增：文档一致性检查
        ]

    files = []
    import glob
    for r in roots:
        if os.path.isfile(r):
            files.append(r)
            continue
        if os.path.isdir(r):
            for root, _, fs in os.walk(r):
                for fn in fs:
                    if fn.endswith(".html") or fn.endswith(".md"):
                        files.append(os.path.join(root, fn))
            continue
        # 通配模式（如 *.html）
        for m in glob.glob(r):
            if m.endswith(".html") or m.endswith(".md"):
                files.append(m)

    # 去重
    files = sorted(set(files))
    if not files:
        print("未找到待检查的文件。")
        return 0

    total_err = 0
    total_warn = 0
    print("=" * 64)
    print("痛风智能体 一致性自检 (lint-demo v2)")
    print(f"检查文件数: {len(files)}")
    print("=" * 64)

    for fp in files:
        if fp.endswith(".md"):
            issues = lint_doc(fp)
        else:
            issues = lint_file(fp)
        errs = [i for i in issues if i[0] == "ERROR"]
        warns = [i for i in issues if i[0] == "WARN"]
        total_err += len(errs)
        total_warn += len(warns)
        rel = os.path.relpath(fp)
        print(f"\n📄 {rel}")
        if not issues:
            print("  ✅ 通过（无硬规则问题）")
        for level, ln, msg in issues:
            tag = "ERROR" if level == "ERROR" else "WARN "
            print(f"  [{tag}] L{ln}: {msg}")

    print("\n" + "=" * 64)
    print(f"汇总: ERROR={total_err}  WARN={total_warn}  文件={len(files)}")
    print("=" * 64)
    return 1 if total_err > 0 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

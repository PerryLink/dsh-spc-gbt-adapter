#!/usr/bin/env python3
"""README visuals for dsh-spc-gbt-adapter — drawn from this plugin's real pipeline.

Two figures, both derived from the shipped material rather than a shared
template:

  hero 1440x576 (Pillow, four files: zh/en x light/dark)
      Left column: plugin name, two value lines, the boundary sentence, meta and
      footer. Right side is the thing this plugin actually reads and returns: a
      control chart for ledger row 1 (`Xbar-R-001`, n = 5) whose centre line
      (10.0000) and limits (UCL 10.2885 / LCL 9.7115) are the numbers in
      `samples/quickstart/input/SP-001-unsafe.json`, with the coefficients the
      row is checked against (A2 / D3 / D4 on the n = 5 tier), then the two
      cards from that run: the SP-001 find (characteristic and chartType blank)
      and the SP-005 skip (threshold = 0, so the rule says so instead of
      passing), and the report line issues 1 · skipped 1.

  flow 1100x660 (hand-written SVG, two files)
      Not a left-to-right node chain. It is a confluence: the ledger channel
      and the rule-pack channel merge into one runTableCheck gate, the gate
      splits by "can this rule run at all?" into issues[] (executed) and
      skipped[] (reason stated), those two columns form one result ledger with
      the buildView projection, and a dashed return path carries a skipped
      reason back to the rule pack — swap rules/*.yaml or config and re-run,
      no TypeScript edit.

Every value below is copied from the repository:
  samples/quickstart/input/SP-001-unsafe.json  (Xbar-R-001, n=5, mean 10.00,
      R 0.50, CL 10.0000, UCL 10.2885, LCL 9.7115, USL 10.60, LSL 9.40)
  samples/quickstart/expected/result.json      (issueCount 1, skippedCount 1)
  rules/spc-gbt-adapter.yaml                   (SP-001..SP-007, A2/D3/D4 for
      n = 2..10, tolerance 0.005 / 0.02, threshold 0 = unset)
The plot points are illustrative (a ledger row carries one mean); they are
labelled as such and all sit inside the control limits, because this plugin
never judges whether the process is in control.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + fonts msyh.ttc / msyhbd.ttc / consola.ttf / consolab.ttf.
"""
from __future__ import annotations

import os
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

FONT_CJK = r"C:\Windows\Fonts\msyh.ttc"
FONT_CJK_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_MONO = r"C:\Windows\Fonts\consola.ttf"
FONT_MONO_BOLD = r"C:\Windows\Fonts\consolab.ttf"
for _path in (FONT_CJK, FONT_CJK_BOLD, FONT_MONO, FONT_MONO_BOLD):
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")

FONT_FILES = {"cjk": FONT_CJK, "cjk_bold": FONT_CJK_BOLD,
              "mono": FONT_MONO, "mono_bold": FONT_MONO_BOLD}
FONT_CSS_CJK = ("'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',"
                "'Source Han Sans SC',sans-serif")
FONT_CSS_MONO = "'Consolas','SFMono-Regular',Menlo,ui-monospace,monospace"

RADIUS = 22
SHADOW = 26

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", card_edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a",
        pill="#ece7f9", band="#f5f2fb", band_alt="#faf8fe", grid="#e7e4f0",
        mark="#b45309", mark_bg="#fdf3e9",
        shadow=(32, 26, 64), glow2="#7a68c9",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", card_edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950",
        pill="#242d42", band="#202839", band_alt="#1e2534", grid="#262f42",
        mark="#d9a441", mark_bg="#2a2216",
        shadow=(0, 0, 0), glow2="#8496f5",
    ),
}


def font(size, kind: str = "cjk_bold") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], int(size))


def hx(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, c1: str, c2: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    a, b = hx(c1), hx(c2)
    for y in range(h):
        t = 0.15 * (y / h) + 0.85 * (y / h) ** 1.35
        d.line([(0, y), (w, y)],
               fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: tuple,
         alpha: int = 40) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i in range(9, 0, -1):
        rr = r * i / 9
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=color + (int(alpha * (1 - i / 10)),))
    return Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")


def card(img: Image.Image, box: tuple, s: dict, radius: int = RADIUS,
         shadow: int = SHADOW, fill: str | None = None) -> Image.Image:
    """A soft-shadowed rounded card on the gradient background."""
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -3):
        sd.rounded_rectangle([x0 - i // 5, y0 + i // 2, x1 + i // 5, y1 + i],
                             radius=radius + i // 5,
                             fill=s["shadow"] + (int(9 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(s["card_edge"]), width=2)
    return base.convert("RGB")


_SCRATCH = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: float, kind: str) -> float:
    return _SCRATCH.textlength(text, font=font(size, kind))


def require_w(text: str, size: float, kind: str, max_w: float,
              what: str) -> None:
    """Fail loudly instead of shipping a clipped or overlapping label."""
    width = measure(text, size, kind)
    if width > max_w + 0.4:
        raise SystemExit(
            f"FATAL: {what} overflows: {text!r} needs {width:.1f}px > {max_w}px")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    size = start
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    raise SystemExit(
        f"FATAL: text does not fit {max_w}px at >= {minimum}px: {text!r}")


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    return min(fit(t, kind, max_w, start, minimum) for t in lines)


def pill(img: Image.Image, xy: tuple[int, int], text: str, s: dict,
         size: int = 16, fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> tuple[int, int]:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = size + 20
    d.rounded_rectangle([x, y, x + w + 30, y + h], radius=h // 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 15, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return int(x + w + 30), int(y + h)


def chip(img: Image.Image, xy: tuple[int, int], text: str, fg: str, bg: str,
         size: float = 11, kind: str = "cjk_bold", padx: int = 9,
         height: int = 20) -> int:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    d.rounded_rectangle([x, y, x + w + padx * 2, y + height],
                        radius=height // 2, fill=hx(bg))
    d.text((x + padx, y + height / 2), text, font=f, fill=hx(fg), anchor="lm")
    return int(w + padx * 2)


def dash_hline(d: ImageDraw.ImageDraw, x0: float, x1: float, y: float,
               color: str, width: int = 2, dash: int = 7, gap: int = 5) -> None:
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=hx(color), width=width)
        x += dash + gap


# --------------------------------------------------------------------------- hero
# Every technical value is an excerpt of this repository's own sample; see the
# module docstring for the file-by-file mapping.
LIMITS = dict(usl=10.60, ucl=10.2885, cl=10.0000, lcl=9.7115, lsl=9.40)
# Illustrative subgroup means: all inside UCL/LCL, because this plugin never
# rules on whether the process is in control.
POINTS = [10.02, 9.96, 10.07, 9.93, 10.03, 9.98, 10.05, 9.95]

HERO = {
    "zh": dict(
        name="dsh-spc-gbt-adapter",
        kicker="DeepSeek Harness 插件 · 控制图台账核查",
        value=["七条规则只核台账自身的算术", "差异落到行号与栏名"],
        sub=["控制限、中心线、Cp/Cpk 与子组档位逐项对照；",
             "不判过程是否受控，结论留给审核人。"],
        meta="SP-001…SP-007 · 规则包即数据 · skipped 逐条写明原因",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        chart_title="台账第 1 行 · Xbar-R-001",
        chart_chip="n = 5 · 只读",
        chart_meta="中心线 10.0000 · 规格限 10.60 / 9.40 · 常数表覆盖 n = 2…10",
        chart_caption="点位为示意，均落在控制限内——受控与否不由本插件判定。",
        const_title="coefficients",
        const_headers=["n", "A2", "D3", "D4"],
        const_rows=[(4, "0.729", "0", "2.282"),
                    (5, "0.577", "0", "2.114"),
                    (6, "0.483", "0", "2.004")],
        const_hl=5,
        const_formulas=["UCL = Xbar + A2·R", "LCL = Xbar − A2·R",
                        "R: D3·R … D4·R"],
        finding=dict(rule="SP-001", sev="warn",
                     locator="第 1 行 · characteristic / chartType",
                     found="characteristic、chartType 都为空",
                     expected="至少填写一项",
                     fix="补填后再核；不判图种是否选对"),
        skipped=dict(rule="SP-005", tag="skipped",
                     l1="threshold = 0 → 未配置",
                     l2="本条自报 skipped，并写明原因",
                     l3="接收准则不硬编码",
                     l4="空 issues ≠ 没问题"),
        strip_left="issues 1 · skipped 1",
        strip_right="结论不在报告里",
    ),
    "en": dict(
        name="dsh-spc-gbt-adapter",
        kicker="DeepSeek Harness plugin · control-chart ledger check",
        value=["Seven rules read one ledger", "each finding names its row"],
        sub=["Limits, centre line, Cp/Cpk, subgroup tiers —",
             "control status is never judged here."],
        meta="SP-001..SP-007 · rules are data · skips explained",
        foot="Apache-2.0 · PerryLink DSH plugin family",
        chart_title="Ledger row 1 · Xbar-R-001",
        chart_chip="n = 5 · read-only",
        chart_meta="centre 10.0000 · spec 10.60 / 9.40 · table covers n = 2…10",
        chart_caption="Points illustrative; control status is not judged here.",
        const_title="coefficients",
        const_headers=["n", "A2", "D3", "D4"],
        const_rows=[(4, "0.729", "0", "2.282"),
                    (5, "0.577", "0", "2.114"),
                    (6, "0.483", "0", "2.004")],
        const_hl=5,
        const_formulas=["UCL = Xbar + A2·R", "LCL = Xbar − A2·R",
                        "R chart: D3·R … D4·R"],
        finding=dict(rule="SP-001", sev="warn",
                     locator="row 1 · characteristic / chartType",
                     found="characteristic and chartType are blank",
                     expected="at least one must be filled",
                     fix="fill one; chart choice is not judged"),
        skipped=dict(rule="SP-005", tag="skipped",
                     l1="threshold = 0 → not configured",
                     l2="the rule reports itself in skipped",
                     l3="no hard-coded acceptance limit",
                     l4="an empty issue list is not a pass"),
        strip_left="issues 1 · skipped 1",
        strip_right="verdict stays with the reviewer",
    ),
}


def control_chart(img: Image.Image, s: dict, h: dict, skin: str) -> Image.Image:
    """The hero's right-hand chart: limits from row 1, plus the n = 5 tier."""
    px0, px1, py0, py1 = 724, 1114, 118, 292
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([px0 - 8, py0 - 6, px1 + 8, py1 + 8], radius=13,
                        fill=hx(s["band"]))

    vmin, vmax = 9.30, 10.70

    def y_of(v: float) -> float:
        return py1 - (v - vmin) / (vmax - vmin) * (py1 - py0)

    y_usl, y_ucl = y_of(LIMITS["usl"]), y_of(LIMITS["ucl"])
    y_cl, y_lcl = y_of(LIMITS["cl"]), y_of(LIMITS["lcl"])
    y_lsl = y_of(LIMITS["lsl"])

    # in-control band between the two control limits
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([px0, y_ucl, px1, y_lcl], radius=9,
                         fill=hx(s["accent"]) + (18 if skin == "light" else 30,))
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    d = ImageDraw.Draw(img)

    # spec limits (dashed, muted) and control limits (solid, accent)
    dash_hline(d, px0, px1, y_usl, s["faint"], 1, 6, 5)
    dash_hline(d, px0, px1, y_lsl, s["faint"], 1, 6, 5)
    d.line([(px0, y_ucl), (px1, y_ucl)], fill=hx(s["accent"]), width=2)
    d.line([(px0, y_lcl), (px1, y_lcl)], fill=hx(s["accent"]), width=2)
    dash_hline(d, px0, px1, y_cl, s["sub"], 2, 8, 5)

    # the series: illustrative subgroup means, joined
    step = (1030 - 744) / (len(POINTS) - 1)
    pts = [(744 + i * step, y_of(v)) for i, v in enumerate(POINTS)]
    d.line(pts, fill=hx(s["accent"]), width=2, joint="curve")
    for (x, y) in pts:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=hx(s["card"]))
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=hx(s["accent"]))

    # right-edge limit labels, knocked out of the band
    labels = [
        (f"USL {LIMITS['usl']:.2f}", y_usl, s["faint"]),
        (f"UCL {LIMITS['ucl']:.4f}", y_ucl, s["accent"]),
        (f"CL  {LIMITS['cl']:.4f}", y_cl, s["sub"]),
        (f"LCL {LIMITS['lcl']:.4f}", y_lcl, s["accent"]),
        (f"LSL {LIMITS['lsl']:.2f}", y_lsl, s["faint"]),
    ]
    for text, y, color in labels:
        w = measure(text, 10, "mono")
        d.rounded_rectangle([1108 - w - 8, y - 9, 1110, y + 5], radius=4,
                            fill=hx(s["band"]))
        d.text((1104, y + 4), text, font=font(10, "mono"), fill=hx(color),
               anchor="rs")

    # coefficients panel on the same card: the tier this row is checked against
    d.line([(1124, py0 - 2), (1124, py1 + 2)], fill=hx(s["grid"]), width=1)
    d.text((1140, 140), h["const_title"], font=font(11.5, "cjk_bold"),
           fill=hx(s["accent"]))
    cols = [1140, 1178, 1236, 1292]
    for x, head in zip(cols, h["const_headers"]):
        d.text((x, 164), head, font=font(10, "mono"), fill=hx(s["faint"]))
    row_y = {4: 188, 5: 212, 6: 236}
    hl = h["const_hl"]
    d.rounded_rectangle([1132, row_y[hl] - 15, 1352, row_y[hl] + 7], radius=7,
                        fill=hx(s["band_alt"]))
    d.rounded_rectangle([1132, row_y[hl] - 15, 1136, row_y[hl] + 7], radius=2,
                        fill=hx(s["accent"]))
    for n, a2, d3, d4 in h["const_rows"]:
        color = s["text"] if n == hl else s["sub"]
        for x, value in zip(cols, (str(n), a2, d3, d4)):
            d.text((x, row_y[n]), value, font=font(11.5, "mono"),
                   fill=hx(color))
    for i, formula in enumerate(h["const_formulas"]):
        d.text((1140, 266 + i * 16), formula, font=font(10.5, "mono"),
               fill=hx(s["faint"]), )
    return img


def hero(lang: str, skin: str) -> None:
    s, h = SKIN[skin], HERO[lang]
    W, HT = 1440, 576
    img = gradient(W, HT, s["bg_from"], s["bg_to"])
    img = glow(img, 1180, 30, 420, hx(s["accent"]),
               24 if skin == "light" else 38)
    img = glow(img, 90, 580, 300, hx(s["glow2"]),
               10 if skin == "light" else 16)

    d = ImageDraw.Draw(img)
    m, col_w = 64, 596

    # ---- left column: kicker / title / value / sub / meta / footer -----------
    pill(img, (m, 56), h["kicker"], s, size=17)
    d = ImageDraw.Draw(img)

    title_size = fit(h["name"], "mono_bold", col_w, 58, 48)
    d.text((m - 2, 118), h["name"], font=font(title_size, "mono_bold"),
           fill=hx(s["text"]))

    value_size = fit_lines(h["value"], "cjk_bold", col_w, 42, 34)
    for i, line in enumerate(h["value"]):
        d.text((m, 204 + i * 56), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]))

    for i, line in enumerate(h["sub"]):
        require_w(line, 22, "cjk", col_w, "hero sub")
        d.text((m + 1, 334 + i * 34), line, font=font(22, "cjk"),
               fill=hx(s["sub"]))

    require_w(h["meta"], 19, "cjk", col_w, "hero meta")
    require_w(h["foot"], 16, "cjk", col_w, "hero footer")
    d.text((m + 1, 428), h["meta"], font=font(19, "cjk"), fill=hx(s["faint"]))
    d.line([m + 1, 480, m + col_w - 4, 480], fill=hx(s["grid"]), width=2)
    d.text((m + 1, 494), h["foot"], font=font(16, "cjk"), fill=hx(s["faint"]))

    # ---- right: the chart card ---------------------------------------------
    img = card(img, (700, 40, 1376, 324), s, radius=RADIUS, shadow=SHADOW)
    d = ImageDraw.Draw(img)
    d.text((724, 64), h["chart_title"], font=font(17, "cjk_bold"),
           fill=hx(s["accent"]))
    chip_w = measure(h["chart_chip"], 11, "cjk")
    chip(img, (1352 - int(chip_w) - 18, 54), h["chart_chip"], s["accent"],
         s["pill"], size=11)
    d = ImageDraw.Draw(img)
    require_w(h["chart_meta"], 11.5, "cjk", 520, "chart meta")
    d.text((724, 92), h["chart_meta"], font=font(11.5, "cjk"),
           fill=hx(s["sub"]))
    require_w(h["chart_caption"], 10.5, "cjk", 400, "chart caption")
    d.text((724, 315), h["chart_caption"], font=font(10.5, "cjk"),
           fill=hx(s["sub"]))
    img = control_chart(img, s, h, skin)

    # ---- right: the two cards from the same run -----------------------------
    img = card(img, (700, 340, 1032, 492), s, radius=18, shadow=20)
    d = ImageDraw.Draw(img)
    f = h["finding"]
    d.text((722, 362), f["rule"], font=font(13.5, "mono_bold"),
           fill=hx(s["accent"]))
    w = measure(f["rule"], 13.5, "mono_bold")
    chip(img, (722 + int(w) + 8, 356), f["sev"], s["accent"], s["pill"],
         size=10)
    d = ImageDraw.Draw(img)
    d.text((1010, 362), "issues[]", font=font(10.5, "mono"),
           fill=hx(s["faint"]), anchor="rs")
    for key, y, size, kind, fill in (
            ("locator", 390, 11.5, "cjk", s["sub"]),
            ("found", 416, 12.5, "cjk", s["text"]),
            ("expected", 440, 11.5, "cjk", s["sub"]),
            ("fix", 462, 11, "cjk", s["faint"])):
        require_w(f[key], size, kind, 288, f"hero finding {key}")
        d.text((722, y), f[key], font=font(size, kind), fill=hx(fill))

    img = card(img, (1044, 340, 1376, 492), s, radius=18, shadow=20)
    d = ImageDraw.Draw(img)
    k = h["skipped"]
    d.text((1066, 362), k["rule"], font=font(13.5, "mono_bold"),
           fill=hx(s["sub"]))
    w = measure(k["rule"], 13.5, "mono_bold")
    chip(img, (1066 + int(w) + 8, 356), k["tag"], s["sub"], s["pill"], size=10)
    d = ImageDraw.Draw(img)
    d.text((1354, 362), "skipped[]", font=font(10.5, "mono"),
           fill=hx(s["faint"]), anchor="rs")
    for key, y, size, kind, fill in (
            ("l1", 390, 11.5, "cjk", s["sub"]),
            ("l2", 414, 12, "cjk", s["text"]),
            ("l3", 438, 11.5, "cjk", s["sub"]),
            ("l4", 460, 11, "cjk", s["faint"])):
        require_w(k[key], size, kind, 288, f"hero skipped {key}")
        d.text((1066, y), k[key], font=font(size, kind), fill=hx(fill))

    # ---- report line --------------------------------------------------------
    img = card(img, (700, 504, 1376, 548), s, radius=18, shadow=16)
    d = ImageDraw.Draw(img)
    d.text((724, 518), h["strip_left"], font=font(13.5, "mono"),
           fill=hx(s["text"]))
    require_w(h["strip_right"], 13.5, "cjk_bold", 330, "hero strip right")
    rw = measure(h["strip_right"], 13.5, "cjk_bold")
    d.text((1352 - rw, 518), h["strip_right"], font=font(13.5, "cjk_bold"),
           fill=hx(s["accent2"]))
    used = measure(h["strip_left"], 13.5, "mono") + rw + 40
    if used > 628:
        raise SystemExit(f"FATAL: hero report strip overflows ({used:.1f}px)")

    name = f"dsh-spc-gbt-adapter-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name} ({W}×{HT})")


# --------------------------------------------------------------------------- flow
FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", edge="#e6e2ef", band="#f5f2fb", band_alt="#faf8fe",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", accent2="#16a34a", rule="#dcd8ea",
        card="#ffffff", shadow="0.10",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", edge="#2e374b", band="#202839", band_alt="#1e2534",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", accent2="#3fb950", rule="#2b3348",
        card="#1b2231", shadow="0.45",
    ),
}


class Svg:
    """Tiny SVG writer that measures every label before it is emitted."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.overflows: list[str] = []

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def text(self, x: float, y: float, content: str, size: float, fill: str, *,
             anchor: str = "start", weight: int | None = None,
             mono: bool = False, max_w: float | None = None,
             opacity: float | None = None) -> None:
        kind = "mono" if mono else "cjk"
        if weight:
            kind += "_bold"
        if max_w is not None:
            w = measure(content, size, kind)
            if w > max_w + 0.4:
                self.overflows.append(f"{content!r} needs {w:.1f}px > {max_w}px")
        family = FONT_CSS_MONO if mono else FONT_CSS_CJK
        attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
                 f'font-family="{family}"', f'font-size="{size}"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<text {" ".join(attrs)}>{escape(content)}</text>')

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1.5,
             shadow: bool = False, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
        if rx:
            attrs.append(f'rx="{rx}"')
        attrs.append(f'fill="{fill}"')
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1.5, dash: str | None = None,
             marker: str | None = None, opacity: float | None = None) -> None:
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def path(self, d: str, *, stroke: str, sw: float = 1.5,
             marker: str | None = None, dash: str | None = None,
             fill: str = "none") -> None:
        attrs = [f'd="{d}"', f'fill="{fill}"', f'stroke="{stroke}"',
                 f'stroke-width="{sw}"', 'stroke-linecap="round"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if marker:
            attrs.append(f'marker-end="url(#{marker})"')
        self.add(f'<path {" ".join(attrs)}/>')

    def circle(self, cx: float, cy: float, r: float, *, fill: str,
               stroke: str | None = None, sw: float = 1.5) -> None:
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if stroke:
            attrs.append(f'stroke="{stroke}"')
            attrs.append(f'stroke-width="{sw}"')
        self.add(f'<circle {" ".join(attrs)}/>')

    def chip(self, x_right: float, y: float, label: str, fg: str, bg: str, *,
             size: float = 11, pad: float = 9, height: float = 20,
             mono: bool = False, weight: int | None = None) -> float:
        """A pill anchored on its right edge; returns its left edge."""
        kind = "mono" if mono else "cjk"
        if weight:
            kind += "_bold"
        w = measure(label, size, kind) + pad * 2
        x = x_right - w
        self.rect(x, y, w, height, fill=bg, rx=height / 2)
        self.text(x + pad, y + height / 2 + size * 0.34, label, size, fg,
                  weight=weight, mono=mono)
        return x

    def svg(self, w: int, h: int, label: str) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-label="{escape(label)}">')
        return "\n".join([head, *self.parts, "</svg>"]) + "\n"


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    W, H = 1100, 660
    v = Svg()

    v.add("<defs>")
    v.add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.3" y2="1">'
          f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
          f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    v.add(f'<filter id="soft" x="-30%" y="-30%" width="160%" height="170%">'
          f'<feDropShadow dx="0" dy="7" stdDeviation="9" '
          f'flood-color="#16122c" flood-opacity="{s["shadow"]}"/></filter>')
    v.add('<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
          'markerWidth="6.4" markerHeight="6.4" orient="auto-start-reverse">'
          f'<path d="M0 0 L10 5 L0 10 z" fill="{s["accent"]}"/></marker>')
    v.add("</defs>")
    v.add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

    # ---- header -------------------------------------------------------------
    v.text(44, 58, "dsh-spc-gbt-adapter", 26, s["text"], weight=700, mono=True,
           max_w=620)
    v.text(44, 86, "台账与规则库两条通道汇流成一次核对：先问这条规则能不能跑，"
                   "再分流成 issues 与 skipped。", 14.5, s["sub"], max_w=840)
    v.chip(1056, 34, "规则库 2026.1 · 7 条", s["accent"], s["band"],
           size=12, pad=12, height=26)

    # ---- two input channels -------------------------------------------------
    v.rect(44, 110, 492, 150, fill=s["panel"], rx=18, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.circle(70, 136, 11, fill=s["accent"])
    v.text(70, 140, "1", 12, s["panel"], anchor="middle", weight=700, mono=True)
    v.text(92, 142, "台账 material", 16, s["text"], weight=700, max_w=250)
    v.chip(520, 124, "file | material", s["accent"], s["band"], size=10.5,
           height=22)
    v.text(64, 182, "parseMaterial · 列别名归一 → characteristic / chartType / n",
           12, s["sub"], max_w=456)
    v.text(64, 206, "只读：不写回、不移动、不删除原件", 12, s["faint"],
           max_w=456)
    v.text(64, 230, "缺项按字段可选处理：报差异，不让程序崩溃", 12, s["faint"],
           max_w=456)

    v.rect(564, 110, 492, 150, fill=s["panel"], rx=18, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.circle(590, 136, 11, fill=s["accent"])
    v.text(590, 140, "2", 12, s["panel"], anchor="middle", weight=700, mono=True)
    v.text(612, 142, "规则库 rulesFile", 16, s["text"], weight=700, max_w=250)
    v.chip(1040, 124, "rules/*.yaml", s["accent"], s["band"], size=10.5,
           height=22)
    v.text(584, 182, "rules/spc-gbt-adapter.yaml · SP-001 … SP-007", 12,
           s["sub"], mono=True, max_w=450)
    v.text(584, 206, "loadRulesetFile：document / number / clause / excerpt / source",
           12, s["faint"], max_w=450)
    v.text(584, 230, "severity 跟着证据走：原则性 ≤ warn、机构配置 ≤ info", 12,
           s["faint"], max_w=450)

    # ---- confluence into the gate ------------------------------------------
    v.path("M290 262 V274 Q290 283 299 283 H546",
           stroke=s["accent"], sw=1.8)
    v.path("M810 262 V274 Q810 283 801 283 H554",
           stroke=s["accent"], sw=1.8)
    v.circle(550, 283, 4, fill=s["accent"])
    v.line(550, 285, 550, 296, stroke=s["accent"], sw=1.8, marker="arr")

    v.add(f'<path d="M550 296 L678 354 L550 412 L422 354 Z" fill="{s["card"]}" '
          f'stroke="{s["accent"]}" stroke-width="2" filter="url(#soft)"/>')
    v.text(550, 350, "runTableCheck", 13.5, s["accent"], anchor="middle",
           weight=700, mono=True, max_w=200)
    v.text(550, 370, "配置与列齐备？未被过滤？", 12, s["sub"], anchor="middle",
           max_w=190)

    # ---- split by "could this rule run at all?" ------------------------------
    v.line(550, 412, 550, 424, stroke=s["accent"], sw=1.8)
    v.line(290, 424, 810, 424, stroke=s["accent"], sw=1.8)
    v.line(290, 424, 290, 436, stroke=s["accent"], sw=1.8, marker="arr")
    v.line(810, 424, 810, 436, stroke=s["accent"], sw=1.8, marker="arr")

    # ---- one ledger with the two channels -----------------------------------
    v.rect(44, 440, 1012, 172, fill=s["panel"], rx=20, stroke=s["edge"],
           sw=1.5, shadow=True)
    v.text(64, 470, "结果账本", 14, s["text"], weight=700, max_w=160)
    v.text(1036, 470, "issues[] 与 skipped[] 一起读", 11, s["faint"],
           anchor="end", max_w=240)
    v.line(543, 484, 543, 568, stroke=s["rule"], sw=1, dash="5 5")

    v.text(64, 498, "已执行 → issues[]", 13.5, s["accent"], weight=700,
           max_w=300)
    v.chip(528, 486, "1 条", s["accent"], s["band"], size=10.5, height=20)
    v.text(64, 524, "SP-001 · warn · row 1 · characteristic", 12.5, s["text"],
           mono=True, max_w=460)
    v.text(64, 546, "found：characteristic、chartType 都为空", 12.5, s["text"],
           max_w=460)
    v.text(64, 566, "expected：至少填一项 · fix：补填后再核", 11.5, s["sub"],
           max_w=460)

    v.text(556, 498, "未执行 → skipped[]", 13.5, s["sub"], weight=700,
           max_w=340)
    v.chip(1036, 486, "1 条", s["sub"], s["band"], size=10.5, height=20)
    v.text(556, 524, "SP-005 · threshold = 0 → 未配置", 12.5, s["text"],
           max_w=460)
    v.text(556, 546, "reason：接收准则因行业、顾客而异", 12.5, s["text"],
           max_w=460)
    v.text(556, 566, "空 issues ≠ 没问题：先看 skippedCount", 11.5, s["faint"],
           max_w=460)

    # buildView projection strip
    v.rect(64, 574, 996, 22, fill=s["band"], rx=11)
    v.text(76, 590,
           "buildView → issueCount · skippedCount · summary{error,warn,info} · "
           "markdown · reportJson", 10.5, s["sub"], mono=True, max_w=700)
    v.text(1036, 590, "结论不在报告里", 11.5, s["accent2"], anchor="end",
           weight=700, max_w=120)

    # ---- return path: a skipped reason goes back to the rule pack -----------
    v.path("M1040 438 V264", stroke=s["sub"], sw=1.6, dash="6 5", marker="arr")
    v.text(1024, 350, "改 rules/*.yaml 或 config → 重跑", 11.5, s["faint"],
           anchor="end", max_w=300)

    # ---- footer -------------------------------------------------------------
    v.text(44, 628,
           "config：rulesFile · disabledRules · onlyRules · skipNotes · "
           "timeoutMs ｜ 只读材料 · 无网络 · 不调用模型",
           11, s["sub"], max_w=1012)
    v.text(44, 648,
           "只核对表内算术与常数一致性：不判过程受控，也不判能力是否充分；"
           "结论留给审核人。", 11, s["faint"], max_w=1012)

    if v.overflows:
        raise SystemExit("FATAL: SVG label overflow:\n  "
                         + "\n  ".join(v.overflows))
    return v.svg(W, H,
                 "dsh-spc-gbt-adapter 结构图：台账与规则库两条通道汇入 "
                 "runTableCheck 门控，按能否执行分流成 issues[] 与 skipped[] 两栏，"
                 "合成同一本结果账本并投影为报告；skipped 的原因可回到规则库重跑")


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
    for skin in ("light", "dark"):
        name = f"dsh-spc-gbt-adapter-flow-v5-{skin}.svg"
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(flow_svg(skin))
        print(f"wrote {name} (1100×660)")


if __name__ == "__main__":
    main()

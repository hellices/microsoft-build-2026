#!/usr/bin/env python3
"""Render Excalidraw (.excalidraw) JSON files to PNG with Pillow.

브라우저/cairo/SVG 없이, .excalidraw 의 rectangle/ellipse/diamond/text/arrow/line
요소를 직접 그려 동일 basename 의 .png 를 같은 폴더에 생성한다.
한글 라벨은 Windows 의 malgun.ttf 로 렌더링한다.

사용:
    python tools/render_excalidraw_png.py                 # 기본 5개 세션 다이어그램
    python tools/render_excalidraw_png.py path/a.excalidraw path/b.excalidraw
"""
from __future__ import annotations

import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

SCALE = 2          # supersample factor for crisp output
PAD = 24           # logical padding around content
BG = (255, 255, 255)

# ── font resolution (Korean-capable) ─────────────────────────────────────
_FONT_CANDIDATES = [
    r"C:\Windows\Fonts\malgun.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
]
_FONT_PATH = next((p for p in _FONT_CANDIDATES if os.path.exists(p)), None)
_font_cache: dict[int, ImageFont.FreeTypeFont] = {}


def _font(size_px: int) -> ImageFont.FreeTypeFont:
    key = max(8, int(size_px))
    if key not in _font_cache:
        if _FONT_PATH:
            _font_cache[key] = ImageFont.truetype(_FONT_PATH, key)
        else:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]


def _color(value, default=None):
    if value in (None, "transparent"):
        return default
    return value


def _abs_points(el):
    x, y = el["x"], el["y"]
    return [(x + px, y + py) for px, py in el.get("points", [])]


def _bounds(elements):
    xs, ys = [], []
    for el in elements:
        if el.get("isDeleted"):
            continue
        t = el["type"]
        if t in ("arrow", "line"):
            for px, py in _abs_points(el):
                xs.append(px)
                ys.append(py)
        else:
            xs += [el["x"], el["x"] + el.get("width", 0)]
            ys += [el["y"], el["y"] + el.get("height", 0)]
    if not xs:
        return 0, 0, 800, 600
    return min(xs), min(ys), max(xs), max(ys)


def _draw_text(draw, el, tf):
    text = el.get("text", "")
    if not text:
        return
    fill = _color(el.get("strokeColor"), "#1e1e1e")
    fs = el.get("fontSize", 16) * SCALE
    font = _font(fs)
    line_h = fs * el.get("lineHeight", 1.25)
    align = el.get("textAlign", "left")
    x, y = tf(el["x"], el["y"])
    w = el.get("width", 0) * SCALE
    for i, line in enumerate(text.split("\n")):
        ly = y + i * line_h
        if align == "center":
            anchor = "ma"
            lx = x + w / 2
        elif align == "right":
            anchor = "ra"
            lx = x + w
        else:
            anchor = "la"
            lx = x
        draw.text((lx, ly), line, font=font, fill=fill, anchor=anchor)


def _draw_box(draw, el, tf):
    x0, y0 = tf(el["x"], el["y"])
    x1, y1 = tf(el["x"] + el["width"], el["y"] + el["height"])
    fill = _color(el.get("backgroundColor"))
    outline = _color(el.get("strokeColor"), "#1e1e1e")
    width = max(1, round(el.get("strokeWidth", 1.5) * SCALE))
    t = el["type"]
    if t == "rectangle":
        radius = 12 * SCALE if el.get("roundness") else 0
        draw.rounded_rectangle([x0, y0, x1, y1], radius=radius,
                               fill=fill, outline=outline, width=width)
    elif t == "ellipse":
        draw.ellipse([x0, y0, x1, y1], fill=fill, outline=outline, width=width)
    elif t == "diamond":
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        draw.polygon([(mx, y0), (x1, my), (mx, y1), (x0, my)],
                     fill=fill, outline=outline, width=width)


def _draw_arrow(draw, el, tf):
    pts = [tf(px, py) for px, py in _abs_points(el)]
    if len(pts) < 2:
        return
    color = _color(el.get("strokeColor"), "#1e1e1e")
    width = max(1, round(el.get("strokeWidth", 1.5) * SCALE))
    draw.line(pts, fill=color, width=width, joint="curve")
    if el.get("endArrowhead") == "arrow" or el["type"] == "arrow":
        (xe, ye), (xp, yp) = pts[-1], pts[-2]
        ang = math.atan2(ye - yp, xe - xp)
        size = 12 * SCALE
        spread = math.radians(24)
        left = (xe - size * math.cos(ang - spread), ye - size * math.sin(ang - spread))
        right = (xe - size * math.cos(ang + spread), ye - size * math.sin(ang + spread))
        draw.polygon([(xe, ye), left, right], fill=color)


def render(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    elements = [e for e in doc.get("elements", []) if not e.get("isDeleted")]
    minx, miny, maxx, maxy = _bounds(elements)

    def tf(x, y):
        return ((x - minx + PAD) * SCALE, (y - miny + PAD) * SCALE)

    w = int((maxx - minx + 2 * PAD) * SCALE)
    h = int((maxy - miny + 2 * PAD) * SCALE)
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    # pass 1: boxes, pass 2: arrows, pass 3: text (text on top)
    for el in elements:
        if el["type"] in ("rectangle", "ellipse", "diamond"):
            _draw_box(draw, el, tf)
    for el in elements:
        if el["type"] in ("arrow", "line"):
            _draw_arrow(draw, el, tf)
    for el in elements:
        if el["type"] == "text":
            _draw_text(draw, el, tf)

    out = os.path.splitext(path)[0] + ".png"
    img.save(out)
    print("rendered", out, f"({w}x{h})")
    return out


_ROOT = os.path.join(os.path.dirname(__file__), "..", "docs", "sessions")
_DEFAULT = [
    "BRK243-claw-agent-harness-microsoft-foundry/foundry-harness-architecture.excalidraw",
    "BRK246-foundry-iq-enterprise-knowledge-agentic-retrieval/agentic-retrieval-architecture.excalidraw",
    "BRK250-observe-control-agents-open-source-tools/eval-control-pipeline.excalidraw",
    "BRK251-build-secure-enterprise-ready-agents-agent-365/agent-365-control-plane.excalidraw",
    "DEMSP390-create-multimodal-ai-agents-persistent-memory/omniagent-architecture.excalidraw",
    "KEY01-microsoft-build-opening-keynote/frontier-intelligence-stack.excalidraw",
    "DEM330-build-multimodal-agents-reason-interact-act/voice-live-agent-architecture.excalidraw",
    "BRK252-observability-to-roi-ai-agents/observability-to-roi-pipeline.excalidraw",
    "DEM368-R1-data-science-machine-learning-microsoft-fabric/fabric-ds-ml-lifecycle.excalidraw",
]


def main() -> None:
    args = sys.argv[1:]
    targets = args or [os.path.join(_ROOT, p) for p in _DEFAULT]
    for t in targets:
        render(t)


if __name__ == "__main__":
    main()

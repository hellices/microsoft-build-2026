"""Generate Excalidraw JSON diagrams for BRK240 session note.

Architecture-style diagrams (not tables): mixes ellipse / diamond / cylinder /
cloud shapes, hub-and-spoke layouts, multi-segment routed arrows.

Run from the repo root:
    python tools/gen_brk240_diagrams.py
"""
import json
import math
import os
import random

OUT_DIR = os.path.join("docs", "sessions", "BRK240-build-context-aware-agents")

random.seed(20260622)


# ---------------------------------------------------------------------
# Excalidraw primitives
# ---------------------------------------------------------------------
def _id():
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16))


def _common(extra=None):
    base = {
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": random.randint(1, 2**31),
        "version": 1,
        "versionNonce": random.randint(1, 2**31),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
    }
    if extra:
        base.update(extra)
    return base


def _shape(kind, x, y, w, h, bg="transparent", stroke="#1e1e1e",
           stroke_width=2, dashed=False, rounded=False):
    extra = {
        "backgroundColor": bg,
        "strokeColor": stroke,
        "strokeWidth": stroke_width,
        "strokeStyle": "dashed" if dashed else "solid",
        "fillStyle": "solid",
    }
    if rounded:
        extra["roundness"] = {"type": 3}
    return {
        "id": _id(),
        "type": kind,
        "x": x, "y": y, "width": w, "height": h,
        **_common(extra),
    }


def rect(x, y, w, h, **kw):
    return _shape("rectangle", x, y, w, h, **kw)


def ellipse(x, y, w, h, **kw):
    return _shape("ellipse", x, y, w, h, **kw)


def diamond(x, y, w, h, **kw):
    return _shape("diamond", x, y, w, h, **kw)


def text(x, y, label, size=16, align="center", w=None, color="#1e1e1e"):
    char_w = size * 0.6
    longest = max((len(line) for line in label.split("\n")), default=1)
    if w is None:
        w = max(40, int(longest * char_w) + 8)
    lines = label.count("\n") + 1
    h = int(size * 1.25 * lines)
    return {
        "id": _id(),
        "type": "text",
        "x": x, "y": y, "width": w, "height": h,
        **_common({
            "strokeColor": color,
            "text": label,
            "fontSize": size,
            "fontFamily": 1,
            "textAlign": align,
            "verticalAlign": "top",
            "baseline": int(size * 0.9),
            "containerId": None,
            "originalText": label,
            "lineHeight": 1.25,
        }),
    }


def centered_text(cx, cy, label, size=14, color="#1e1e1e"):
    char_w = size * 0.6
    longest = max((len(line) for line in label.split("\n")), default=1)
    w = max(40, int(longest * char_w) + 8)
    lines = label.count("\n") + 1
    h = int(size * 1.25 * lines)
    return text(cx - w // 2, cy - h // 2, label, size=size, w=w, color=color)


def labeled_rect(x, y, w, h, label, bg="#ffffff", size=14, rounded=True,
                 stroke="#1e1e1e", stroke_width=2, dashed=False):
    s = rect(x, y, w, h, bg=bg, rounded=rounded, stroke=stroke,
             stroke_width=stroke_width, dashed=dashed)
    if label:
        return [s, centered_text(x + w // 2, y + h // 2, label, size=size)]
    return [s]


def labeled_ellipse(x, y, w, h, label, bg="#ffffff", size=14,
                    stroke="#1e1e1e", stroke_width=2):
    s = ellipse(x, y, w, h, bg=bg, stroke=stroke, stroke_width=stroke_width)
    return [s, centered_text(x + w // 2, y + h // 2, label, size=size)]


def labeled_diamond(x, y, w, h, label, bg="#ffffff", size=14,
                    stroke="#1e1e1e", stroke_width=2):
    s = diamond(x, y, w, h, bg=bg, stroke=stroke, stroke_width=stroke_width)
    return [s, centered_text(x + w // 2, y + h // 2, label, size=size)]


def cylinder(x, y, w, h, label, bg="#ffffff", size=13, stroke="#1e1e1e"):
    """Database cylinder = top ellipse + body rect + bottom arc."""
    cap = max(14, int(h * 0.18))
    els = []
    # body rect (between cap centers)
    els.append(rect(x, y + cap // 2, w, h - cap, bg=bg, stroke=stroke,
                    stroke_width=2, rounded=False))
    # top ellipse (full)
    els.append(ellipse(x, y, w, cap, bg=bg, stroke=stroke, stroke_width=2))
    # bottom ellipse — full, then cover top half with body bg to fake arc
    els.append(ellipse(x, y + h - cap, w, cap, bg=bg, stroke=stroke,
                       stroke_width=2))
    els.append(rect(x + 2, y + h - cap, w - 4, cap // 2 + 1, bg=bg,
                    stroke=bg, stroke_width=0, rounded=False))
    els.append(centered_text(x + w // 2, y + h // 2 + 2, label, size=size))
    return els


def cloud(cx, cy, w, h, label, bg="#ffffff", size=14, stroke="#1e1e1e"):
    """Cloud shape — overlapping ellipses."""
    els = []
    bw, bh = int(w * 0.6), int(h * 0.55)
    els.append(ellipse(cx - bw // 2, cy - bh // 2, bw, bh,
                       bg=bg, stroke=stroke, stroke_width=2))
    bump_w = int(w * 0.35)
    bump_h = int(h * 0.45)
    els.append(ellipse(cx - int(w * 0.42), cy - int(h * 0.05),
                       bump_w, bump_h, bg=bg, stroke=stroke, stroke_width=2))
    els.append(ellipse(cx + int(w * 0.07), cy - int(h * 0.05),
                       bump_w, bump_h, bg=bg, stroke=stroke, stroke_width=2))
    els.append(ellipse(cx - int(w * 0.15), cy - int(h * 0.30),
                       bump_w, bump_h, bg=bg, stroke=stroke, stroke_width=2))
    # cover internal seams
    els.append(ellipse(cx - bw // 2 + 6, cy - bh // 2 + 6,
                       bw - 12, bh - 12, bg=bg, stroke=bg, stroke_width=0))
    els.append(centered_text(cx, cy, label, size=size))
    return els


# ---------------------------------------------------------------------
# Arrows
# ---------------------------------------------------------------------
def _arrow_points(points, **style):
    x0, y0 = points[0]
    rel = [[px - x0, py - y0] for (px, py) in points]
    xs = [p[0] for p in rel]
    ys = [p[1] for p in rel]
    w = max(xs) - min(xs)
    h = max(ys) - min(ys)
    return {
        "id": _id(),
        "type": "arrow",
        "x": x0, "y": y0, "width": w, "height": h,
        **_common({
            "strokeColor": style.get("stroke", "#1e1e1e"),
            "strokeStyle": "dashed" if style.get("dashed") else "solid",
            "strokeWidth": style.get("stroke_width", 2),
            "points": rel,
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": style.get("start_arrow"),
            "endArrowhead": None if style.get("no_end") else "arrow",
        }),
    }


def arrow(x1, y1, x2, y2, label=None, label_size=12, **style):
    els = [_arrow_points([(x1, y1), (x2, y2)], **style)]
    if label:
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2 - 16
        els.append(centered_text(mx, my, label, size=label_size,
                                 color=style.get("stroke", "#1e1e1e")))
    return els


def routed_arrow(points, label=None, label_at=None, label_size=12, **style):
    els = [_arrow_points(points, **style)]
    if label:
        if label_at is None:
            best, best_idx = 0, 0
            for i in range(len(points) - 1):
                dx = points[i + 1][0] - points[i][0]
                dy = points[i + 1][1] - points[i][1]
                d = dx * dx + dy * dy
                if d > best:
                    best, best_idx = d, i
            x = (points[best_idx][0] + points[best_idx + 1][0]) // 2
            y = (points[best_idx][1] + points[best_idx + 1][1]) // 2 - 16
        else:
            x, y = label_at
        els.append(centered_text(x, y, label, size=label_size,
                                 color=style.get("stroke", "#1e1e1e")))
    return els


def title(x, y, label, size=22, color="#1e1e1e"):
    return text(x, y, label, size=size, align="left", color=color)


def save(name, elements):
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://github.com/hellices/microsoft-build-2026",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"wrote {path}")


# ---------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------
C_WORK = "#bfdbfe"
C_FABRIC = "#bbf7d0"
C_FOUNDRY = "#fde68a"
C_WEB = "#fbcfe8"
C_IQ_BG = "#eef2ff"
C_AGENT = "#ddd6fe"
C_DATA = "#f1f5f9"
C_SEC = "#fee2e2"
C_M365 = "#cffafe"
C_FLOW_USER = "#1e40af"
C_FLOW_DATA = "#15803d"
C_FLOW_AUTH = "#b91c1c"


# =====================================================================
# 1. microsoft-iq-platform — layered architecture, side identity rail
# =====================================================================
def gen_iq_platform():
    e = []
    e.append(title(40, 20, "Microsoft IQ — context platform for agents",
                   size=22))

    # ---- Layer 1: Agents (top) ----
    e.append(text(280, 60, "Agents", size=14, align="left"))
    e += labeled_rect(280, 85, 240, 75,
                      "Foundry Agent\n(Refund processor)",
                      bg=C_AGENT, size=14, stroke_width=3)
    e += labeled_rect(560, 85, 240, 75,
                      "GitHub Copilot CLI\n(developer surface)",
                      bg=C_AGENT, size=14, stroke_width=3)
    e += labeled_rect(840, 85, 240, 75,
                      "Custom agent\n(MCP / A2A / REST)",
                      bg=C_AGENT, size=14, stroke_width=3)

    # ---- Identity rail (left) ----
    e += labeled_rect(40, 85, 200, 600,
                      "Entra ID\n\nIdentity\n+ OBO tokens\n"
                      "+ sensitivity labels\n+ DLP\n+ audit",
                      bg=C_SEC, size=14, stroke_width=3, dashed=True)
    e += arrow(240, 120, 280, 120, stroke=C_FLOW_AUTH, label="auth",
               label_size=11)
    e += arrow(240, 320, 280, 320, stroke=C_FLOW_AUTH, label="permission",
               label_size=11)
    e += arrow(240, 560, 280, 560, stroke=C_FLOW_AUTH, label="audit",
               label_size=11)

    # ---- Layer 2: Unified Microsoft IQ band ----
    band_x, band_y, band_w, band_h = 280, 200, 1080, 230
    e.append(rect(band_x, band_y, band_w, band_h, bg=C_IQ_BG,
                  stroke="#312e81", stroke_width=3, rounded=True))
    e.append(text(band_x + 16, band_y + 10,
                  "Microsoft IQ  —  unified context layer",
                  size=18, align="left"))

    iqs = [
        ("Work IQ", "people\ncollaboration", C_WORK),
        ("Fabric IQ", "business ops\nontologies", C_FABRIC),
        ("Foundry IQ", "knowledge\nagentic RAG", C_FOUNDRY),
        ("Web IQ", "external web\np95 ~164 ms", C_WEB),
    ]
    iq_w, iq_h, gap = 240, 135, 30
    iq_y = band_y + 65
    iq_centers = []
    for i, (name, role, color) in enumerate(iqs):
        x = band_x + 20 + i * (iq_w + gap)
        e += labeled_ellipse(x, iq_y, iq_w, iq_h, f"{name}\n\n{role}",
                             bg=color, size=14, stroke_width=3)
        iq_centers.append((x + iq_w // 2, iq_y, iq_y + iq_h))

    # Agents → IQ band: 3 query arrows
    for ax in [400, 680, 960]:
        e += routed_arrow(
            [(ax, 160), (ax, 200)],
            stroke=C_FLOW_USER,
        )
    e.append(centered_text(540, 178, "context query / tool call",
                           size=12, color=C_FLOW_USER))

    # ---- Layer 3: Data sources ----
    src_y = 520
    sources = [
        ("M365\n(Outlook · Teams\nSharePoint · Loop)", C_M365, "cylinder"),
        ("OneLake\n+ semantic models\n+ ontologies", C_FABRIC, "cylinder"),
        ("Knowledge bases\n(policies, docs)", C_FOUNDRY, "cylinder"),
        ("Public web\n(news · images · video)", C_WEB, "cloud"),
    ]
    src_w, src_h = 240, 140
    for i, (label, color, kind) in enumerate(sources):
        cx, _iqy, iq_bottom = iq_centers[i]
        sx = cx - src_w // 2
        if kind == "cylinder":
            e += cylinder(sx, src_y, src_w, src_h, label, bg=color, size=13)
        else:
            e += cloud(cx, src_y + src_h // 2, src_w + 40, src_h + 30,
                       label, bg=color, size=13)
        # query arrow (IQ → source) on left, data arrow (source → IQ) on right
        e += routed_arrow(
            [(cx - 30, iq_bottom + 4), (cx - 30, src_y - 4)],
            stroke=C_FLOW_USER,
        )
        e += routed_arrow(
            [(cx + 30, src_y - 4), (cx + 30, iq_bottom + 4)],
            stroke=C_FLOW_DATA,
        )

    e.append(centered_text(820, 480, "query    ↕    in-place context",
                           size=13, color="#374151"))

    # ---- Legend ----
    lx, ly = 1100, 705
    e += labeled_rect(lx, ly, 280, 115, "", bg="#fafafa", size=12,
                      stroke="#9ca3af", stroke_width=1, rounded=False)
    e.append(text(lx + 10, ly + 8, "Legend", size=13, align="left"))
    e += arrow(lx + 10, ly + 40, lx + 60, ly + 40, stroke=C_FLOW_USER)
    e.append(text(lx + 70, ly + 32, "query / call", size=12, align="left"))
    e += arrow(lx + 10, ly + 65, lx + 60, ly + 65, stroke=C_FLOW_DATA)
    e.append(text(lx + 70, ly + 57, "data / context", size=12, align="left"))
    e += arrow(lx + 10, ly + 90, lx + 60, ly + 90, stroke=C_FLOW_AUTH)
    e.append(text(lx + 70, ly + 82, "identity / audit", size=12,
                  align="left"))

    save("microsoft-iq-platform.excalidraw", e)


# =====================================================================
# 2. refund-agent-architecture — hub-and-spoke
# =====================================================================
def gen_refund_agent():
    e = []
    e.append(title(40, 20,
                   "Refund Agent — 4 IQs converging on one Foundry agent",
                   size=22))

    # ---- Trigger (top-left) ----
    e += labeled_rect(60, 90, 280, 80,
                      "Amanda's email\n\"Build a refund agent\"",
                      bg=C_M365, size=13, stroke_width=2, dashed=True)
    e += labeled_rect(60, 200, 280, 70,
                      "GitHub Copilot CLI\n+ Work IQ retrieval",
                      bg=C_AGENT, size=13)
    e += arrow(200, 170, 200, 200, stroke=C_FLOW_USER)

    # ---- Central hub: Refund Processor (diamond) ----
    hub_cx, hub_cy = 760, 380
    hub_w, hub_h = 360, 220
    e += labeled_diamond(hub_cx - hub_w // 2, hub_cy - hub_h // 2,
                         hub_w, hub_h,
                         "Refund Processor\n(Foundry Agent)\n\n"
                         "context delegation\nMCP auto-approval\n"
                         "OAuth consent",
                         bg=C_AGENT, size=14, stroke_width=3)

    # CLI → hub
    e += routed_arrow(
        [(340, 235), (500, 235), (500, hub_cy - 80),
         (hub_cx - hub_w // 2 + 30, hub_cy - 80)],
        stroke=C_FLOW_USER, label="build", label_size=12,
    )

    # ---- 4 IQ spokes (ellipses) ----
    iqs = [
        # angle, name, sub, color, src label, src kind
        (210, "Web IQ", "grounding\nweb content", C_WEB,
         "Public web", "cloud"),
        (150, "Foundry IQ", "Refund policy\nKB", C_FOUNDRY,
         "Policy files", "cylinder"),
        (30,  "Fabric IQ", "Data Agent\nOrder + shipment\nontology",
         C_FABRIC, "OneLake\n(orders)", "cylinder"),
        (330, "Work IQ", "MCP — Mail\nCalendar · Teams", C_WORK,
         "M365\n(emails, chats)", "cylinder"),
    ]
    R_IQ = 290
    R_SRC = 500
    iq_w, iq_h = 210, 120
    src_w, src_h = 220, 110
    for ang, name, sub, color, src_label, src_kind in iqs:
        rad = math.radians(ang)
        iqx = hub_cx + int(R_IQ * math.cos(rad)) - iq_w // 2
        iqy = hub_cy + int(R_IQ * math.sin(rad)) - iq_h // 2
        e += labeled_ellipse(iqx, iqy, iq_w, iq_h,
                             f"{name}\n{sub}", bg=color, size=13,
                             stroke_width=3)
        iq_cx = iqx + iq_w // 2
        iq_cy = iqy + iq_h // 2
        dx = hub_cx - iq_cx
        dy = hub_cy - iq_cy
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        start = (int(iq_cx + ux * (iq_w // 2 - 8)),
                 int(iq_cy + uy * (iq_h // 2 - 8)))
        end = (int(hub_cx - ux * (hub_w // 2 - 40)),
               int(hub_cy - uy * (hub_h // 2 - 40)))
        e += arrow(*start, *end, stroke=C_FLOW_DATA)

        # source further out
        srx = hub_cx + int(R_SRC * math.cos(rad)) - src_w // 2
        sry = hub_cy + int(R_SRC * math.sin(rad)) - src_h // 2
        if src_kind == "cylinder":
            e += cylinder(srx, sry, src_w, src_h, src_label,
                          bg=C_DATA, size=12)
        else:
            e += cloud(srx + src_w // 2, sry + src_h // 2,
                       src_w + 30, src_h + 20, src_label,
                       bg=C_DATA, size=12)
        src_cx = srx + src_w // 2
        src_cy = sry + src_h // 2
        sdx = iq_cx - src_cx
        sdy = iq_cy - src_cy
        sd = math.hypot(sdx, sdy)
        sux, suy = sdx / sd, sdy / sd
        sstart = (int(src_cx + sux * (src_w // 2 - 8)),
                  int(src_cy + suy * (src_h // 2 - 8)))
        send = (int(iq_cx - sux * (iq_w // 2 - 8)),
                int(iq_cy - suy * (iq_h // 2 - 8)))
        e += arrow(*sstart, *send, stroke=C_FLOW_DATA, dashed=True)

    # ---- Identity bar (bottom) ----
    e += labeled_rect(60, 760, 1340, 60,
                      "Entra ID — Agentic User Authorization (OBO via MSAL)",
                      bg=C_SEC, size=14, stroke_width=3, dashed=True)
    e += routed_arrow(
        [(hub_cx, 760), (hub_cx, hub_cy + hub_h // 2 + 10)],
        stroke=C_FLOW_AUTH, label="auth", label_size=12,
    )

    # ---- Runtime stack ----
    e += labeled_rect(60, 850, 420, 90,
                      "Microsoft Agents SDK\nCloudAdapter + aiohttp",
                      bg="#ffffff", size=13)
    e += labeled_rect(510, 850, 420, 90,
                      "Agent 365 (Autopilot)\nblueprint · org-chart identity\n"
                      "observability (App Insights)",
                      bg="#ffffff", size=13)
    e += labeled_rect(960, 850, 440, 90,
                      "Surfaces\nTeams · Outlook · Shipment dashboard",
                      bg=C_M365, size=13)

    # ---- Legend ----
    lx, ly = 1180, 90
    e += labeled_rect(lx, ly, 220, 130, "", bg="#fafafa", size=12,
                      stroke="#9ca3af", stroke_width=1, rounded=False)
    e.append(text(lx + 10, ly + 8, "Legend", size=13, align="left"))
    e += arrow(lx + 10, ly + 40, lx + 60, ly + 40, stroke=C_FLOW_USER)
    e.append(text(lx + 70, ly + 32, "build / invoke", size=12, align="left"))
    e += arrow(lx + 10, ly + 70, lx + 60, ly + 70, stroke=C_FLOW_DATA)
    e.append(text(lx + 70, ly + 62, "context / data", size=12, align="left"))
    e += arrow(lx + 10, ly + 100, lx + 60, ly + 100, stroke=C_FLOW_AUTH)
    e.append(text(lx + 70, ly + 92, "identity", size=12, align="left"))

    save("refund-agent-architecture.excalidraw", e)


# =====================================================================
# 3. work-iq-api — protocols → API → capabilities → org intel → M365
# =====================================================================
def gen_work_iq_api():
    e = []
    e.append(title(40, 20,
                   "Work IQ API — in-place access to M365 for agents",
                   size=22))

    # ---- Protocol channels (top) ----
    chans = [
        (140, "A2A\nagent ↔ agent"),
        (540, "MCP\nstd. tool calls"),
        (940, "REST API\ndirect HTTP"),
    ]
    for cx, label in chans:
        e += labeled_rect(cx, 90, 280, 75, label,
                          bg=C_AGENT, size=14, stroke_width=3)
    e.append(text(40, 100, "Your\nagents", size=14, align="left"))

    # ---- API gateway band ----
    e += labeled_rect(140, 210, 1080, 55,
                      "Work IQ API gateway",
                      bg="#e0e7ff", size=15, stroke_width=2)
    for cx, _ in chans:
        e += arrow(cx + 140, 165, cx + 140, 210, stroke=C_FLOW_USER)

    # ---- 4 capability blocks (ellipses) ----
    caps = [
        ("Chat", "agent ↔ user\nconversation"),
        ("Context", "people · files\nthreads retrieval"),
        ("Tools", "calendar · mail\nfile actions"),
        ("Workspaces", "long-running\ncollaboration"),
    ]
    cap_w, cap_h, gap = 240, 140, 20
    cap_x0 = 160
    cap_y = 310
    for i, (name, sub) in enumerate(caps):
        x = cap_x0 + i * (cap_w + gap)
        e += labeled_ellipse(x, cap_y, cap_w, cap_h,
                             f"{name}\n\n{sub}",
                             bg=C_WORK, size=14, stroke_width=3)
        e += arrow(x + cap_w // 2, 265, x + cap_w // 2, cap_y,
                   stroke=C_FLOW_USER)

    # ---- Organizational Intelligence ----
    e += labeled_ellipse(360, 500, 660, 110,
                         "Organizational Intelligence — knowledge graph\n"
                         "(people · docs · threads · meetings)",
                         bg="#fef9c3", size=14, stroke_width=3)
    for i in range(4):
        x = cap_x0 + i * (cap_w + gap) + cap_w // 2
        e += arrow(x, cap_y + cap_h, x, 500, stroke=C_FLOW_DATA)

    # ---- M365 cylinders ----
    src_y = 670
    src_w, src_h = 240, 120
    m365 = [("Outlook", C_M365), ("Teams", C_M365),
            ("SharePoint", C_M365), ("Loop", C_M365)]
    for i, (name, color) in enumerate(m365):
        x = cap_x0 + i * (cap_w + gap)
        e += cylinder(x, src_y, src_w, src_h, name, bg=color, size=14)
        cx = x + src_w // 2
        e += arrow(cx, 610, cx, src_y, stroke=C_FLOW_DATA, dashed=True)

    # ---- In-place callout ----
    e += labeled_rect(1080, 670, 320, 120,
                      "In-place access\n\n"
                      "queries cross the boundary,\n"
                      "data stays in M365.\n"
                      "EntraID + sensitivity labels\nenforced.",
                      bg=C_SEC, size=12, stroke_width=2, dashed=True)
    e += arrow(1060, 730, 1080, 730, stroke=C_FLOW_AUTH, no_end=True)

    # ---- Legend ----
    lx, ly = 1240, 90
    e += labeled_rect(lx, ly, 220, 115, "", bg="#fafafa", size=12,
                      stroke="#9ca3af", stroke_width=1, rounded=False)
    e.append(text(lx + 10, ly + 8, "Legend", size=13, align="left"))
    e += arrow(lx + 10, ly + 40, lx + 60, ly + 40, stroke=C_FLOW_USER)
    e.append(text(lx + 70, ly + 32, "request", size=12, align="left"))
    e += arrow(lx + 10, ly + 65, lx + 60, ly + 65, stroke=C_FLOW_DATA)
    e.append(text(lx + 70, ly + 57, "context", size=12, align="left"))
    e += arrow(lx + 10, ly + 90, lx + 60, ly + 90,
               stroke=C_FLOW_DATA, dashed=True)
    e.append(text(lx + 70, ly + 82, "in-place (no copy)", size=12,
                  align="left"))

    save("work-iq-api.excalidraw", e)


if __name__ == "__main__":
    gen_iq_platform()
    gen_refund_agent()
    gen_work_iq_api()

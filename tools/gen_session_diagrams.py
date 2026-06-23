#!/usr/bin/env python3
"""Generate Excalidraw diagrams for Build 2026 session notes.

각 세션의 Architecture 다이어그램을 .excalidraw JSON 으로 생성한다.
사용자는 VS Code Excalidraw 에디터에서 열어 동일 basename 으로 PNG export 만 하면 된다.

재실행 가능 — 좌표/색상 수정 시 다시 돌리면 .excalidraw 가 갱신된다.
"""
from __future__ import annotations

import json
import os
import random

random.seed(2026)

# ── palette (excalidraw-diagram-generator skill 가이드 기준) ──────────────
BLUE = "#a5d8ff"    # entry / source
GREEN = "#b2f2bb"   # backend / output
YELLOW = "#ffd43b"  # central / core
RED = "#ffc9c9"     # security / governance / cross-cutting
GREY = "#e9ecef"    # neutral

STROKE = "#1e1e1e"
FONT = 5            # Excalifont
FS = 16             # font size


def _nonce() -> int:
    return random.randint(1, 2_000_000_000)


def rect(eid: str, x: float, y: float, w: float, h: float, text: str,
         fill: str = BLUE) -> list[dict]:
    """Return a rectangle element with a bound text label."""
    tid = eid + "_t"
    rectangle = {
        "id": eid, "type": "rectangle", "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": STROKE, "backgroundColor": fill,
        "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": {"type": 3}, "seed": _nonce(), "version": 1,
        "versionNonce": _nonce(), "isDeleted": False,
        "boundElements": [{"type": "text", "id": tid}],
        "updated": 1, "link": None, "locked": False,
    }
    n_lines = text.count("\n") + 1
    line_h = FS * 1.25
    text_h = line_h * n_lines
    label = {
        "id": tid, "type": "text", "x": x + 8, "y": y + (h - text_h) / 2,
        "width": w - 16, "height": text_h, "angle": 0, "strokeColor": STROKE,
        "backgroundColor": "transparent", "fillStyle": "solid",
        "strokeWidth": 1.5, "strokeStyle": "solid", "roughness": 1,
        "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
        "seed": _nonce(), "version": 1, "versionNonce": _nonce(),
        "isDeleted": False, "boundElements": [], "updated": 1, "link": None,
        "locked": False, "text": text, "fontSize": FS, "fontFamily": FONT,
        "textAlign": "center", "verticalAlign": "middle", "baseline": FS,
        "containerId": eid, "originalText": text, "lineHeight": 1.25,
    }
    return [rectangle, label]


def arrow(x1: float, y1: float, x2: float, y2: float,
          color: str = STROKE) -> dict:
    return {
        "id": f"a_{_nonce()}", "type": "arrow", "x": x1, "y": y1,
        "width": abs(x2 - x1), "height": abs(y2 - y1), "angle": 0,
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1.5, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": {"type": 2}, "seed": _nonce(), "version": 1,
        "versionNonce": _nonce(), "isDeleted": False, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "points": [[0, 0], [x2 - x1, y2 - y1]], "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
    }


def title(text: str, x: float, y: float, w: float = 560) -> dict:
    return {
        "id": f"ttl_{_nonce()}", "type": "text", "x": x, "y": y, "width": w,
        "height": 30, "angle": 0, "strokeColor": STROKE,
        "backgroundColor": "transparent", "fillStyle": "solid",
        "strokeWidth": 1.5, "strokeStyle": "solid", "roughness": 1,
        "opacity": 100, "groupIds": [], "frameId": None, "roundness": None,
        "seed": _nonce(), "version": 1, "versionNonce": _nonce(),
        "isDeleted": False, "boundElements": [], "updated": 1, "link": None,
        "locked": False, "text": text, "fontSize": 20, "fontFamily": FONT,
        "textAlign": "left", "verticalAlign": "top", "baseline": 20,
        "containerId": None, "originalText": text, "lineHeight": 1.25,
    }


def cx(b):  # center x of a rect element list
    r = b[0]
    return r["x"] + r["width"] / 2


def bottom(b):
    r = b[0]
    return r["x"] + r["width"] / 2, r["y"] + r["height"]


def top(b):
    r = b[0]
    return r["x"] + r["width"] / 2, r["y"]


def right(b):
    r = b[0]
    return r["x"] + r["width"], r["y"] + r["height"] / 2


def left(b):
    r = b[0]
    return r["x"], r["y"] + r["height"] / 2


def write(path: str, elements: list[dict]) -> None:
    doc = {
        "type": "excalidraw", "version": 2,
        "source": "https://github.com/hellices/microsoft-build-2026",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("wrote", path)


ROOT = os.path.join(os.path.dirname(__file__), "..", "docs", "sessions")
W = 300   # default box width
H = 64    # default box height


# ════════════════════════════════════════════════════════════════════════
# BRK243 — CLAW & Agent Harness (Foundry 3-layer)
# ════════════════════════════════════════════════════════════════════════
def brk243():
    e = []
    e.append(title("BRK243 — Agent Harness on Microsoft Foundry", 220, 0))
    collab = rect("b243_collab", 250, 50, W, H, "Collaboration Layer\nTeams / M365 Copilot", BLUE)
    runtime = rect("b243_runtime", 250, 175, W, H, "Runtime Layer\nHosted Agents", BLUE)
    obs = rect("b243_obs", 640, 175, 260, H, "Trust / Security /\nObservability / Evals", RED)
    harness = rect("b243_harness", 250, 300, W, H, "Agent Harness\ncontext · state · tools · HITL", YELLOW)
    sandbox = rect("b243_sandbox", 640, 300, 260, H, "Sandbox / VM\nHermes claw agents", GREY)
    loop = rect("b243_loop", 250, 425, W, H, "Agent Loop", YELLOW)
    intel = rect("b243_intel", 90, 555, 280, H, "Intelligence Layer\nFoundry + 3rd-party Models", GREEN)
    tools = rect("b243_tools", 420, 555, 280, H, "MCP Tools\n(e.g., SharePoint)", GREEN)
    for b in (collab, runtime, obs, harness, sandbox, loop, intel, tools):
        e += b
    e.append(arrow(*bottom(collab), *top(runtime)))
    e.append(arrow(*bottom(runtime), *top(harness)))
    e.append(arrow(*right(runtime), *left(obs)))
    e.append(arrow(*bottom(harness), *top(loop)))
    e.append(arrow(*right(harness), *left(sandbox)))
    e.append(arrow(*bottom(loop), *top(intel)))
    e.append(arrow(*bottom(loop), *top(tools)))
    write(os.path.join(ROOT, "BRK243-claw-agent-harness-microsoft-foundry",
                       "foundry-harness-architecture.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# BRK246 — Foundry IQ agentic retrieval
# ════════════════════════════════════════════════════════════════════════
def brk246():
    e = []
    e.append(title("BRK246 — Foundry IQ agentic retrieval", 200, 0))
    src = rect("b246_src", 230, 50, 320, 80, "Enterprise Knowledge Sources\nFiles · M365 · Fabric · Web", BLUE)
    iq = rect("b246_iq", 250, 180, 280, H, "Foundry IQ Integration", YELLOW)
    eng = rect("b246_eng", 250, 300, 280, 80, "Retrieval Engine\nagentic retrieval · ranking · query plan", YELLOW)
    search = rect("b246_search", 250, 430, 280, H, "Azure AI Search backend", GREEN)
    resp = rect("b246_resp", 250, 550, 280, H, "Grounded Agent Response", GREEN)
    gov = rect("b246_gov", 620, 300, 260, 80, "Security & Governance\nEntra permissions · Purview labels", RED)
    for b in (src, iq, eng, search, resp, gov):
        e += b
    e.append(arrow(*bottom(src), *top(iq)))
    e.append(arrow(*bottom(iq), *top(eng)))
    e.append(arrow(*bottom(eng), *top(search)))
    e.append(arrow(*bottom(search), *top(resp)))
    e.append(arrow(*right(iq), gov[0]["x"], gov[0]["y"] + 20))
    e.append(arrow(*right(eng), *left(gov)))
    write(os.path.join(ROOT, "BRK246-foundry-iq-enterprise-knowledge-agentic-retrieval",
                       "agentic-retrieval-architecture.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# BRK250 — Eval & control pipeline (ASSERT / ACS)
# ════════════════════════════════════════════════════════════════════════
def brk250():
    e = []
    e.append(title("BRK250 — Agent eval & control pipeline", 200, 0))
    req = rect("b250_req", 80, 60, 300, 80, "RAI Requirements\n& Risk Catalog", BLUE)
    fw = rect("b250_fw", 420, 60, 320, 80, "Microsoft Agent Framework\nor LangGraph + MCP Tools", BLUE)
    agent = rect("b250_agent", 250, 200, 300, H, "Agent under test", YELLOW)
    assert_b = rect("b250_assert", 250, 320, 300, 80, "ASSERT\nYAML falsifiable evals\n(single / multi-turn)", YELLOW)
    acs = rect("b250_acs", 250, 470, 300, 80, "ACS\ndeterministic + AI-assisted\ncontrols across frameworks", YELLOW)
    agt = rect("b250_agt", 70, 620, 280, H, "Agent Governance Toolkit", GREEN)
    foundry = rect("b250_foundry", 450, 620, 280, H, "Microsoft Foundry", GREEN)
    defender = rect("b250_def", 380, 740, 200, H, "Microsoft Defender", RED)
    purview = rect("b250_pur", 600, 740, 200, H, "Microsoft Purview", RED)
    for b in (req, fw, agent, assert_b, acs, agt, foundry, defender, purview):
        e += b
    e.append(arrow(*bottom(req), agent[0]["x"] + 90, agent[0]["y"]))
    e.append(arrow(*bottom(fw), agent[0]["x"] + 210, agent[0]["y"]))
    e.append(arrow(*bottom(agent), *top(assert_b)))
    e.append(arrow(*bottom(assert_b), *top(acs)))
    e.append(arrow(*bottom(acs), *top(agt)))
    e.append(arrow(*bottom(acs), *top(foundry)))
    e.append(arrow(*bottom(foundry), *top(defender)))
    e.append(arrow(*bottom(foundry), *top(purview)))
    write(os.path.join(ROOT, "BRK250-observe-control-agents-open-source-tools",
                       "eval-control-pipeline.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# BRK251 — Agent 365 control plane
# ════════════════════════════════════════════════════════════════════════
def brk251():
    e = []
    e.append(title("BRK251 — Agent 365 control plane", 220, 0))
    agents = rect("b251_agents", 250, 50, 320, 80, "Custom / Third-party Agents\nMicrosoft · LangChain · external", BLUE)
    sdk = rect("b251_sdk", 270, 180, 280, 80, "Agent 365 SDK & CLI\nAgent ID · observability · mapping", YELLOW)
    cp = rect("b251_cp", 270, 310, 280, 80, "Agent 365 Control Plane\nObserve · Govern · Secure", YELLOW)
    entra = rect("b251_entra", 40, 450, 200, 56, "Entra Identity", RED)
    defender = rect("b251_def", 250, 450, 200, 56, "Defender Protection", RED)
    purview = rect("b251_pur", 460, 450, 200, 56, "Purview Governance", RED)
    intune = rect("b251_intune", 670, 450, 220, 56, "Intune Shadow-AI Detect", RED)
    rules = rect("b251_rules", 270, 570, 280, H, "Admin Center\nTemplates & Rules", GREEN)
    surf = rect("b251_surf", 270, 690, 280, H, "Enterprise Surfaces\nTeams · Word", GREEN)
    for b in (agents, sdk, cp, entra, defender, purview, intune, rules, surf):
        e += b
    e.append(arrow(*bottom(agents), *top(sdk)))
    e.append(arrow(*bottom(sdk), *top(cp)))
    e.append(arrow(cp[0]["x"] + 40, cp[0]["y"] + cp[0]["height"], *top(entra)))
    e.append(arrow(cp[0]["x"] + 110, cp[0]["y"] + cp[0]["height"], *top(defender)))
    e.append(arrow(cp[0]["x"] + 170, cp[0]["y"] + cp[0]["height"], *top(purview)))
    e.append(arrow(cp[0]["x"] + 240, cp[0]["y"] + cp[0]["height"], *top(intune)))
    e.append(arrow(*bottom(cp), *top(rules)))
    e.append(arrow(*bottom(rules), *top(surf)))
    write(os.path.join(ROOT, "BRK251-build-secure-enterprise-ready-agents-agent-365",
                       "agent-365-control-plane.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# DEMSP390 — Omniagent 3-layer (app / bridge / agent)
# ════════════════════════════════════════════════════════════════════════
def demsp390():
    e = []
    e.append(title("DEMSP390 — Omniagent app / bridge / agent", 200, 0))
    user = rect("d390_user", 260, 50, 280, H, "User across surfaces", BLUE)
    agent = rect("d390_agent", 260, 175, 280, 80, "Agent (persona)\nmultimodal video / voice / text", YELLOW)
    api = rect("d390_api", 620, 175, 260, H, "Napster Omniagent API", GREEN)
    mem = rect("d390_mem", 620, 300, 260, 80, "Persistent Memory\nhuman emulation", RED)
    bridge = rect("d390_bridge", 260, 300, 280, 80, "Edge MCP (bridge / action)\nin-page MCP server · local cognition", YELLOW)
    app = rect("d390_app", 260, 430, 280, H, "App (truth)\nsite code · DOM · state", GREEN)
    for b in (user, agent, api, mem, bridge, app):
        e += b
    e.append(arrow(*bottom(user), *top(agent)))
    e.append(arrow(*right(agent), *left(api)))
    e.append(arrow(*bottom(api), *top(mem)))
    e.append(arrow(*bottom(agent), *top(bridge)))
    e.append(arrow(*bottom(bridge), *top(app)))
    write(os.path.join(ROOT, "DEMSP390-create-multimodal-ai-agents-persistent-memory",
                       "omniagent-architecture.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# KEY01 — Frontier intelligence ecosystem stack
# ════════════════════════════════════════════════════════════════════════
def key01():
    e = []
    e.append(title("KEY01 — Frontier intelligence ecosystem", 200, 0))
    edge = rect("k01_edge", 250, 60, 320, 80,
                "Edge / Device\nWindows AI · Surface RTX Spark · Project Solara", BLUE)
    cloud = rect("k01_cloud", 250, 185, 320, 80,
                 "Cloud — Azure\nMI300 · Cobalt ARM · NVIDIA Vera Rubin", BLUE)
    agents = rect("k01_agents", 250, 310, 320, 80,
                  "Agents\nMicrosoft Foundry · GitHub Copilot · Rayfin SDK", YELLOW)
    gov = rect("k01_gov", 640, 310, 260, 80, "Governance\nAgent 365", RED)
    models = rect("k01_models", 250, 435, 320, 80,
                  "Models\nMAI family · Frontier Tuning", YELLOW)
    frontier = rect("k01_frontier", 250, 560, 320, 80,
                    "Frontier\nMicrosoft Discovery · Majorana 2", GREEN)
    for b in (edge, cloud, agents, gov, models, frontier):
        e += b
    e.append(arrow(*bottom(edge), *top(cloud)))
    e.append(arrow(*bottom(cloud), *top(agents)))
    e.append(arrow(*right(agents), *left(gov)))
    e.append(arrow(*bottom(agents), *top(models)))
    e.append(arrow(*bottom(models), *top(frontier)))
    write(os.path.join(ROOT, "KEY01-microsoft-build-opening-keynote",
                       "frontier-intelligence-stack.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# DEM330 — Voice Live API multimodal agent
# ════════════════════════════════════════════════════════════════════════
def dem330():
    e = []
    e.append(title("DEM330 — Voice Live API multimodal agent", 200, 0))
    user = rect("d330_user", 260, 60, 280, H, "User", BLUE)
    avatar = rect("d330_avatar", 260, 180, 280, 80,
                  "WebRTC avatar (browser)\nrealtime voice + video", BLUE)
    voice = rect("d330_voice", 260, 300, 280, 80,
                 "Voice Live API\nSTT + reasoning + TTS", YELLOW)
    nhd = rect("d330_nhd", 620, 300, 260, 80,
               "Neural HD V3 · Maya Transcribe 1\nPersonal Voice (MyVoice 2)", GREEN)
    agent = rect("d330_agent", 260, 430, 280, H,
                 "Foundry Prompt Agent", YELLOW)
    mcp = rect("d330_mcp", 260, 555, 280, 80,
               "MCP server (Contoso Travel)\nbook · query tools", GREEN)
    for b in (user, avatar, voice, nhd, agent, mcp):
        e += b
    e.append(arrow(*bottom(user), *top(avatar)))
    e.append(arrow(*bottom(avatar), *top(voice)))
    e.append(arrow(*right(voice), *left(nhd)))
    e.append(arrow(*bottom(voice), *top(agent)))
    e.append(arrow(*bottom(agent), *top(mcp)))
    write(os.path.join(ROOT, "DEM330-build-multimodal-agents-reason-interact-act",
                       "voice-live-agent-architecture.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# BRK252 — Observability to ROI pipeline
# ════════════════════════════════════════════════════════════════════════
def brk252():
    e = []
    e.append(title("BRK252 — From observability to ROI", 200, 0))
    agent = rect("b252_agent", 250, 60, 320, 80,
                 "Agent (any framework)\nLangChain · LangGraph · OpenAI SDK", BLUE)
    trace = rect("b252_trace", 270, 185, 280, H,
                 "Tracing\nOpenTelemetry · Foundry MCP", YELLOW)
    evals = rect("b252_eval", 270, 305, 280, 80,
                 "Evaluation\nrubric evaluator · multi-turn · simulation", YELLOW)
    mon = rect("b252_mon", 620, 305, 260, 80,
               "Monitoring\nAzure Monitor full-stack", RED)
    opt = rect("b252_opt", 270, 435, 280, 80,
               "Optimization\nAZD AI Agent Optimize (+27%)", GREEN)
    roi = rect("b252_roi", 270, 560, 280, 80,
               "Agent ROI\ncost + labor savings → net value", GREEN)
    for b in (agent, trace, evals, mon, opt, roi):
        e += b
    e.append(arrow(*bottom(agent), *top(trace)))
    e.append(arrow(*bottom(trace), *top(evals)))
    e.append(arrow(*right(evals), *left(mon)))
    e.append(arrow(*bottom(evals), *top(opt)))
    e.append(arrow(*bottom(opt), *top(roi)))
    write(os.path.join(ROOT, "BRK252-observability-to-roi-ai-agents",
                       "observability-to-roi-pipeline.excalidraw"), e)


# ════════════════════════════════════════════════════════════════════════
# DEM368-R1 — Fabric data science & ML lifecycle
# ════════════════════════════════════════════════════════════════════════
def dem368():
    e = []
    e.append(title("DEM368-R1 — Fabric data science & ML", 200, 0))
    data = rect("d368_data", 250, 60, 320, 80,
                "OneLake / Lakehouse\nAzure Blob ingest + prep", BLUE)
    build = rect("d368_build", 250, 185, 320, 80,
                 "Notebook + PySpark / SynapseML\nlinear regression · decision tree", YELLOW)
    mlflow = rect("d368_mlflow", 250, 310, 320, H,
                  "MLflow\nlog · compare · version", YELLOW)
    ops = rect("d368_ops", 70, 435, 280, 80,
               "Batch scoring + Power BI\noperationalize", GREEN)
    agent = rect("d368_agent", 470, 435, 280, 80,
                 "Fabric Data Agents\nNL -> SQL", GREEN)
    spread = rect("d368_spread", 470, 560, 280, 80,
                  "Copilot Studio · M365 Copilot · MCP", GREEN)
    for b in (data, build, mlflow, ops, agent, spread):
        e += b
    e.append(arrow(*bottom(data), *top(build)))
    e.append(arrow(*bottom(build), *top(mlflow)))
    e.append(arrow(mlflow[0]["x"] + 80, mlflow[0]["y"] + mlflow[0]["height"], *top(ops)))
    e.append(arrow(mlflow[0]["x"] + 240, mlflow[0]["y"] + mlflow[0]["height"], *top(agent)))
    e.append(arrow(*bottom(agent), *top(spread)))
    write(os.path.join(ROOT, "DEM368-R1-data-science-machine-learning-microsoft-fabric",
                       "fabric-ds-ml-lifecycle.excalidraw"), e)


if __name__ == "__main__":
    brk243()
    brk246()
    brk250()
    brk251()
    demsp390()
    key01()
    dem330()
    brk252()
    dem368()
    print("done")

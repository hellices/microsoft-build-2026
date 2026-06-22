"""Generate Excalidraw JSON diagrams for BRK226 session note.

Run from the repo root:
    python tools/gen_brk226_diagrams.py
"""
import json
import os
import random

OUT_DIR = os.path.join("docs", "sessions", "BRK226-inside-azure-innovations")

random.seed(20260622)


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


def rect(x, y, w, h, bg="transparent", stroke="#1e1e1e", stroke_width=2,
         rounded=True, dashed=False):
    return {
        "id": _id(),
        "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        **_common({
            "backgroundColor": bg,
            "strokeColor": stroke,
            "strokeWidth": stroke_width,
            "strokeStyle": "dashed" if dashed else "solid",
            "fillStyle": "solid",
            "roundness": {"type": 3} if rounded else None,
        }),
    }


def text(x, y, label, size=16, align="left", w=None, color="#1e1e1e"):
    # Rough char width estimate per Excalidraw default font.
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


def label_box(x, y, w, h, label, bg="#f0f4ff", size=16, stroke="#1e1e1e",
              stroke_width=2, dashed=False, rounded=True):
    """Box with a centered text label."""
    r = rect(x, y, w, h, bg=bg, stroke=stroke, stroke_width=stroke_width,
             dashed=dashed, rounded=rounded)
    char_w = size * 0.6
    longest = max((len(line) for line in label.split("\n")), default=1)
    tw = min(w - 8, int(longest * char_w) + 8)
    lines = label.count("\n") + 1
    th = int(size * 1.25 * lines)
    t = text(x + (w - tw) // 2, y + (h - th) // 2, label, size=size,
             align="center", w=tw)
    return [r, t]


def arrow(x1, y1, x2, y2, stroke="#1e1e1e", dashed=False, label=None,
          label_size=14):
    elements = [{
        "id": _id(),
        "type": "arrow",
        "x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1,
        **_common({
            "strokeColor": stroke,
            "strokeStyle": "dashed" if dashed else "solid",
            "points": [[0, 0], [x2 - x1, y2 - y1]],
            "lastCommittedPoint": None,
            "startBinding": None,
            "endBinding": None,
            "startArrowhead": None,
            "endArrowhead": "arrow",
        }),
    }]
    if label:
        mx = (x1 + x2) // 2
        my = (y1 + y2) // 2 - 18
        elements.append(text(mx, my, label, size=label_size, align="center"))
    return elements


def title(x, y, label, size=22):
    return text(x, y, label, size=size, align="left")


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


# ---- Color palette ----
C_HOST = "#fff4d6"        # host/OS layer
C_HYPER = "#ffe0b2"       # hypervisor
C_VM = "#d0e8ff"          # VMs
C_POD = "#d8f0d8"         # containers/pods
C_BOOST = "#ffd6e0"       # Azure Boost / accelerators
C_SEC = "#e8d6ff"         # security / TEE
C_ACCEL = "#ffe9b0"       # GPU/accelerators


# =====================================================================
# 1. azure-boost-offload.excalidraw
# =====================================================================
def gen_azure_boost_offload():
    e = []
    # Left panel — Traditional
    e.append(title(60, 40, "Traditional infrastructure"))
    e += label_box(60, 90, 360, 380, "Physical server", bg="#ffffff", size=14, rounded=False)
    # internals
    e += label_box(90, 130, 300, 60, "VM / Containers (customer workloads)", bg=C_POD)
    e += label_box(90, 210, 300, 60, "Hypervisor", bg=C_HYPER)
    e += label_box(90, 290, 300, 130,
                   "Host OS\n(network + storage I/O + agents)", bg=C_HOST)
    e += arrow(240, 270, 240, 290)

    # Right panel — Offloaded
    e.append(title(520, 40, "Offloaded infrastructure (Azure Boost)"))
    e += label_box(520, 90, 460, 380, "Physical server", bg="#ffffff", size=14, rounded=False)
    e += label_box(550, 130, 240, 200, "VM / Containers\n(customer workloads)", bg=C_POD)
    e += label_box(550, 350, 240, 100, "Hypervisor (slim)", bg=C_HYPER)
    # Boost card
    e += label_box(820, 130, 140, 320, "Azure Boost\n(dedicated card)",
                   bg=C_BOOST, size=14)
    e += label_box(830, 200, 120, 40, "I/O accel.", bg="#ffffff", size=12)
    e += label_box(830, 250, 120, 40, "Mgmt agents", bg="#ffffff", size=12)
    e += label_box(830, 300, 120, 40, "Security\nboundary", bg="#ffffff", size=12)
    e += label_box(830, 360, 120, 70, "Storage /\nNetwork", bg="#ffffff", size=12)
    # I/O moves from host to Boost
    e += arrow(790, 220, 820, 220, label="I/O")
    e += arrow(790, 270, 820, 270)
    e += arrow(790, 380, 820, 380)
    save("azure-boost-offload.excalidraw", e)


# =====================================================================
# 2. direct-virtualization.excalidraw
# =====================================================================
def gen_direct_virtualization():
    e = []
    # Before
    e.append(title(60, 40, "Before — Nested hypervisor"))
    e += label_box(60, 90, 400, 380, "Physical server", bg="#ffffff", size=14, rounded=False)
    e += label_box(90, 130, 340, 50, "Microsoft Hypervisor", bg=C_HYPER)
    e += label_box(90, 200, 340, 250, "Azure VM", bg=C_VM)
    e += label_box(110, 240, 300, 50, "Nested Hypervisor", bg=C_HYPER)
    e += label_box(110, 310, 140, 120, "Container\nPod", bg=C_POD)
    e += label_box(270, 310, 140, 120, "Container\nPod", bg=C_POD)

    # After
    e.append(title(540, 40, "After — Direct virtualization"))
    e += label_box(540, 90, 460, 380, "Physical server", bg="#ffffff", size=14, rounded=False)
    e += label_box(570, 130, 400, 50, "Microsoft Hypervisor", bg=C_HYPER)
    e += label_box(570, 200, 120, 250, "Parent\nPartition\n(VM mgmt)", bg=C_VM, size=14)
    e += label_box(710, 200, 130, 250, "Child VM\n=\nContainer\nPod", bg=C_POD)
    e += label_box(850, 200, 130, 250, "Child VM\n=\nContainer\nPod", bg=C_POD)
    save("direct-virtualization.excalidraw", e)


# =====================================================================
# 3. aci-live-migration.excalidraw
# =====================================================================
def gen_aci_live_migration():
    e = []
    e.append(title(60, 30, "ACI Container Live Migration"))
    # Hypervisor strip across the bottom
    e += label_box(60, 470, 920, 50, "Microsoft Hypervisor", bg=C_HYPER)
    # Left: unhealthy L1 VM
    e += label_box(60, 90, 400, 360, "Unhealthy L1 VM", bg="#ffe2e2", size=16)
    e += label_box(90, 140, 160, 50, "ACI Agent", bg="#ffffff", size=13)
    e += label_box(270, 140, 160, 50, "Live Migration\nAgent", bg="#ffffff", size=13)
    e += label_box(90, 210, 340, 50, "Container Runtime", bg="#ffffff", size=13)
    e += label_box(90, 280, 100, 150, "Pod 1", bg=C_POD)
    e += label_box(210, 280, 100, 150, "Pod 2", bg=C_POD)
    e += label_box(330, 280, 100, 150, "Pod 3", bg=C_POD)
    # Right: healthy L1 VM (destination)
    e += label_box(580, 90, 400, 360, "Healthy L1 VM", bg="#e2f7e2", size=16)
    e += label_box(610, 140, 160, 50, "ACI Agent", bg="#ffffff", size=13)
    e += label_box(790, 140, 160, 50, "Live Migration\nAgent", bg="#ffffff", size=13)
    e += label_box(610, 210, 340, 50, "Container Runtime", bg="#ffffff", size=13)
    # destination shows pods after migration
    e += label_box(610, 280, 100, 150, "Pod 1", bg=C_POD)
    e += label_box(730, 280, 100, 150, "Pod 2", bg=C_POD)
    e += label_box(850, 280, 100, 150, "Pod 3", bg=C_POD)
    # arrows
    e += arrow(460, 360, 580, 360, label="Live migrate pods", label_size=16)
    save("aci-live-migration.excalidraw", e)


# =====================================================================
# 4. manifold-direct-virt.excalidraw
# =====================================================================
def gen_manifold():
    e = []
    e.append(title(60, 30, "Manifold on Direct Virtualization (MaaS)"))
    # Hardware row at bottom
    e += label_box(60, 520, 920, 60,
                   "Hardware:   CPU      |      GPU      |      GPU      |     FPGA / ASIC",
                   bg="#eeeeee", size=14)
    # Hypervisor
    e += label_box(60, 440, 920, 50,
                   "Microsoft Hypervisor   (direct virtualization)", bg=C_HYPER)
    # Host OS + VM mgmt
    e += label_box(60, 380, 920, 40, "Host OS / VM management", bg=C_HOST, size=14)
    # Azure VM frame
    e += label_box(60, 90, 920, 270,
                   "Azure VM with direct virtualization", bg="#ffffff",
                   size=14, rounded=False)
    # Parent partition
    e += label_box(90, 150, 160, 180, "Parent\nPartition", bg=C_VM)
    # CPU container UVM
    e += label_box(280, 150, 200, 180,
                   "CPU Container\nUVM\n(Manifold runtime)", bg=C_POD, size=14)
    # GPU container UVMs
    e += label_box(500, 150, 220, 180,
                   "GPU Container UVM\nModel A", bg=C_ACCEL, size=14)
    e += label_box(740, 150, 220, 180,
                   "GPU Container UVM\nModel B", bg=C_ACCEL, size=14)
    # Manifold label box on top
    e += label_box(280, 100, 680, 40,
                   "Manifold — AI accelerator abstraction (CPU / GPU / FPGA / ASIC)",
                   bg=C_BOOST, size=14)
    # Access arrows from UVMs down to GPU hardware
    e += arrow(600, 360, 600, 520)
    e += arrow(840, 360, 840, 520)
    save("manifold-direct-virt.excalidraw", e)


# =====================================================================
# 5. azure-context-cache.excalidraw
# =====================================================================
def gen_context_cache():
    e = []
    e.append(title(60, 30, "Azure Context Cache"))
    # Pipeline boxes
    e += label_box(60, 120, 160, 100, "Client\napplications", bg=C_VM)
    e += label_box(260, 120, 160, 100, "Enterprise\nSecurity Layer", bg=C_SEC, size=14)
    e += label_box(460, 90, 240, 160,
                   "Azure Context Cache\n(cache mgmt & stats)", bg=C_BOOST, size=14)
    e += label_box(740, 120, 160, 100, "Enterprise\nSecurity Layer", bg=C_SEC, size=14)
    e += label_box(940, 120, 180, 100, "Azure OpenAI\nEndpoint", bg=C_POD, size=14)
    # Arrows
    e += arrow(220, 170, 260, 170, label="EntraID")
    e += arrow(420, 170, 460, 170, label="prompt / context")
    e += arrow(700, 170, 740, 170, label="cached prefix")
    e += arrow(900, 170, 940, 170)
    # Context cache account (storage)
    e += label_box(490, 320, 180, 80, "Context Cache\nAccount", bg="#ffffff", size=13)
    e += arrow(580, 250, 580, 320, dashed=True, label="cached context")
    save("azure-context-cache.excalidraw", e)


# =====================================================================
# 6. overlake-control-plane.excalidraw
# =====================================================================
def gen_overlake():
    e = []
    e.append(title(60, 30, "Overlake — converged compute control plane"))
    # Top: two resource providers
    e += label_box(60, 100, 420, 100,
                   "ACI & AI Sandbox Groups RP\n(serverless containers / sandboxes)",
                   bg=C_POD, size=14)
    e += label_box(520, 100, 420, 100,
                   "VMSS CRP\n(single VMs)", bg=C_VM, size=14)
    # Middle: Overlake
    e += label_box(60, 240, 880, 80,
                   "Overlake — converged Azure compute control plane",
                   bg=C_BOOST, size=16)
    # Arrows
    e += arrow(270, 200, 270, 240)
    e += arrow(730, 200, 730, 240)
    # Bottom: Azure host
    e += label_box(60, 380, 880, 220,
                   "Azure Host  —  On-Demand / Spot / Fungible Fleet",
                   bg="#ffffff", size=14, rounded=False)
    # Inside host: examples
    e += label_box(90, 440, 200, 140,
                   "L1/L2 agent offload\nDirect Virtualization\n(L2 UVM container)",
                   bg=C_HYPER, size=13)
    e += label_box(310, 440, 200, 140,
                   "L1/L2 agent offload\nDirect Virtualization\n(L2 UVM container)",
                   bg=C_HYPER, size=13)
    e += label_box(530, 440, 180, 140, "VM\n(Agents)", bg=C_VM)
    e += label_box(730, 440, 180, 140, "VM\n(Agents)", bg=C_VM)
    # Arrow from Overlake down to host
    e += arrow(500, 320, 500, 380)
    save("overlake-control-plane.excalidraw", e)


# =====================================================================
# 7. confidential-live-migration.excalidraw
# =====================================================================
def gen_conf_live_migration():
    e = []
    e.append(title(60, 30, "Confidential Live Migration (MigTD)"))
    # Left: unpatched node
    e += label_box(60, 100, 420, 480,
                   "Unpatched node", bg="#ffe2e2", size=16)
    e += label_box(90, 150, 360, 50, "Host OS / VM management", bg=C_HOST, size=13)
    e += label_box(90, 220, 360, 60, "MigTD (Send)", bg=C_SEC, size=14)
    e += label_box(90, 300, 360, 50, "Microsoft Hypervisor", bg=C_HYPER, size=13)
    e += label_box(90, 370, 360, 190,
                   "Azure CVM\n(SEV-SNP / TDX)\nkeys + data protected in TEE",
                   bg=C_BOOST, size=14)
    # Right: patched node
    e += label_box(560, 100, 420, 480,
                   "Patched node", bg="#e2f7e2", size=16)
    e += label_box(590, 150, 360, 50, "Host OS / VM management", bg=C_HOST, size=13)
    e += label_box(590, 220, 360, 60, "MigTD (Receive)", bg=C_SEC, size=14)
    e += label_box(590, 300, 360, 50, "Microsoft Hypervisor", bg=C_HYPER, size=13)
    e += label_box(590, 370, 360, 190,
                   "Azure CVM (migrated)\nTEE boundary preserved",
                   bg=C_BOOST, size=14)
    # Migration arrow
    e += arrow(480, 250, 560, 250,
               label="encrypted migration\n(attested)", label_size=14)
    e += arrow(480, 465, 560, 465, dashed=True, label="CVM live migrates")
    save("confidential-live-migration.excalidraw", e)


# =====================================================================
# 8. azure-integrated-hsm.excalidraw
# =====================================================================
def gen_integrated_hsm():
    e = []
    e.append(title(60, 30, "Azure Integrated HSM"))
    # Stack (left)
    e += label_box(60, 100, 460, 50, "Hardware  (AMD D / E v7 series)", bg="#eeeeee", size=14)
    e += label_box(60, 170, 460, 50, "Hypervisor", bg=C_HYPER)
    e += label_box(60, 240, 460, 50, "Host OS", bg=C_HOST)
    e += label_box(60, 310, 460, 280, "Guest OS", bg=C_VM, size=14)
    e += label_box(90, 360, 400, 200, "Virtual Machine\n(Code + Memory)\n\nNCrypt API (Windows)\nOpenSSL engine (Linux)",
                   bg="#ffffff", size=14)
    # HSM (right)
    e += label_box(620, 100, 360, 490,
                   "Azure Integrated HSM", bg=C_SEC, size=18)
    e += label_box(650, 170, 300, 80,
                   "Keys never leave\nHSM boundary", bg="#ffffff", size=14)
    e += label_box(650, 270, 300, 80,
                   "FIPS 140-3 Level 3", bg="#ffffff", size=14)
    e += label_box(650, 370, 300, 80,
                   "Crypto offload\n+ local cache", bg="#ffffff", size=14)
    e += label_box(650, 470, 300, 80,
                   "Per-VM local interface\n(no key in VM memory)",
                   bg="#ffffff", size=13)
    # Arrows from VM to HSM
    e += arrow(490, 460, 620, 320,
               label="standard API calls", label_size=13)
    save("azure-integrated-hsm.excalidraw", e)


# =====================================================================
# 9. project-mosaic.excalidraw
# =====================================================================
def gen_project_mosaic():
    e = []
    e.append(title(60, 30, "Project Mosaic — wide-and-slow optical interconnect"))
    # Left: narrow-and-fast
    e += label_box(60, 100, 420, 460,
                   "Status quo — narrow-and-fast", bg="#ffffff", size=16,
                   rounded=False)
    e += label_box(90, 160, 360, 60,
                   "Few channels @ high speed", bg="#ffe2e2", size=14)
    # Source
    e += label_box(90, 250, 100, 100, "Source", bg=C_HOST)
    # Dest
    e += label_box(350, 250, 100, 100, "Dest", bg=C_HOST)
    # Few thick channels
    for i, y in enumerate([280, 310]):
        e += arrow(190, y, 350, y)
    e += label_box(90, 400, 360, 140,
                   "Copper: high loss → short distance\nOptics (lasers): power-hungry, complex DSP",
                   bg="#ffffff", size=13)

    # Right: Project Mosaic
    e += label_box(540, 100, 460, 460,
                   "Project Mosaic — wide-and-slow", bg="#ffffff", size=16,
                   rounded=False)
    e += label_box(570, 160, 400, 60,
                   "1000s channels @ low speed", bg="#d8f0d8", size=14)
    # microLED array
    e += label_box(570, 250, 120, 120, "microLED\narray", bg=C_BOOST, size=13)
    # imaging fiber middle
    e += label_box(710, 280, 120, 60, "Imaging\nfiber", bg=C_HYPER, size=13)
    # sensor array
    e += label_box(850, 250, 120, 120, "Silicon\nsensor\narray", bg=C_BOOST, size=13)
    # Many thin parallel channels
    import random as _r
    _r.seed(1)
    for k in range(10):
        y = 260 + k * 10
        e += arrow(690, y, 710, y)
        e += arrow(830, y, 850, y)
    e += label_box(570, 400, 400, 140,
                   "microLED + imaging fiber + sensor array\n→ 1000s of cores per fiber\n→ 1 mm form factor",
                   bg="#ffffff", size=13)
    save("project-mosaic.excalidraw", e)


if __name__ == "__main__":
    gen_azure_boost_offload()
    gen_direct_virtualization()
    gen_aci_live_migration()
    gen_manifold()
    gen_context_cache()
    gen_overlake()
    gen_conf_live_migration()
    gen_integrated_hsm()
    gen_project_mosaic()
    print("done")

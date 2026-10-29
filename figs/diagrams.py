"""Architecture / concept diagrams (Figures 1-21, 26-29, 31-34)."""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from figlib import *  # noqa


def fig01():
    fig, ax = canvas(2.75)
    H = 100 * 2.75 / W
    label(ax, 50, H - 3, "Immersive VR/AR ecosystem", fs=7.2, bold=True, c=NAVY)
    # devices
    devs = [("VR headset\n(HMD + controllers)", BLUE), ("AR glasses /\nsmartphone AR", TEAL),
            ("Haptics & body\ntrackers", PURPLE), ("Biosensors\n(eye, EEG, HR)", ORANGE)]
    for i, (t, c) in enumerate(devs):
        box(ax, 2 + i * 24.5, H - 17, 22.5, 10, t, c=c, fs=5.8)
    label(ax, 50, H - 20.5, "Sensing & rendering at the user", fs=5.6, it=True, c=GRAY)
    # edge
    box(ax, 6, H - 37, 40, 12, "Edge node / companion PC\nlocal inference, split rendering", c=GREEN, fs=5.8)
    box(ax, 54, H - 37, 40, 12, "5G / Wi-Fi 6E access\nMEC server, low latency", c=AMBER, fs=5.8)
    # platform
    box(ax, 2, H - 57, 96, 14, "", c=NAVY)
    label(ax, 50, H - 46, "Platform & cloud services", fs=6.3, bold=True, c=NAVY)
    for i, t in enumerate(["Social / multi-\nuser worlds", "Analytics &\npersonalisation",
                           "Avatar & identity\nservices", "App stores &\nthird-party SDKs"]):
        box(ax, 4 + i * 23.5, H - 55.5, 21.5, 7.5, t, c=NAVY, fill="white", fs=5.4)
    # stakeholders
    for i, (t, c) in enumerate([("Users", BLUE), ("Developers", TEAL), ("Advertisers", ORANGE),
                                ("Regulators", RED), ("Researchers", PURPLE)]):
        box(ax, 2 + i * 19.6, 2, 17.6, 6, t, c=c, solid=True, fs=5.8, bold=True)
    label(ax, 50, 11, "Stakeholders who consume or govern the data", fs=5.6, it=True, c=GRAY)
    for x in [13, 37, 63, 87]:
        arrow(ax, (x, H - 17), (26 if x < 50 else 74, H - 25), c=GRAY, lw=0.6)
    arrow(ax, (26, H - 37), (40, H - 43), c=GRAY, lw=0.6)
    arrow(ax, (74, H - 37), (60, H - 43), c=GRAY, lw=0.6)
    arrow(ax, (50, H - 57), (50, 12.5), c=GRAY, lw=0.6, style="<|-|>")
    arrow(ax, (46, H - 31), (54, H - 31), c=GRAY, lw=0.6, style="<|-|>")
    return save(fig, 1, "VR-AR Ecosystem Overview")


def fig02():
    fig, ax = canvas(2.6)
    H = 100 * 2.6 / W
    circle(ax, 50, H / 2, 13, "Immersive\nuser data", c=NAVY, solid=True, fs=6.5)
    items = [("Behavioural\nbiometrics", "motion re-identifies\nusers in seconds", BLUE),
             ("Eye-gaze\ninference", "interest, health,\nemotion leakage", TEAL),
             ("Spatial / room\nmapping", "home layout,\nbystanders", GREEN),
             ("Continuous\ncollection", "90 Hz telemetry,\nno natural pause", AMBER),
             ("Opaque\nconsent", "non-intuitive notices\ninside headsets", ORANGE),
             ("Centralised\naggregation", "breach and\nsecondary use", RED)]
    import math
    for i, (t, s, c) in enumerate(items):
        ang = math.pi / 2 - i * 2 * math.pi / 6
        cx, cy = 50 + 36 * math.cos(ang), H / 2 + 26 * math.sin(ang)
        box(ax, cx - 15, cy - 7.5, 30, 15, "", c=c)
        label(ax, cx, cy + 2.5, t, fs=5.9, bold=True, c=c)
        label(ax, cx, cy - 3.8, s, fs=5.0, c=DARK)
        arrow(ax, (50 + 13 * math.cos(ang), H / 2 + 13 * math.sin(ang)),
              (cx - 15 * math.cos(ang) * 0.9, cy - 7.5 * math.sin(ang) * 0.95), c=c, lw=0.7,
              style="-")
    return save(fig, 2, "Privacy Challenges in Immersive Environments")


def fig03():
    fig, ax = canvas(3.0)
    H = 100 * 3.0 / W
    label(ax, 50, H - 3, "Threat landscape across the VR/AR data path", fs=7, bold=True, c=NAVY)
    stages = ["Sensors", "Device OS\n& apps", "Network", "Platform\nserver", "Third\nparties"]
    for i, s in enumerate(stages):
        box(ax, 6 + i * 18.8, H - 16, 17, 9, s, c=NAVY, solid=True, fs=5.8, bold=True)
        if i < 4:
            arrow(ax, (23 + i * 18.8, H - 11.5), (24.8 + i * 18.8, H - 11.5), c=NAVY)
    threats = [
        ["Side-channel\n(IMU, gaze)", "Malicious SDK\nover-collection", "Eavesdropping\n/ MITM", "Gradient\ninversion", "Data brokerage\n/ resale"],
        ["Spoofed sensor\ninput", "Keystroke &\nPIN inference", "Traffic\nfingerprinting", "Membership &\nattribute inference", "Cross-platform\nlinkage"],
        ["Bystander\ncapture", "Avatar\nimpersonation", "Replay\nattacks", "Model poisoning\n/ backdoors", "Profiling &\nmanipulation"],
    ]
    cols = [ORANGE, AMBER, RED]
    rows = ["Collection", "Inference", "Integrity"]
    for r, row in enumerate(threats):
        y = H - 31 - r * 15
        for i, t in enumerate(row):
            box(ax, 6 + i * 18.8, y, 17, 12, t, c=cols[r], fs=5.0)
    for r, t in enumerate(rows):
        label(ax, 3, H - 25 - r * 15, t, fs=5.6, c=cols[r], bold=True, rot=90)
    box(ax, 6, 2, 92, 9, "Impact: re-identification, sensitive-trait disclosure (health, age, gender),\n"
        "behavioural manipulation, physical safety risk, regulatory penalties", c=GRAY, fs=5.6)
    return save(fig, 3, "Privacy Threat Landscape in VR-AR")


def fig04():
    fig, ax = canvas(3.0)
    H = 100 * 3.0 / W
    box(ax, 20, H - 10, 60, 7, "Privacy-preserving immersive learning", c=NAVY, solid=True, fs=6, bold=True)
    branches = [("Federated\nlearning", BLUE, ["FedAvg /\nFedProx", "SCAFFOLD", "Personalised\nFL", "Decentralised\nFL"]),
                ("Privacy\nmechanisms", TEAL, ["Differential\nprivacy", "Secure\naggregation", "Homomorphic\nencryption", "TEEs"]),
                ("VR/AR privacy", ORANGE, ["Motion\nbiometrics", "Eye-tracking\nprivacy", "Avatar\nanonymity", "Spatial\ndata"]),
                ("Edge &\nsystems", GREEN, ["MEC\noffloading", "Split\nrendering", "Compression", "Scheduling"]),
                ("Governance\n& trust", PURPLE, ["XAI", "Regulation", "Zero trust", "Ethics"])]
    for i, (t, c, leaves) in enumerate(branches):
        x = 1 + i * 19.8
        box(ax, x, H - 26, 18, 10, t, c=c, solid=True, fs=5.8, bold=True)
        arrow(ax, (50, H - 10), (x + 9, H - 16), c=GRAY, style="-", lw=0.6)
        for j, lf in enumerate(leaves):
            y = H - 39 - j * 11
            box(ax, x + 1, y, 16, 8.5, lf, c=c, fs=5.1)
            arrow(ax, (x + 9, H - 26 if j == 0 else y + 19.5), (x + 9, y + 8.5), c=c, style="-", lw=0.5)
    label(ax, 50, 3, "Reviewed works grouped by primary contribution (Table III)", fs=5.6, it=True, c=GRAY)
    return save(fig, 4, "Literature Taxonomy")


def fig05():
    fig, ax = canvas(2.9)
    H = 100 * 2.9 / W
    steps = [("Elicitation", "stakeholder interviews,\nthreat workshops"),
             ("Analysis", "LINDDUN + STRIDE,\nDPIA"), ("Specification", "FR / NFR matrix\n(Table IV)"),
             ("Validation", "experiments,\ncompliance audit")]
    for i, (t, s) in enumerate(steps):
        x = 2 + i * 24.5
        box(ax, x, H - 18, 21.5, 14, "", c=BLUE)
        label(ax, x + 10.75, H - 8, t, fs=6.2, bold=True, c=BLUE)
        label(ax, x + 10.75, H - 14, s, fs=5.1)
        if i < 3:
            arrow(ax, (x + 21.5, H - 11), (x + 24.5, H - 11), c=BLUE)
    arrow(ax, (88, H - 18), (12, H - 18), c=GRAY, rad=-0.25, ls="--", text="feedback loop", fs=5.2, toff=(0, -9))
    cats = [("Privacy", TEAL, "data minimisation,\nunlinkability, DP budget"),
            ("Security", RED, "confidential updates,\nByzantine robustness"),
            ("Trust", PURPLE, "explanations,\naudit trail, consent"),
            ("Latency", AMBER, "< 20 ms motion-to-\nphoton for inference"),
            ("Scalability", GREEN, "10^3 - 10^6 headsets,\npartial participation"),
            ("Interoperability", NAVY, "OpenXR, ONNX,\nstandard APIs"),
            ("User experience", ORANGE, "no frame drops,\nbattery < 5 %/h")]
    for i, (t, c, s) in enumerate(cats):
        col, row = i % 4, i // 4
        x = 2 + col * 24.5; y = H - 45 - row * 19
        box(ax, x, y, 21.5, 16, "", c=c)
        label(ax, x + 10.75, y + 11.5, t, fs=6, bold=True, c=c)
        label(ax, x + 10.75, y + 5, s, fs=5.0)
    box(ax, 75.5, H - 64, 21.5, 16, "Traceability:\neach requirement\nmapped to a layer,\nmetric and test", c=GRAY, fs=5.2)
    return save(fig, 5, "Requirement Engineering Framework")


def fig06():
    fig, ax = canvas(2.7)
    H = 100 * 2.7 / W
    st = [("Generate", BLUE, "pose, gaze,\naudio, scene"), ("Pre-process\non device", TEAL, "windowing,\nfeatures"),
          ("Learn\nlocally", GREEN, "local SGD,\npersonalise"), ("Share\nprotected", PURPLE, "clip, noise,\nmask"),
          ("Aggregate", NAVY, "secure sum,\nrobust agg."), ("Retain /\ndelete", RED, "TTL, erasure,\naudit")]
    import math
    cx, cy, R = 50, H / 2 + 3, 25
    for i, (t, c, s) in enumerate(st):
        a = math.pi / 2 - i * 2 * math.pi / 6
        x, y = cx + 36 * math.cos(a), cy + R * math.sin(a)
        box(ax, x - 13, y - 7.5, 26, 15, "", c=c)
        label(ax, x, y + 2.6, t, fs=5.9, bold=True, c=c)
        label(ax, x, y - 3.8, s, fs=5.0)
        a2 = math.pi / 2 - (i + 0.5) * 2 * math.pi / 6
        a3 = math.pi / 2 - (i + 1) * 2 * math.pi / 6
    for i in range(6):
        a1 = math.pi / 2 - (i + 0.32) * 2 * math.pi / 6
        a2 = math.pi / 2 - (i + 0.68) * 2 * math.pi / 6
        arrow(ax, (cx + 34 * math.cos(a1), cy + 23 * math.sin(a1)),
              (cx + 34 * math.cos(a2), cy + 23 * math.sin(a2)), c=GRAY, rad=-0.15)
    box(ax, 34, cy - 7, 32, 14, "Governance controls\nconsent, purpose,\nDP ledger, logs", c=AMBER, fs=5.5)
    label(ax, 50, 3, "Generate, pre-process and learn run on the headset; only protected updates leave it",
          fs=5.3, it=True, c=GRAY)
    box(ax, 3, cy - 14, 94, 44, c=BLUE, fill="none", ls="--", lw=0.5, z=0) if False else None
    return save(fig, 6, "VR-AR Data Lifecycle Architecture")


def fig07():
    fig, ax = canvas(2.8)
    H = 100 * 2.8 / W
    box(ax, 32, H / 2 - 9, 36, 18, "Federated governance\nboard\npolicy, DP budget,\nincident response", c=NAVY, solid=True, fs=5.8)
    sh = [(2, H - 18, "Users / data\nsubjects", BLUE, "consent, access,\nerasure requests"),
          (68, H - 18, "Platform\noperator", TEAL, "runs aggregator,\npublishes model cards"),
          (2, 4, "Regulators\n(DPB, EDPB)", RED, "audits, fines,\nDPIA review"),
          (68, 4, "Developers /\nenterprises", GREEN, "purpose-bound\nmodel access"),
          (35, H - 18, "Ethics & research\nboard", PURPLE, "fairness, IRB,\nred-teaming"),
          (35, 4, "Device OEMs", AMBER, "TEE, sensor\npermissions")]
    for x, y, t, c, s in sh:
        box(ax, x, y, 30, 14, "", c=c)
        label(ax, x + 15, y + 9.5, t, fs=5.8, bold=True, c=c)
        label(ax, x + 15, y + 3.5, s, fs=5.0)
        arrow(ax, (x + 15, y + (0 if y > H / 2 else 14)), (50, H / 2 + (9 if y > H / 2 else -9)),
              c=c, style="<|-|>", lw=0.6)
    return save(fig, 7, "Multi-Stakeholder Governance Model")


def fig08():
    fig, ax = canvas(2.8)
    H = 100 * 2.8 / W
    steps = [("1  Model the system", "data-flow diagram of\nheadset-edge-server", BLUE),
             ("2  Identify assets", "telemetry, updates,\nglobal model, keys", TEAL),
             ("3  Enumerate threats", "STRIDE (security) +\nLINDDUN (privacy)", ORANGE),
             ("4  Score risk", "likelihood x impact\n(1-5 scale, Table V)", RED),
             ("5  Select controls", "DP, SecAgg, robust\nagg., TEE, consent", GREEN),
             ("6  Validate", "attack experiments\n(Section XIV)", PURPLE)]
    for i, (t, s, c) in enumerate(steps):
        y = H - 13 - i * 12.6
        box(ax, 3, y, 44, 10.5, "", c=c)
        label(ax, 5, y + 7, t, fs=6, bold=True, c=c, ha="left")
        label(ax, 5, y + 2.8, s.replace("\n", " "), fs=5.0, ha="left")
        if i < 5:
            arrow(ax, (25, y), (25, y - 2.1), c=GRAY)
    box(ax, 52, H - 50, 45, 47, "", c=NAVY)
    label(ax, 74.5, H - 7, "Adversary model", fs=6.4, bold=True, c=NAVY)
    adv = ["A1 honest-but-curious server", "A2 malicious clients (<= 30 %)",
           "A3 network eavesdropper", "A4 third-party app / SDK",
           "A5 external model consumer", "A6 insider with DB access"]
    for j, a in enumerate(adv):
        label(ax, 54, H - 14 - j * 5.8, a, fs=5.3, ha="left")
    box(ax, 52, 3, 45, 22, "Assumptions: device OS and TEE\nare trusted; at least 2 honest\nclients per round; "
        "keys distributed\nvia authenticated PKI", c=GRAY, fs=5.2)
    return save(fig, 8, "Threat Modeling Framework")


def fig09():
    fig, ax = canvas(2.9)
    H = 100 * 2.9 / W
    box(ax, 3, 18, 30, 60, "", c=BLUE)
    label(ax, 18, 74, "Headset", fs=6.5, bold=True, c=BLUE)
    for j, t in enumerate(["IMU / 6DoF", "Eye tracker", "Cameras / depth", "Microphones", "Local model"]):
        box(ax, 6, 64 - j * 10.5, 24, 8, t, c=BLUE, fill="white", fs=5.5)
    box(ax, 40, 35, 20, 25, "Wireless\nlink\n(TLS 1.3)", c=AMBER, fs=5.8)
    box(ax, 67, 18, 30, 60, "", c=NAVY)
    label(ax, 82, 74, "Server", fs=6.5, bold=True, c=NAVY)
    for j, t in enumerate(["Aggregator", "Model registry", "Analytics API", "Identity svc", "Logs / DB"]):
        box(ax, 70, 64 - j * 10.5, 24, 8, t, c=NAVY, fill="white", fs=5.5)
    arrow(ax, (33, 47), (40, 47), c=GRAY); arrow(ax, (60, 47), (67, 47), c=GRAY)
    pts = [(4.5, 66, "1"), (4.5, 55, "2"), (31.5, 34, "3"), (50, 62, "4"), (68.5, 66, "5"),
           (95.5, 45, "6"), (95.5, 24, "7")]
    for x, y, n in pts:
        circle(ax, x, y, 2.6, n, c=RED, solid=True, fs=5.6)
    leg = ["1 sensor side-channels", "2 gaze-based inference", "3 malicious app / SDK",
           "4 sniffing, replay", "5 inversion, poisoning", "6 model-query attacks", "7 insider / breach"]
    for j, t in enumerate(leg):
        label(ax, 3 + (j % 4) * 24.5, 12 - (j // 4) * 5.5, t, fs=5.1, ha="left", c=RED)
    label(ax, 50, H - 3, "Attack surface (numbered entry points)", fs=6.8, bold=True, c=NAVY)
    return save(fig, 9, "VR-AR Attack Surface Diagram")


def fig10():
    w, h = 7.16, 3.8
    fig, ax = canvas(h, w)
    H = 100 * h / w
    label(ax, 50, H - 2.2, "PP-FedXR: privacy-preserving federated learning for VR/AR ecosystems",
          fs=8.2, bold=True, c=NAVY)
    # trust & governance bar
    box(ax, 1.5, H - 14.5, 97, 10, "", c=PURPLE)
    label(ax, 3, H - 9.5, "Trust &\ngovernance\nlayer", fs=6.3, bold=True, c=PURPLE, ha="left")
    for j, t in enumerate(["XAI dashboard\n(sensor-group attributions)", "Trust score TS (10)",
                           "Consent & purpose\nregistry", "Model cards +\nDP ledger", "Compliance mapping\n(GDPR, DPDP, HIPAA)"]):
        box(ax, 15 + j * 16.7, H - 13.3, 15.4, 7.6, t, c=PURPLE, fill="white", fs=5.6)
    top = H - 18.5          # top of lower blocks
    bot = 6.0
    hh = top - bot
    inner = [("Sensors: 6DoF pose,\ngaze, hands", BLUE), ("On-device features\n+ local SGD", GREEN),
             ("Clip + DP noise\n+ 8-bit quantise", TEAL), ("Pairwise SecAgg\nmasking", PURPLE)]
    bh, gap = 4.75, 1.0
    def stack(x, wdt, items, c_out):
        ys = []
        for j, (t, c) in enumerate(items):
            y = top - 5.2 - (j + 1) * bh - j * gap
            box(ax, x + 1, y, wdt - 2, bh, t, c=c if c_out is None else c_out, fill="white", fs=5.5)
            ys.append(y)
        for j in range(len(ys) - 1):
            arrow(ax, (x + wdt / 2, ys[j]), (x + wdt / 2, ys[j + 1] + bh), c=GRAY, lw=0.5, ms=4)
    for i, nm in enumerate(["Headset 1", "Headset 2", "Headset K"]):
        x = 1.5 + i * 15.2
        box(ax, x, bot, 14, hh, "", c=BLUE)
        label(ax, x + 7, top - 2.6, nm, fs=6.5, bold=True, c=BLUE)
        stack(x, 14, inner, None)
    label(ax, 23.7, bot - 3.0, "Raw telemetry never leaves the device", fs=6, it=True, c=BLUE)
    ex = 47.5
    box(ax, ex, bot, 17, hh, "", c=GREEN)
    label(ax, ex + 8.5, top - 2.6, "Edge intelligence", fs=6.5, bold=True, c=GREEN)
    stack(ex, 17, [("Real-time inference\n(p95 = 0.033 ms)", GREEN), ("Personalised\nfine-tuning", GREEN),
                   ("Cohort selection\n& scheduling", GREEN), ("Update relay\n(cannot unmask)", GREEN)], GREEN)
    sx = 71
    box(ax, sx, bot, 27.5, hh, "", c=NAVY)
    label(ax, sx + 13.75, top - 2.6, "Federated aggregation server", fs=6.5, bold=True, c=NAVY)
    stack(sx, 27.5, [("Secure sum: masks cancel", NAVY), ("Norm-bounded robust aggregation", NAVY),
                   ("Server-momentum update (4)", NAVY), ("RDP privacy accountant (6)-(7)", NAVY)], NAVY)
    yb = top - 5.2 - 4 * bh - 3 * gap + bh / 2
    arrow(ax, (46.6, yb), (ex, yb), c=PURPLE, lw=0.8)
    arrow(ax, (ex + 17, yb), (sx, yb), c=PURPLE, lw=0.8)
    label(ax, (ex + 17 + sx) / 2, yb + 3.2, "masked\nupdates", fs=5.4, c=PURPLE)
    yt = top - 5.2 - bh + bh / 2
    arrow(ax, (sx, yt), (ex + 17, yt), c=NAVY, lw=0.8)
    label(ax, (ex + 17 + sx) / 2, yt - 3.4, "global\nmodel w_t", fs=5.4, c=NAVY)
    for x in [8.5, 23.7, 38.9, ex + 8.5, sx + 13.75]:
        arrow(ax, (x, top), (x, H - 14.5), c=PURPLE, style="<|-|>", lw=0.6, ms=4)
    return save(fig, 10, "Overall Federated VR-AR Learning Architecture")


def fig11():
    w, h = 7.16, 3.3
    fig, ax = canvas(h, w)
    H = 100 * h / w
    layers = [("L6 Application", ORANGE, ["Virtual classroom", "Rehab therapy", "Industrial training", "Social gaming", "Smart-city AR"]),
              ("L5 Trust", PURPLE, ["Explanations", "Trust score", "Audit logs", "Model cards"]),
              ("L4 Edge", GREEN, ["Local inference", "Personalisation", "Caching", "Offloading policy"]),
              ("L3 Privacy & security", TEAL, ["Clipping", "Gaussian DP", "Secure aggregation", "Robust aggregation", "TLS / TEE"]),
              ("L2 Federated learning", BLUE, ["Client selection", "Local SGD", "Aggregation", "Momentum", "Quantisation"]),
              ("L1 Device & data", NAVY, ["6DoF pose", "Eye gaze", "Hand tracking", "Feature windows"])]
    lh, step = 5.4, 6.3
    for i, (t, c, items) in enumerate(layers):
        y = H - 2 - lh - i * step
        box(ax, 1, y, 98, lh, c=c, r=1)
        box(ax, 1, y, 17, lh, t, c=c, solid=True, fs=6.4, bold=True, r=1)
        n = len(items); wd = (79 - (n - 1) * 1.2) / n
        for j, it in enumerate(items):
            box(ax, 19.5 + j * (wd + 1.2), y + 0.8, wd, lh - 1.6, it, c=c, fill="white", fs=6.0)
    box(ax, 1, 1.2, 98, 4.6, "Cross-cutting: governance board, consent registry, privacy ledger and compliance controls (Sections V, XVI, XVII)",
        c=GRAY, fs=6.0)
    return save(fig, 11, "Layered System Architecture")


def fig12():
    fig, ax = canvas(3.1)
    H = 100 * 3.1 / W
    steps = [("Server", r"broadcast global model $w_t$" + "\n" + r"to sampled cohort $S_t$ (q = 0.1)", NAVY),
             ("Client", "local SGD on own windows\n(E = 2 epochs, B = 32)", BLUE),
             ("Client", r"compute update $\Delta_k$," + "\nclip to C = 0.5", TEAL),
             ("Client", r"add $\mathcal{N}(0, z^2C^2/m)$ share," + "\nquantise, mask", PURPLE),
             ("Server", "unmask aggregate sum,\naverage over m", NAVY),
             ("Server", r"momentum step ($\beta$ = 0.9)," + "\nupdate privacy ledger", NAVY),
             ("Edge", r"deploy $w_{t+1}$; optional" + "\npersonal fine-tune", GREEN)]
    for i, (who, t, c) in enumerate(steps):
        y = H - 12 - i * 11.2
        box(ax, 4, y, 16, 8.5, who, c=c, solid=True, fs=6, bold=True)
        box(ax, 23, y, 56, 8.5, t, c=c, fs=5.6)
        label(ax, 84.5, y + 4.25, f"step {i + 1}", fs=5.4, c=GRAY)
        if i < 6:
            arrow(ax, (53, y), (53, y - 2.7), c=GRAY)
    arrow(ax, (92, H - 12 - 5 * 11.2 + 4), (92, H - 12 + 4), c=ORANGE, lw=0.9)
    label(ax, 96, H / 2 + 2, "repeat for T = 200 rounds", fs=5.4, c=ORANGE, rot=90)
    return save(fig, 12, "Federated Learning Workflow")


def fig13():
    fig, ax = canvas(2.2)
    H = 100 * 2.2 / W
    for i in range(5):
        y = H - 11 - i * 9.6
        c = RED if i == 3 else BLUE
        box(ax, 2, y, 17, 7.5, rf"$\Delta_{i + 1}$" if i < 4 else r"$\Delta_m$", c=c, fs=6)
        box(ax, 23, y, 15, 7.5, r"clip $\|\cdot\| \leq C$", c=TEAL, fs=5.4)
        box(ax, 42, y, 14, 7.5, "+ noise share", c=PURPLE, fs=5.4)
        arrow(ax, (19, y + 3.75), (23, y + 3.75), c=GRAY); arrow(ax, (38, y + 3.75), (42, y + 3.75), c=GRAY)
        arrow(ax, (56, y + 3.75), (62, H / 2 + 3), c=GRAY, lw=0.5)
    label(ax, 10.5, H - 11 - 3 * 9.6 - 1.5, "poisoned (x -5)", fs=5, c=RED)
    box(ax, 62, H / 2 - 7, 16, 20, "Secure\nsum\n(masks\ncancel)", c=NAVY, fs=5.8)
    box(ax, 82, H / 2 - 7, 16, 20, r"$\frac{1}{m}\sum$" + "\n+ momentum\n" + r"$\rightarrow w_{t+1}$", c=NAVY, solid=True, fs=5.6)
    arrow(ax, (78, H / 2 + 3), (82, H / 2 + 3), c=NAVY)
    label(ax, 50, 4, "Clipping bounds every client's influence: a poisoned update\ncan move the average by at most C/m",
          fs=5.5, it=True, c=GRAY)
    return save(fig, 13, "Model Aggregation Process")


def fig14():
    fig, ax = canvas(3.2)
    H = 100 * 3.2 / W
    rings = [(46, GRAY, "Governance", "consent, purpose limitation, retention, audit"),
             (38, RED, "Network", "TLS 1.3, certificate pinning, replay nonces"),
             (30, PURPLE, "Aggregation", "pairwise-mask secure aggregation"),
             (22, TEAL, "Output", "client-level differential privacy (z, C)"),
             (14, BLUE, "Device", "TEE, sensor permissions, raw data kept local")]
    cx, cy, s = 50, H - 36, 0.70
    for r, c, t, d in rings:
        ax.add_patch(Circle((cx, cy), r * s, fc=L[c], ec=c, lw=0.7, zorder=1))
    circle(ax, cx, cy, 5.6, "Raw\ntelemetry", c=NAVY, solid=True, fs=4.9)
    for r, c, t, d in rings:
        label(ax, cx, cy + r * s - 3.2, t, fs=5.9, bold=True, c=c)
    for k, (r, c, t, d) in enumerate(rings[::-1]):
        y = 19.5 - k * 4.3
        box(ax, 6, y - 1.5, 3, 3, c=c, solid=True, r=0.4)
        label(ax, 11, y, f"{t}: {d}", fs=5.4, ha="left")
    return save(fig, 14, "Privacy Preservation Architecture")


def fig15():
    fig, ax = canvas(3.1)
    H = 100 * 3.1 / W
    cols = [("Client i", BLUE, 14), ("Client j", BLUE, 38), ("Server", NAVY, 62), ("Privacy ledger", PURPLE, 87)]
    for t, c, x in cols:
        box(ax, x - 10, H - 9, 20, 6, t, c=c, solid=True, fs=6, bold=True)
        ax.plot([x, x], [3, H - 9], color=c, lw=0.6, ls=(0, (3, 2)), zorder=0)
    msgs = [(14, 62, "1 client i advertises DH public key", BLUE), (38, 62, "1' client j advertises DH public key", BLUE),
            (62, 14, "2 broadcast key list + w_t", NAVY),
            (14, 14, "3 s_ij = KDF(DH(i, j))", BLUE), (14, 62, "4 y_i = x_i + PRG(s_ij) (mod 2^32)", PURPLE),
            (38, 62, "4' y_j = x_j - PRG(s_ij)", PURPLE), (62, 62, "5 sum y = x_i + x_j  (masks cancel)", NAVY),
            (62, 87, "6 log (z, q, T) -> epsilon", PURPLE), (62, 38, "7 new global model", NAVY)]
    y = H - 15
    for a, b, t, c in msgs:
        if a == b:
            box(ax, a - 12 if a < 50 else a - 20, y - 3, 24 if a < 50 else 38, 5.5, t, c=c, fs=5.2)
        else:
            arrow(ax, (a, y), (b, y), c=c, lw=0.7)
            if t:
                label(ax, (a + b) / 2, y + 2.2, t, fs=5.2, c=c)
        y -= 9.2
    return save(fig, 15, "Secure Data Exchange Framework")


def fig16():
    fig, ax = canvas(2.4)
    H = 100 * 2.4 / W
    st = [("Sense", "90 Hz pose,\ngaze, hands", BLUE), ("Window", "2 s buffer\n(180 frames)", TEAL),
          ("Featurise", "48 stats\n(8 groups)", GREEN), ("Infer", "global +\npersonal head", PURPLE),
          ("Act", "adapt scene,\nhaptics, UI", ORANGE)]
    for i, (t, s, c) in enumerate(st):
        x = 2 + i * 19.7
        box(ax, x, H - 24, 17.5, 18, "", c=c)
        label(ax, x + 8.75, H - 11, t, fs=6.2, bold=True, c=c)
        label(ax, x + 8.75, H - 18.5, s, fs=5.2)
        if i < 4:
            arrow(ax, (x + 17.5, H - 15), (x + 19.7, H - 15), c=GRAY)
    box(ax, 2, 18, 47, 16, "Privacy-aware personalisation:\n1 local epoch on own data;\nweights never uploaded", c=GREEN, fs=5.5)
    box(ax, 51, 18, 47, 16, "Periodic contribution:\nclipped, noised, masked update\nwhen idle + charging + Wi-Fi", c=PURPLE, fs=5.5)
    arrow(ax, (70, H - 24), (74, 34), c=GRAY, lw=0.6); arrow(ax, (25, 34), (66, H - 24), c=GRAY, lw=0.6, rad=0.0)
    box(ax, 2, 3, 96, 11, "Latency budget: motion-to-photon < 20 ms;\nmeasured edge pipeline p95 = 0.033 ms (Fig. 24)",
        c=AMBER, fs=5.6)
    return save(fig, 16, "Edge Intelligence Workflow")


def fig17():
    fig, ax = canvas(2.7)
    H = 100 * 2.7 / W
    tiers = [("Device tier", BLUE, "inference, raw data,\nlocal training", 2),
             ("Edge / MEC tier", GREEN, "cohort scheduling,\npersonalisation cache,\nupdate relay", 35),
             ("Cloud tier", NAVY, "secure aggregation,\nprivacy accountant,\nmodel registry", 68)]
    for t, c, s, x in tiers:
        box(ax, x, H - 40, 30, 34, "", c=c)
        label(ax, x + 15, H - 11, t, fs=6.4, bold=True, c=c)
        label(ax, x + 15, H - 24, s, fs=5.4)
    arrow(ax, (32, H - 30), (35, H - 30), c=GRAY, style="<|-|>")
    arrow(ax, (65, H - 30), (68, H - 30), c=GRAY, style="<|-|>")
    label(ax, 50, H - 46, "Placement policy (who computes what)", fs=6.2, bold=True, c=NAVY)
    rows = [("Latency-critical inference", "device", BLUE), ("Model personalisation", "device / edge", GREEN),
            ("Round orchestration", "edge", GREEN), ("Global aggregation", "cloud", NAVY),
            ("Raw telemetry storage", "never centralised", RED)]
    for j, (a, b, c) in enumerate(rows):
        y = H - 53 - j * 5.6
        label(ax, 8, y, a, fs=5.5, ha="left"); label(ax, 92, y, b, fs=5.5, ha="right", c=c, bold=True)
        ax.plot([8, 92], [y - 2.5, y - 2.5], color="#DDDDDD", lw=0.4)
    return save(fig, 17, "Edge-to-Cloud Coordination Framework")


def fig18(task=None, groups=None):
    fig, ax = canvas(2.9)
    H = 100 * 2.9 / W
    box(ax, 2, H - 16, 28, 12, "Global model\n(MLP 48-64-8)", c=NAVY, fs=5.8)
    box(ax, 36, H - 16, 28, 12, "Explainer\npermutation importance\nper sensor group", c=PURPLE, fs=5.4)
    box(ax, 70, H - 16, 28, 12, "Transparency\ndashboard in\nheadset settings", c=ORANGE, fs=5.6)
    arrow(ax, (30, H - 10), (36, H - 10), c=GRAY); arrow(ax, (64, H - 10), (70, H - 10), c=GRAY)
    if task is not None:
        label(ax, 50, H - 22, "Measured attributions: accuracy drop when a group is shuffled", fs=5.8, bold=True, c=NAVY)
        mx = max(task) or 1
        for j, (g, v) in enumerate(zip(groups, task)):
            y = H - 29 - j * 5.3
            label(ax, 31, y, g, fs=5.3, ha="right")
            box(ax, 33, y - 1.8, 55 * v / mx, 3.6, c=PURPLE, solid=True, r=0.4)
            label(ax, 34 + 55 * v / mx, y, f"{100 * v:.1f} pp", fs=5.0, ha="left", c=PURPLE)
    return save(fig, 18, "Explainable VR-AR AI Framework")


def fig19():
    fig, ax = canvas(2.6)
    H = 100 * 2.6 / W
    comps = [("Privacy P", "1 - 2|AUC_MI - 0.5|,\nx (1 - exposure)", TEAL, 0.35),
             ("Utility U", "accuracy /\ncentralised acc.", BLUE, 0.20),
             ("Robustness R", "acc. at 20 % attackers\n/ clean acc.", RED, 0.25),
             ("Transparency T", "controls implemented\n(of 6)", PURPLE, 0.20)]
    for i, (t, s, c, wgt) in enumerate(comps):
        x = 2 + i * 24.5
        box(ax, x, H - 24, 22, 20, "", c=c)
        label(ax, x + 11, H - 9, t, fs=6, bold=True, c=c)
        label(ax, x + 11, H - 17, s, fs=5.0)
        arrow(ax, (x + 11, H - 24), (50, H - 40), c=c, lw=0.6, text=f"w = {wgt}", fs=5.2, toff=(0, -1))
    box(ax, 28, H - 52, 44, 12, r"Trust score  $TS=\sum_i w_i S_i$   (10)", c=NAVY, solid=True, fs=6.2, bold=True)
    for j, (lo, hi, t, c) in enumerate([(0.0, 0.6, "low: block deployment", RED),
                                        (0.6, 0.8, "medium: deploy with review", AMBER),
                                        (0.8, 1.0, "high: deploy, monitor", GREEN)]):
        box(ax, 4 + j * 31.5, 4, 29, 9, f"{lo:.1f}-{hi:.1f}\n{t.split(': ')[0]}: {t.split(': ')[1]}".replace(": ", ":\n", 1), c=c, fs=5.3)
    arrow(ax, (50, H - 52), (50, 13), c=GRAY)
    return save(fig, 19, "Trust Assessment Model")


def fig20():
    fig, ax = canvas(2.9)
    H = 100 * 2.9 / W
    box(ax, 2, H - 20, 30, 16, "VR-MotionPriv-Synth\n1,000 users, 65,920\nwindows, 48 features,\n8 activities", c=BLUE, fs=5.4)
    box(ax, 36, H - 20, 28, 16, "Per-user split\n80 % train / 20 % test\nDirichlet alpha = 0.4\nlabel skew", c=TEAL, fs=5.4)
    box(ax, 68, H - 20, 30, 16, "Simulated fleet\nK = 1,000 headsets\nm = 100 per round\nT = 200 rounds", c=GREEN, fs=5.4)
    arrow(ax, (32, H - 12), (36, H - 12), c=GRAY); arrow(ax, (64, H - 12), (68, H - 12), c=GRAY)
    label(ax, 50, H - 26, "Training configurations compared", fs=6.2, bold=True, c=NAVY)
    cfgs = ["Centralised", "Local-only", "FedAvg", "FedProx", "DP-FedAvg", "PP-FedXR"]
    for i, t in enumerate(cfgs):
        box(ax, 2 + i * 16.3, H - 38, 15, 8, t, c=NAVY if i < 5 else ORANGE, solid=i == 5, fs=5.4)
    label(ax, 50, H - 44, "Attack and systems harness", fs=6.2, bold=True, c=NAVY)
    atk = ["Re-identification\n(raw data, LDP)", "Membership\ninference (loss)", "Model poisoning\n(10-30 %)",
           "SecAgg cost\n& correctness", "Latency\n(edge vs cloud)", "Scalability\n(m = 25-400)"]
    for i, t in enumerate(atk):
        box(ax, 2 + i * 16.3, H - 58, 15, 11, t, c=RED if i < 3 else PURPLE, fs=4.9)
    box(ax, 2, 3, 96, 9, "Python 3.13 + NumPy 2.3, single CPU thread, fixed seeds;\ncode and data released (see Data availability)",
        c=GRAY, fs=5.4)
    return save(fig, 20, "Experimental Architecture")


def fig21():
    fig, ax = canvas(1.9)
    H = 100 * 1.9 / W
    dims = [("Privacy", TEAL, ["epsilon (delta = 1e-4)", "MI attack AUC", "re-ID accuracy"]),
            ("Utility", BLUE, ["test accuracy", "per-user accuracy", "personalisation gain"]),
            ("Systems", GREEN, ["latency p50 / p95", "bytes per update", "SecAgg time"]),
            ("Trust", PURPLE, ["robust accuracy", "transparency", "trust score"])]
    for i, (t, c, ms) in enumerate(dims):
        x = 2 + i * 24.5
        box(ax, x, H - 10, 22, 7, t, c=c, solid=True, fs=6.2, bold=True)
        for j, mtxt in enumerate(ms):
            box(ax, x + 1, H - 19.5 - j * 8.3, 20, 6.5, mtxt, c=c, fs=5.3)
    box(ax, 2, 2, 96, 10, "Each metric is computed by the released harness (results.json) and mapped\n"
        "to a requirement in Table IV and a regulatory control in Table XI", c=GRAY, fs=5.6)
    return save(fig, 21, "Evaluation Framework")


def fig26():
    fig, ax = canvas(2.9)
    H = 100 * 2.9 / W
    regs = [("GDPR", "EU"), ("DPDP Act\n2023", "India"), ("HIPAA", "US health"), ("NIST PF\n1.0", "US"),
            ("ISO/IEC\n27701", "intl.")]
    ctrls = ["Data minimisation\n(on-device raw data)", "Client-level DP\n+ privacy ledger",
             "Secure aggregation\n+ TLS", "Consent & purpose\nregistry", "Erasure & retention\nautomation",
             "XAI + model cards"]
    for i, (r, s) in enumerate(regs):
        box(ax, 2, H - 13 - i * 13, 24, 10.5, f"{r}", c=RED, fs=5.8, bold=True)
        label(ax, 14, H - 13 - i * 13 + 1.6, s, fs=4.6, c=GRAY, it=True)
    for j, t in enumerate(ctrls):
        box(ax, 72, H - 13 - j * 10.8, 26, 9, t, c=TEAL, fs=5.2)
    links = [(0, 0), (0, 1), (0, 3), (0, 4), (0, 5), (1, 0), (1, 3), (1, 4), (2, 2), (2, 1), (2, 4),
             (3, 0), (3, 5), (3, 2), (4, 3), (4, 2), (4, 4)]
    for a, b in links:
        arrow(ax, (26, H - 13 - a * 13 + 5.2), (72, H - 13 - b * 10.8 + 4.5), c=GRAY, style="-", lw=0.4)
    label(ax, 49, H - 3, "requirement -> technical control", fs=5.6, it=True, c=GRAY)
    return save(fig, 26, "Compliance Mapping Architecture")


def fig27():
    fig, ax = canvas(2.6)
    H = 100 * 2.6 / W
    import math
    pr = [("Autonomy", BLUE), ("Transparency", PURPLE), ("Behavioural\nprivacy", TEAL),
          ("Fairness", GREEN), ("Safety", RED), ("Accountability", NAVY)]
    circle(ax, 50, H / 2, 12, "Responsible\nimmersive AI", c=ORANGE, solid=True, fs=6)
    for i, (t, c) in enumerate(pr):
        a = math.pi / 2 - i * 2 * math.pi / 6
        x, y = 50 + 35 * math.cos(a), H / 2 + 24 * math.sin(a)
        box(ax, x - 12, y - 5.5, 24, 11, t, c=c, fs=5.8, bold=True)
        arrow(ax, (50 + 12 * math.cos(a), H / 2 + 12 * math.sin(a)), (x - 9 * math.cos(a), y - 5 * math.sin(a)),
              c=c, style="-", lw=0.6)
    return save(fig, 27, "Ethical VR-AR Framework")


def fig28():
    fig, ax = canvas(2.8)
    H = 100 * 2.8 / W
    for i, t in enumerate(["Hospital A\nstroke rehab", "Hospital B\nphysio", "Home patients\n(standalone HMD)"]):
        x = 2 + i * 22
        box(ax, x, H - 22, 20, 16, t, c=BLUE, fs=5.4)
        box(ax, x + 2, H - 40, 16, 10, "local model\n+ EHR stays", c=GREEN, fs=5.0)
        arrow(ax, (x + 10, H - 22), (x + 10, H - 30), c=GRAY)
        arrow(ax, (x + 10, H - 40), (80, H - 52), c=PURPLE, lw=0.5)
    box(ax, 70, H - 24, 28, 18, "Therapist\ndashboard\nprogress + XAI", c=ORANGE, fs=5.4)
    box(ax, 66, H - 62, 32, 14, "HIPAA / DPDP-aligned\nsecure aggregator\n(BAA in place)", c=NAVY, fs=5.4)
    arrow(ax, (82, H - 48), (84, H - 24), c=NAVY)
    box(ax, 2, 4, 60, 14, "Outcomes: range-of-motion estimation and\nadherence prediction learnt across sites\nwithout pooling patient kinematics", c=GRAY, fs=5.3)
    return save(fig, 28, "Healthcare VR-AR Learning Ecosystem")


def fig29():
    fig, ax = canvas(2.7)
    H = 100 * 2.7 / W
    for i, t in enumerate(["Plant 1\nassembly", "Plant 2\nwelding", "Plant 3\nsafety drills"]):
        y = H - 16 - i * 16
        box(ax, 2, y, 22, 12, t, c=BLUE, fs=5.6)
        box(ax, 28, y, 22, 12, "On-prem edge\nserver (OT net)", c=GREEN, fs=5.4)
        arrow(ax, (24, y + 6), (28, y + 6), c=GRAY)
        arrow(ax, (50, y + 6), (60, H - 32), c=PURPLE, lw=0.6)
    box(ax, 60, H - 42, 38, 20, "Corporate aggregator\nskill-assessment model\nworker IDs pseudonymised", c=NAVY, fs=5.4)
    box(ax, 60, H - 62, 38, 14, "Works council review\n+ trust dashboard", c=PURPLE, fs=5.4)
    arrow(ax, (79, H - 42), (79, H - 48), c=GRAY)
    box(ax, 2, 3, 96, 8, "Worker telemetry is used for training quality only, never for individual performance scoring",
        c=AMBER, fs=5.4)
    return save(fig, 29, "Industrial Training Deployment Architecture")


def fig31():
    fig, ax = canvas(2.6)
    H = 100 * 2.6 / W
    items = [("Bandwidth", "uplink-constrained HMDs", "8-bit / sparse updates", BLUE),
             ("Device heterogeneity", "Quest vs AR glasses", "tiered models, FedProx", TEAL),
             ("Latency", "rendering contention", "idle-time training", GREEN),
             ("Energy", "battery & thermal", "charge-only scheduling", AMBER),
             ("Interoperability", "vendor silos", "OpenXR + ONNX", PURPLE),
             ("Governance complexity", "multi-jurisdiction", "policy-as-code", RED)]
    label(ax, 23, H - 4, "Challenge", fs=6.2, bold=True, c=NAVY)
    label(ax, 54, H - 4, "Root cause", fs=6.2, bold=True, c=NAVY)
    label(ax, 83, H - 4, "Mitigation path", fs=6.2, bold=True, c=NAVY)
    for j, (a, b, c_, col) in enumerate(items):
        y = H - 13 - j * 10.3
        box(ax, 3, y, 38, 8, a, c=col, solid=True, fs=5.6, bold=True)
        box(ax, 43, y, 22, 8, b, c=col, fs=5.2)
        box(ax, 70, y, 27, 8, c_, c=GREEN, fs=5.2)
        arrow(ax, (65, y + 4), (70, y + 4), c=GRAY)
    return save(fig, 31, "Challenges and Limitations Roadmap")


def fig32():
    fig, ax = canvas(2.6)
    H = 100 * 2.6 / W
    ax.plot([5, 95], [H / 2, H / 2], color=NAVY, lw=1.4)
    phases = [("2026-27", "Short term", ["distributed DP + SecAgg\nin production SDKs", "OpenXR privacy\nextensions"], BLUE),
              ("2028-29", "Medium term", ["federated foundation\nmodels for XR", "cognitive identity\nprotection"], TEAL),
              ("2030+", "Long term", ["quantum-safe\naggregation", "autonomous, auditable\ngovernance agents"], PURPLE)]
    for i, (yr, t, its, c) in enumerate(phases):
        x = 18 + i * 32
        circle(ax, x, H / 2, 3.2, "", c=c, solid=True)
        label(ax, x, H / 2 + 6.5, yr, fs=6.2, bold=True, c=c)
        label(ax, x, H / 2 - 6.5, t, fs=5.8, it=True, c=c)
        for j, it in enumerate(its):
            yy = H / 2 + 12 + j * 11 if j == 0 else H / 2 - 23
            box(ax, x - 14, yy, 28, 10, it, c=c, fs=5.2)
    return save(fig, 32, "Future Research Roadmap")


def fig33():
    fig, ax = canvas(2.8)
    H = 100 * 2.8 / W
    box(ax, 2, H - 16, 96, 12, "", c=PURPLE)
    label(ax, 50, H - 7.5, "Federated XR foundation model (multi-modal: pose, gaze, audio, scene)", fs=5.8, bold=True, c=PURPLE)
    for j, t in enumerate(["adapters on device", "PQC key exchange", "DP fine-tuning"]):
        box(ax, 8 + j * 30, H - 14.5, 26, 4.5, t, c=PURPLE, fill="white", fs=5.2)
    box(ax, 2, H - 36, 46, 16, "Cognitive digital-identity vault\nself-sovereign ID, selective\ndisclosure, avatar unlinkability", c=TEAL, fs=5.3)
    box(ax, 52, H - 36, 46, 16, "Autonomous governance agents\npolicy-as-code, continuous\ncompliance proofs", c=NAVY, fs=5.3)
    box(ax, 2, H - 56, 96, 14, "6G / MEC fabric: semantic communication, in-network aggregation,\nverifiable computation (zk-proofs of correct training)",
        c=GREEN, fs=5.4)
    box(ax, 2, 3, 96, 10, "Users and devices: AR glasses, neural interfaces, haptics", c=BLUE, fs=5.6)
    for x in [25, 75]:
        arrow(ax, (x, H - 20), (x, H - 16), c=GRAY, style="<|-|>")
        arrow(ax, (x, H - 42), (x, H - 36), c=GRAY, style="<|-|>")
    arrow(ax, (50, 13), (50, H - 56), c=GRAY, style="<|-|>")
    return save(fig, 33, "Next-Generation Immersive AI Architecture")


def fig34():
    fig, ax = canvas(2.6)
    H = 100 * 2.6 / W
    box(ax, 33, H / 2 - 8, 34, 16, "PP-FedXR\ncase study", c=NAVY, solid=True, fs=6.8, bold=True)
    cs = [("C1 Threat & risk model\nfor VR/AR telemetry", RED), ("C2 Layered federated\narchitecture", BLUE),
          ("C3 Privacy + security\nlayer with RDP ledger", TEAL), ("C4 Edge personalisation\n< 1 ms inference", GREEN),
          ("C5 Trust score\n& XAI dashboard", PURPLE), ("C6 Reproducible\nevaluation + compliance", ORANGE)]
    pos = [(2, H - 18), (68, H - 18), (2, H / 2 - 7), (68, H / 2 - 7), (2, 4), (68, 4)]
    for (t, c), (x, y) in zip(cs, pos):
        box(ax, x, y, 30, 14, t, c=c, fs=5.4)
        arrow(ax, (x + (30 if x < 50 else 0), y + 7), (33 if x < 50 else 67, H / 2), c=c, style="-", lw=0.6)
    return save(fig, 34, "Contribution Summary Framework")


ALL = [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13,
       fig14, fig15, fig16, fig17, fig19, fig20, fig21, fig26, fig27, fig28, fig29, fig31, fig32,
       fig33, fig34]

if __name__ == "__main__":
    only = sys.argv[1:]
    for f in ALL:
        if not only or f.__name__ in only:
            print(f())

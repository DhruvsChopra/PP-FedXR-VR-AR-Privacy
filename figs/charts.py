"""Result charts (Figures 18, 22-25, 30 and Appendix A1-A4) drawn from results/results.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *  # noqa
import numpy as np
import matplotlib.pyplot as plt
import diagrams

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "results.json")
R = json.load(open(RES))
SER = {"FedAvg": BLUE, "FedProx": TEAL, "DP-FedAvg": AMBER, "PP-FedXR (proposed)": ORANGE}


def style(ax, grid="y"):
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#888"); ax.spines["bottom"].set_color("#888")
    ax.tick_params(colors="#333", length=2.5, width=0.5)
    if grid:
        ax.grid(axis=grid, color="#E5E5E5", lw=0.5); ax.set_axisbelow(True)


def sub(ax, t):
    ax.set_title(t, loc="left", fontsize=7, fontweight="bold", color=NAVY, pad=4)


def save2(fig, name):
    fn = os.path.join(OUT, name + ".png")
    fig.savefig(fn, dpi=600, facecolor="white", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig); return fn


def fig18():
    return diagrams.fig18(task=R["xai"]["task"], groups=R["xai"]["groups"])


def fig22():
    fig, (a, b) = plt.subplots(2, 1, figsize=(W, 3.9), gridspec_kw=dict(height_ratios=[1.35, 1], hspace=0.55))
    for k, c in SER.items():
        h = np.array(R["fl"][k]["hist"])
        a.plot(h[:, 0], 100 * h[:, 1], color=c, lw=1.2 if "proposed" in k else 0.9,
               label=k.replace(" (proposed)", " (prop.)"), ls="-" if k != "FedProx" else (0, (3, 1.5)))
    a.axhline(100 * R["centralised"]["acc"], color=NAVY, lw=0.8, ls="--")
    a.text(200, 100 * R["centralised"]["acc"] + 0.6, f"Centralised {100*R['centralised']['acc']:.1f} %",
           ha="right", va="bottom", fontsize=5.8, color=NAVY)
    a.axhline(100 * R["local_only"]["acc"], color=GRAY, lw=0.8, ls=":")
    a.text(4, 100 * R["local_only"]["acc"] - 0.7, f"Local-only {100*R['local_only']['acc']:.1f} %",
           ha="left", va="top", fontsize=5.8, color=GRAY)
    a.set_xlabel("Communication round"); a.set_ylabel("Test accuracy (%)")
    a.set_ylim(60, 100); a.set_xlim(0, 202)
    a.legend(frameon=False, loc="lower right", ncol=2, bbox_to_anchor=(1.0, 0.0))
    style(a); sub(a, "(a) Convergence on pooled held-out windows")
    names = list(SER)
    x = np.arange(len(names)); wdt = 0.36
    g = [100 * R["fl"][k]["per_user_global"] for k in names]
    p = [100 * R["fl"][k]["per_user_personal"] for k in names]
    b.bar(x - wdt / 2, g, wdt, color=[L[SER[k]] for k in names], edgecolor=[SER[k] for k in names], lw=0.6, label="global model")
    b.bar(x + wdt / 2, p, wdt, color=[SER[k] for k in names], label="after edge personalisation")
    for i in range(len(names)):
        b.text(x[i] + wdt / 2, p[i] + 0.3, f"{p[i]:.1f}", ha="center", va="bottom", fontsize=5.4)
        b.text(x[i] - wdt / 2, g[i] + 0.3, f"{g[i]:.1f}", ha="center", va="bottom", fontsize=5.4)
    b.set_xticks(x, [n.replace(" (proposed)", "\n(proposed)") for n in names])
    b.set_ylim(85, 96.5); b.set_ylabel("Mean per-user acc. (%)")
    b.legend(frameon=False, loc="upper right", fontsize=5.6, ncol=2, bbox_to_anchor=(1.0, 1.04))
    style(b); sub(b, "(b) Per-user accuracy, global vs personalised")
    return save2(fig, "Fig 22 Model Accuracy Results")


def fig23():
    fig, (a, b) = plt.subplots(2, 1, figsize=(W, 3.9), gridspec_kw=dict(hspace=0.55))
    pu = R["pu"]
    eps = [d["eps"] for d in pu]; acc = [100 * d["acc"] for d in pu]
    a.plot(eps, acc, "-o", color=ORANGE, ms=3, lw=1.0, label="PP-FedXR (z swept)")
    for d in pu:
        a.annotate(f"z={d['z']}", (d["eps"], 100 * d["acc"]), textcoords="offset points", xytext=(3, -8),
                   fontsize=5.3, color=DARK)
    a.axhline(100 * R["fl"]["FedAvg"]["acc"], color=BLUE, lw=0.8, ls="--")
    a.text(2.05, 100 * R["fl"]["FedAvg"]["acc"] + 0.4, "FedAvg, no DP", fontsize=5.6, color=BLUE)
    a.axhline(100 * R["centralised"]["acc"], color=NAVY, lw=0.8, ls=":")
    a.text(2.05, 100 * R["centralised"]["acc"] + 0.4, "Centralised, no privacy", fontsize=5.6, color=NAVY)
    a.set_xscale("log"); a.set_xlabel(r"Client-level privacy budget $\varepsilon$ ($\delta=10^{-4}$, log scale)")
    a.set_ylabel("Test accuracy (%)"); a.set_ylim(80, 98)
    style(a, "both"); sub(a, "(a) Accuracy vs privacy budget, T = 200, q = 0.1")
    rid = R["reid"]
    lab = ["raw" if d["b"] == 0 else f"b={d['b']}" for d in rid]
    x = np.arange(len(rid)); w = 0.27
    b.bar(x - w, [100 * d["session"] for d in rid], w, color=RED, label="re-ID, session")
    b.bar(x, [100 * d["top1"] for d in rid], w, color=L[RED], edgecolor=RED, lw=0.6, label="re-ID, 2 s window")
    b.bar(x + w, [100 * d["task_acc"] for d in rid], w, color=GREEN, label="task accuracy")
    b.set_xticks(x, lab); b.set_ylabel("Percent"); b.set_ylim(0, 105)
    b.set_xlabel("Centralised data with Laplace local-DP noise of scale b")
    b.legend(frameon=False, fontsize=5.5, ncol=3, loc="upper right", bbox_to_anchor=(1.0, 1.08))
    style(b); sub(b, "(b) Local DP alternative: identity leakage vs utility")
    return save2(fig, "Fig 23 Privacy vs Utility Analysis")


def fig24():
    fig = plt.figure(figsize=(W, 4.3))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], hspace=0.62, wspace=0.42)
    a = fig.add_subplot(gs[0, :])
    lat = R["latency"]
    for k, c, n in [("edge_samples", GREEN, "Edge (on-device)"), ("cloud_samples", NAVY, "Cloud offload")]:
        v = np.sort(lat[k]); a.plot(v, np.arange(1, len(v) + 1) / len(v), color=c, lw=1.1, label=n)
    a.axvline(20, color=RED, lw=0.8, ls="--"); a.text(21, 0.08, "20 ms motion-to-\nphoton budget", fontsize=5.4, color=RED)
    a.set_xscale("log"); a.set_xlabel("Feature extraction + inference latency (ms, log scale)")
    a.set_ylabel("CDF"); a.legend(frameon=False, loc="center left")
    style(a, "both"); sub(a, "(a) End-to-end inference latency per 2 s window")
    b = fig.add_subplot(gs[1, 0])
    sc = R["scale"]
    m = [d["per_round"] for d in sc]
    b.plot(m, [100 * d["acc"] for d in sc], "-o", color=ORANGE, ms=3)
    for d in sc:
        b.annotate(f"$\\varepsilon$={d['eps']:.1f}", (d["per_round"], 100 * d["acc"]), textcoords="offset points",
                   xytext=(-6, -10 if d["per_round"] < 300 else 5), fontsize=5.0)
    b.set_xscale("log"); b.set_xticks(m, [str(v) for v in m]); b.minorticks_off()
    b.set_xlabel("Clients per round m"); b.set_ylabel("Accuracy (%)"); b.set_ylim(70, 97)
    style(b, "both"); sub(b, "(b) Cohort size, 100 rounds")
    c = fig.add_subplot(gs[1, 1])
    sa = R["secagg"]
    n = [d["n"] for d in sa]
    c.plot(n, [d["per_client_ms"] for d in sa], "-o", color=PURPLE, ms=3, label="per client")
    c.annotate(f"round total\n{sa[-1]['mask_seconds_total']:.2f} s", (n[-1], sa[-1]["per_client_ms"]),
               textcoords="offset points", xytext=(-34, 4), fontsize=5.2, color=PURPLE)
    c.set_xlabel("Cohort size n"); c.set_ylabel("Per-client masking (ms)"); c.set_ylim(0, 7.5)
    style(c, "both"); sub(c, "(c) SecAgg overhead")
    return save2(fig, "Fig 24 Latency and Scalability Analysis")


def comm_eff(bytes_):
    lo, hi = R["comm"]["q8_bytes_per_update"], R["comm"]["raw_bytes_per_sec"] * 3600
    return 1 - np.log10(bytes_ / lo) / np.log10(hi / lo)


def radar_values():
    T = R["trust"]; lat = R["latency"]
    lat_score = lambda ms: float(np.clip(1 - ms / 100, 0, 1))
    raw_h = R["comm"]["raw_bytes_per_sec"] * 3600
    V = {
        "Centralised": [T["Centralised"]["P"], T["Centralised"]["U"], T["Centralised"]["R"], T["Centralised"]["T"],
                        comm_eff(raw_h), lat_score(lat["cloud_p95"])],
        "FedAvg": [T["FedAvg"]["P"], T["FedAvg"]["U"], T["FedAvg"]["R"], T["FedAvg"]["T"],
                   comm_eff(R["comm"]["fp32_bytes_per_update"]), lat_score(lat["edge_p95"])],
        "DP-FedAvg": [T["DP-FedAvg"]["P"], T["DP-FedAvg"]["U"], T["DP-FedAvg"]["R"], T["DP-FedAvg"]["T"],
                      comm_eff(R["comm"]["fp32_bytes_per_update"]), lat_score(lat["edge_p95"])],
        "PP-FedXR (proposed)": [T["PP-FedXR (proposed)"]["P"], T["PP-FedXR (proposed)"]["U"], T["PP-FedXR (proposed)"]["R"],
                                T["PP-FedXR (proposed)"]["T"], comm_eff(R["comm"]["q8_bytes_per_update"]), lat_score(lat["edge_p95"])],
    }
    return ["Privacy", "Utility", "Robustness", "Transparency", "Comm.\nefficiency", "Latency"], V


def fig25():
    axes_l, V = radar_values()
    ang = np.linspace(0, 2 * np.pi, len(axes_l), endpoint=False).tolist(); ang += ang[:1]
    fig = plt.figure(figsize=(W, 3.0)); ax = fig.add_subplot(111, polar=True)
    cols = {"Centralised": NAVY, "FedAvg": BLUE, "DP-FedAvg": AMBER, "PP-FedXR (proposed)": ORANGE}
    for k, v in V.items():
        vv = v + v[:1]
        ax.plot(ang, vv, color=cols[k], lw=1.2 if "prop" in k else 0.9, label=k)
        ax.fill(ang, vv, color=cols[k], alpha=0.12 if "prop" in k else 0.04)
    ax.set_xticks(ang[:-1], axes_l, fontsize=6.2)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0], ["0.25", "0.5", "0.75", "1"], fontsize=5.2, color=GRAY)
    ax.set_ylim(0, 1.05); ax.spines["polar"].set_color("#BBB"); ax.grid(color="#DDD", lw=0.5)
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.05, 1.05), fontsize=5.8)
    return save2(fig, "Fig 25 Comparative Radar Chart")


def cost_model():
    """Illustrative 3-year cost model for a 10,000-headset enterprise fleet (assumptions in Table XIV)."""
    fleet, hours_day, days = 10_000, 1.0, 250
    raw_gb_year = R["comm"]["raw_bytes_per_sec"] * 3600 * hours_day * days * fleet / 1e9
    storage = raw_gb_year * 1.5 * 0.023 * 12 * 3 * 0.5      # avg half-year residency, replication 1.5x
    egress = raw_gb_year * 3 * 0.02
    breach_cost, p_central, p_fl = 4.88e6, 0.10, 0.03
    breach = 3 * breach_cost * p_central; breach_fl = 3 * breach_cost * p_fl
    compliance_c, compliance_fl = 3 * 180_000, 3 * 90_000
    fl_infra = 3 * 60_000 + 120_000                         # aggregator + one-off integration
    fl_update_gb = R["comm"]["q8_bytes_per_update"] * fleet * days * 4 / 1e9
    return dict(raw_gb_year=raw_gb_year,
                central=dict(storage=storage, egress=egress, breach=breach, compliance=compliance_c, infra=3 * 40_000),
                fl=dict(storage=fl_update_gb * 0.023 * 3, egress=fl_update_gb * 0.02 * 3, breach=breach_fl,
                        compliance=compliance_fl, infra=fl_infra))


def fig30():
    cm = cost_model()
    fig = plt.figure(figsize=(W, 3.5))
    gs = fig.add_gridspec(2, 2, hspace=0.75, wspace=0.5)
    a = fig.add_subplot(gs[0, :])
    cats = ["storage", "egress", "breach", "compliance", "infra"]
    labs = ["Storage", "Egress", "Expected\nbreach loss", "Compliance\neffort", "Infrastructure"]
    x = np.arange(len(cats)); w = 0.38
    a.bar(x - w / 2, [cm["central"][c] / 1e3 for c in cats], w, color=NAVY, label="Centralised analytics")
    a.bar(x + w / 2, [cm["fl"][c] / 1e3 for c in cats], w, color=ORANGE, label="PP-FedXR")
    a.set_xticks(x, labs, fontsize=5.6); a.set_ylabel("3-year cost (k USD)")
    a.legend(frameon=False, fontsize=5.6); style(a)
    tc, tf = sum(cm["central"].values()), sum(cm["fl"].values())
    sub(a, f"(a) Illustrative 3-year TCO: {tc/1e6:.2f} M vs {tf/1e6:.2f} M USD")
    b = fig.add_subplot(gs[1, 0])
    b.bar(["Centralised", "PP-FedXR"], [cm["raw_gb_year"] / 1e3, 0.0], color=[NAVY, ORANGE])
    b.text(1, 0.05 * cm["raw_gb_year"] / 1e3, "0 TB raw", ha="center", fontsize=5.6, color=ORANGE)
    b.set_ylabel("Raw telemetry held (TB/yr)"); style(b); sub(b, "(b) Data exposure")
    c = fig.add_subplot(gs[1, 1])
    T = R["trust"]; ks = ["Centralised", "FedAvg", "DP-FedAvg", "PP-FedXR (proposed)"]
    c.barh([k.replace(" (proposed)", "") for k in ks], [T[k]["score"] for k in ks],
           color=[NAVY, BLUE, AMBER, ORANGE])
    for i, k in enumerate(ks):
        c.text(T[k]["score"] + 0.02, i, f"{T[k]['score']:.2f}", va="center", fontsize=5.6)
    c.set_xlim(0, 1.15); c.set_xlabel("Trust score TS"); style(c, "x"); sub(c, "(c) Trust score")
    return save2(fig, "Fig 30 Business Impact Dashboard")


def appA():
    out = []
    # A1 poisoning
    fig, ax = plt.subplots(figsize=(W, 2.2))
    P_ = R["poison"]
    for agg, c, n in [("mean", BLUE, "FedAvg (mean)"), ("median", TEAL, "Coordinate median"),
                      ("trimmed", PURPLE, "Trimmed mean (20 %)"), ("normbound", ORANGE, "PP-FedXR (norm-bound + DP)")]:
        d = [p for p in P_ if p["agg"] == agg]
        ax.plot([100 * p["frac"] for p in d], [100 * p["acc"] for p in d], "-o", ms=3, color=c, label=n)
    ax.set_xlabel("Malicious clients (%)"); ax.set_ylabel("Test accuracy (%)"); ax.set_xticks([0, 10, 20, 30])
    ax.legend(frameon=False, fontsize=5.6); style(ax, "both")
    out.append(save2(fig, "Fig A1 Poisoning Robustness"))
    # A2 importance identity vs task
    fig, ax = plt.subplots(figsize=(W, 2.4))
    g = R["xai"]["groups"]; y = np.arange(len(g)); h = 0.38
    ax.barh(y - h / 2, [100 * v for v in R["xai"]["task"]], h, color=PURPLE, label="activity model (PP-FedXR)")
    ax.barh(y + h / 2, [100 * v for v in R["xai"]["identity"]], h, color=RED, label="re-identification attacker")
    ax.set_yticks(y, g); ax.invert_yaxis(); ax.set_xlabel("Accuracy drop when group is permuted (pp)")
    ax.legend(frameon=False, fontsize=5.6, loc="lower center", ncol=2, bbox_to_anchor=(0.4, 1.0)); style(ax, "x")
    out.append(save2(fig, "Fig A2 Sensor-Group Importance Task vs Identity"))
    # A3 confusion
    from vrfl_labels import ACT
    cm = np.array(R["confusion"]); cmn = cm / cm.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(W, 3.0))
    im = ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    for i in range(8):
        for j in range(8):
            ax.text(j, i, f"{100*cmn[i, j]:.0f}", ha="center", va="center", fontsize=5.2,
                    color="white" if cmn[i, j] > 0.5 else DARK)
    ax.set_xticks(range(8), ACT, rotation=40, ha="right", fontsize=5.6)
    ax.set_yticks(range(8), ACT, fontsize=5.6)
    ax.set_xlabel("Predicted activity"); ax.set_ylabel("True activity")
    fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02).ax.tick_params(labelsize=5.4)
    out.append(save2(fig, "Fig A3 Confusion Matrix PP-FedXR"))
    return out


if __name__ == "__main__":
    for f in [fig18, fig22, fig23, fig24, fig25, fig30, appA]:
        print(f())
    cm = cost_model(); print({k: (round(sum(v.values())) if isinstance(v, dict) else v) for k, v in cm.items()})
    print(cm)
    axes_l, V = radar_values(); print(axes_l); [print(k, np.round(v, 3)) for k, v in V.items()]

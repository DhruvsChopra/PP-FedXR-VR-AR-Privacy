"""Runs every experiment reported in the case study and writes results/results.json.
Usage:  python run_all.py            (approx. 10-15 min on a 2-core laptop CPU)
"""
import json, os, sys, time
import vrfl  # noqa: F401  (pins BLAS threads)
import numpy as np
from vrfl import data as D, privacy as P
from vrfl.fl import run_fl, personalise, train_centralised, train_local_only, pooled
from vrfl.attacks import reidentification, membership_inference
from vrfl.model import MLP

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "run_log.txt"), "w")


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); LOG.write(s + "\n"); LOG.flush()


R = {}
ROUNDS, M, K = 200, 100, 1000
DELTA = 1e-4
PROPOSED = dict(dp_z=1.0, clip_C=0.5, server_mom=0.9, server_lr=0.5)

t0 = time.time()
X, Y, U = D.make_dataset(n_users=K)
cl = D.split_per_user(X, Y, U)
np.savez_compressed(os.path.join(OUT, "vr_motionpriv_synth.npz"), X=X, Y=Y, U=U)
R["dataset"] = dict(samples=int(len(Y)), users=K, features=D.N_FEAT, classes=D.N_CLASS,
                    train=int(sum(len(c["ytr"]) for c in cl.values())),
                    test=int(sum(len(c["yte"]) for c in cl.values())),
                    class_counts=np.bincount(Y).tolist(),
                    samples_per_user=[int(np.percentile(np.bincount(U), q)) for q in (5, 50, 95)])
log("dataset", R["dataset"])

# ------------------------------------------------------------ E1 accuracy & convergence
log("E1 baselines")
cen = train_centralised(cl, epochs=10)
R["centralised"] = dict(acc=cen["acc"], hist=cen["hist"])
R["local_only"] = dict(acc=train_local_only(cl))
runs = {
    "FedAvg": dict(),
    "FedProx": dict(algo="fedprox", prox_mu=0.01),
    "DP-FedAvg": dict(dp_z=1.0, clip_C=0.5),
    "PP-FedXR (proposed)": dict(PROPOSED, secagg=True),
}
R["fl"] = {}
for name, cfg in runs.items():
    r = run_fl(cl, rounds=ROUNDS, per_round=M, eval_every=10, **cfg)
    mi = membership_inference(r["w"], cl)
    g, p = personalise(cl, r["w"])
    R["fl"][name] = dict(acc=r["acc"], hist=r["hist"], bytes_up=r["bytes_up"],
                         seconds=r["seconds"], secagg_seconds=r["secagg_seconds"],
                         mi_auc=mi[0], mi_adv=mi[1], per_user_global=g, per_user_personal=p)
    if name == "PP-FedXR (proposed)":
        np.save(os.path.join(OUT, "global_model_proposed.npy"), r["w"])
        W_PROP = r["w"]
    log(f"  {name:22s} acc={r['acc']:.4f} mi_auc={mi[0]:.3f} pers={p:.4f} t={r['seconds']:.1f}s")
mi_c = membership_inference(cen["w"], cl)
R["centralised"].update(mi_auc=mi_c[0], mi_adv=mi_c[1])
log("  centralised", cen["acc"], "local-only", R["local_only"]["acc"], "mi", mi_c)
R["n_params"] = MLP().n_params
for name in R["fl"]:
    z = runs[name].get("dp_z", 0)
    R["fl"][name]["epsilon"] = P.epsilon(M / K, z, ROUNDS, DELTA) if z > 0 else None
log("  eps proposed", R["fl"]["PP-FedXR (proposed)"]["epsilon"])

# ------------------------------------------------------------ E2 privacy-utility sweep
log("E2 privacy-utility")
R["pu"] = []
for z in [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
    r = run_fl(cl, rounds=ROUNDS, per_round=M, eval_every=ROUNDS, **dict(PROPOSED, dp_z=z))
    eps = P.epsilon(M / K, z, ROUNDS, DELTA)
    mi = membership_inference(r["w"], cl)
    R["pu"].append(dict(z=z, eps=eps, acc=r["acc"], mi_auc=mi[0]))
    log(f"  z={z} eps={eps:.2f} acc={r['acc']:.4f} mi={mi[0]:.3f}")

# ------------------------------------------------------------ E3 re-identification
log("E3 re-identification")
R["reid"] = []
for b in [0, 0.5, 1.0, 2.0, 3.0]:
    t1, t5, ses, rid_model = reidentification(cl, epochs=12, noise_b=b or None)
    if b:
        cu = train_centralised(cl, epochs=10, noise_b=b)["acc"]
    else:
        cu = cen["acc"]; RID_MODEL = rid_model
    R["reid"].append(dict(b=b, eps_ldp_per_feature=(None if not b else 1.0 / b),
                          top1=t1, top5=t5, session=ses, task_acc=cu))
    log(f"  b={b} window-top1={t1:.3f} top5={t5:.3f} session={ses:.3f} task-acc={cu:.4f}")

# ------------------------------------------------------------ E4 poisoning robustness
log("E4 poisoning")
R["poison"] = []
for frac in [0.0, 0.1, 0.2, 0.3]:
    for agg in ["mean", "median", "trimmed", "normbound"]:
        cfg = dict(agg=agg, malicious_frac=frac)
        if agg == "normbound":
            cfg = dict(PROPOSED, malicious_frac=frac)
        r = run_fl(cl, rounds=120, per_round=M, eval_every=120, **cfg)
        R["poison"].append(dict(frac=frac, agg=agg, acc=r["acc"]))
        log(f"  frac={frac} agg={agg} acc={r['acc']:.4f}")

# ------------------------------------------------------------ E5 communication
log("E5 communication")
r8 = run_fl(cl, rounds=ROUNDS, per_round=M, eval_every=ROUNDS, quant_bits=8, **PROPOSED)
R["comm"] = dict(fp32_bytes_per_update=R["n_params"] * 4,
                 q8_bytes_per_update=R["n_params"] + 8,
                 q8_acc=r8["acc"], fp32_acc=R["fl"]["PP-FedXR (proposed)"]["acc"],
                 # raw-stream comparison: HMD pose(7)+2 controllers(14)+gaze(6)=27 float32 @ 90 Hz
                 raw_bytes_per_sec=27 * 4 * 90)
log("  ", R["comm"])

# ------------------------------------------------------------ E6 secure aggregation
log("E6 secure aggregation")
rng = np.random.default_rng(1)
R["secagg"] = []
d = R["n_params"]
for n in [10, 25, 50, 100, 200]:
    ups = [rng.normal(0, 0.02, d) for _ in range(n)]
    s, masked, tm = P.secure_aggregate(ups, seed=n)
    err = float(np.abs(s - P.plain_quantised_sum(ups)).max())
    corr = float(np.corrcoef(P._decode(masked[0]), ups[0])[0, 1])
    R["secagg"].append(dict(n=n, mask_seconds_total=tm, per_client_ms=1000 * tm / n,
                            max_abs_error=err, masked_corr=corr))
    log(f"  n={n} total={tm:.3f}s per-client={1000*tm/n:.2f}ms err={err:.2e} corr={corr:.4f}")

# ------------------------------------------------------------ E7 latency
log("E7 latency")
m = MLP(); m.set(W_PROP)
win = rng.normal(0, 1, (180, 27)).astype(np.float32)   # 2 s @ 90 Hz, 27 channels
def feat(w):
    return np.concatenate([w[:, :24].reshape(180, 8, 3).mean(0).ravel(),
                           w[:, :24].reshape(180, 8, 3).std(0).ravel()])
fx = []; inf = []
x1 = X[:1]
for _ in range(5000):
    a = time.perf_counter(); f = feat(win); b = time.perf_counter(); m.predict_proba(x1); c = time.perf_counter()
    fx.append((b - a) * 1000); inf.append((c - b) * 1000)
fx, inf = np.array(fx), np.array(inf)
edge = fx + inf
rtt = rng.lognormal(np.log(48), 0.35, 5000)            # modelled Wi-Fi/5G round trip to cloud (ms)
upl = (48 * 4 * 8) / 20e6 * 1000                       # 192-byte feature vector on 20 Mbps uplink
cloud = fx + upl + rtt + inf
R["latency"] = dict(feature_ms_p50=float(np.median(fx)), infer_ms_p50=float(np.median(inf)),
                    edge_p50=float(np.median(edge)), edge_p95=float(np.percentile(edge, 95)),
                    cloud_p50=float(np.median(cloud)), cloud_p95=float(np.percentile(cloud, 95)),
                    edge_hist=np.histogram(edge, bins=30)[0].tolist(),
                    edge_samples=edge[:2000].tolist(), cloud_samples=cloud[:2000].tolist())
log("  ", {k: v for k, v in R["latency"].items() if not isinstance(v, list)})

# ------------------------------------------------------------ E8 scalability
log("E8 scalability")
R["scale"] = []
for mm in [25, 50, 100, 200, 400]:
    r = run_fl(cl, rounds=100, per_round=mm, eval_every=100, **PROPOSED)
    # SecAgg cost for this cohort size (one measured round)
    ups = [rng.normal(0, 0.02, d) for _ in range(min(mm, 200))]
    _, _, tm = P.secure_aggregate(ups, seed=mm)
    if mm > 200:
        tm *= (mm / 200) ** 2                                 # O(n^2) pairwise extrapolation
    comp_per_round = r["seconds"] / 100
    comm_per_client = R["n_params"] * 4 * 8 / 20e6           # seconds on 20 Mbps uplink
    R["scale"].append(dict(per_round=mm, acc=r["acc"], eps=P.epsilon(mm / K, 1.0, 100, DELTA),
                           sim_seconds_per_round=comp_per_round, secagg_seconds=tm,
                           client_upload_s=comm_per_client,
                           server_bytes_per_round=mm * R["n_params"] * 4))
    log(f"  m={mm} acc={r['acc']:.4f} eps={R['scale'][-1]['eps']:.2f} secagg={tm:.3f}s")

# ------------------------------------------------------------ E9 explainability
log("E9 explainability")
xte, yte = pooled(cl, "te")
def group_importance(model, x, y, reps=3):
    base = model.accuracy(x, y); out = []
    for g in range(8):
        drops = []
        for _ in range(reps):
            xp = x.copy(); idx = rng.permutation(len(x))
            xp[:, g * 6:(g + 1) * 6] = x[idx, g * 6:(g + 1) * 6]
            drops.append(base - model.accuracy(xp, y))
        out.append(float(np.mean(drops)))
    return base, out
_, imp_task = group_importance(m, xte, yte)
uid = np.concatenate([np.full(len(c["yte"]), u) for u, c in cl.items()])
_, imp_id = group_importance(RID_MODEL, xte, uid)
R["xai"] = dict(groups=D.FEATURE_GROUPS, task=imp_task, identity=imp_id)
log("  task", np.round(imp_task, 3), "identity", np.round(imp_id, 3))
# per-class accuracy / confusion for the proposed model
pred = m.predict_proba(xte).argmax(1)
conf = np.zeros((8, 8), int)
for a, b in zip(yte, pred):
    conf[a, b] += 1
R["confusion"] = conf.tolist()

# ------------------------------------------------------------ E10 trust score
log("E10 trust score")
cen_acc = cen["acc"]
reid_raw = R["reid"][0]["session"]
def trust(acc, mi_auc, robust, transparency, exposure):
    Pv = (1 - 2 * abs(mi_auc - 0.5)) * (1 - exposure)
    Uv = acc / cen_acc
    return dict(P=Pv, U=Uv, R=robust, T=transparency,
                score=0.35 * Pv + 0.20 * Uv + 0.25 * robust + 0.20 * transparency)
poison = {(p["frac"], p["agg"]): p["acc"] for p in R["poison"]}
rob_mean = poison[(0.2, "mean")] / poison[(0.0, "mean")]
rob_nb = poison[(0.2, "normbound")] / poison[(0.0, "normbound")]
fl = R["fl"]
R["trust"] = {
    "Centralised": trust(cen_acc, R["centralised"]["mi_auc"], 1.0, 2 / 6, reid_raw),
    "FedAvg": trust(fl["FedAvg"]["acc"], fl["FedAvg"]["mi_auc"], rob_mean, 2 / 6, 0.0),
    "FedProx": trust(fl["FedProx"]["acc"], fl["FedProx"]["mi_auc"], rob_mean, 2 / 6, 0.0),
    "DP-FedAvg": trust(fl["DP-FedAvg"]["acc"], fl["DP-FedAvg"]["mi_auc"], rob_nb, 3 / 6, 0.0),
    "PP-FedXR (proposed)": trust(fl["PP-FedXR (proposed)"]["acc"], fl["PP-FedXR (proposed)"]["mi_auc"],
                                 rob_nb, 6 / 6, 0.0),
}
for k, v in R["trust"].items():
    log(f"  {k:22s} " + " ".join(f"{a}={b:.3f}" for a, b in v.items()))

R["runtime_seconds"] = time.time() - t0
json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=1)
log("done in", round(R["runtime_seconds"], 1), "s")

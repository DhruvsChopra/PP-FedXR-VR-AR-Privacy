"""Federated training loop covering FedAvg, FedProx, DP-FedAvg, robust aggregation,
quantisation, server momentum (the proposed PP-FedXR configuration) and edge
personalisation."""
import time
import numpy as np
from .model import MLP, local_sgd
from . import privacy as P


def pooled(clients, key):
    xs = np.concatenate([c["x" + key] for c in clients.values()])
    ys = np.concatenate([c["y" + key] for c in clients.values()])
    return xs, ys


def run_fl(clients, rounds=150, per_round=100, epochs=2, lr=0.1, bs=32,
           algo="fedavg", prox_mu=0.0, dp_z=0.0, clip_C=None, agg="mean",
           server_lr=1.0, server_mom=0.0, quant_bits=None, malicious_frac=0.0,
           attack_scale=5.0, secagg=False, seed=0, eval_every=5, log=None):
    rng = np.random.default_rng(seed)
    ids = np.array(list(clients.keys()))
    K = len(ids)
    mal = set(rng.choice(ids, size=int(malicious_frac * K), replace=False).tolist())
    model = MLP(seed=seed)
    w = model.get().astype(np.float64)
    v = np.zeros_like(w)
    xte, yte = pooled(clients, "te")
    hist = []
    agg_fn = dict(mean=P.agg_mean, median=P.agg_median, trimmed=P.agg_trimmed,
                  normbound=P.agg_normbound)[agg]
    bytes_up = 0
    secagg_time = 0.0
    t_start = time.perf_counter()
    for r in range(1, rounds + 1):
        sel = rng.choice(ids, size=per_round, replace=False)
        ups, wts = [], []
        for c in sel:
            d = clients[c]
            wl = local_sgd(model, w.astype(np.float32), d["xtr"], d["ytr"], epochs, bs, lr, rng,
                           prox_mu if algo == "fedprox" else 0.0)
            u = wl.astype(np.float64) - w
            if c in mal:                                   # model-poisoning client
                u = -attack_scale * u
            if clip_C is not None:
                u, _ = P.clip(u, clip_C)
            if quant_bits:
                u = P.stochastic_quantise(u, quant_bits, rng)
                bytes_up += len(u) * quant_bits / 8 + 8
            else:
                bytes_up += len(u) * 4
            ups.append(u); wts.append(len(d["ytr"]))
        if secagg:
            # distributed DP: every client adds N(0,(zC)^2/m) before masking, so the server
            # only ever decodes the already-noised sum (total noise std = zC)
            if dp_z > 0:
                ups = [u + rng.normal(0, dp_z * clip_C / np.sqrt(per_round), size=w.shape)
                       for u in ups]
            s, _, tm = P.secure_aggregate(ups, seed=r)
            secagg_time += tm
            delta = s / per_round
        elif dp_z > 0:                                     # client-level DP (central noise)
            s = np.sum(ups, axis=0) + rng.normal(0, dp_z * clip_C, size=w.shape)
            delta = s / per_round
        else:
            delta = agg_fn(ups, wts) if agg == "mean" else agg_fn(ups)
        v = server_mom * v + delta
        w = w + server_lr * v
        if r % eval_every == 0 or r == rounds:
            model.set(w)
            acc = model.accuracy(xte, yte)
            hist.append((r, acc))
            if log:
                log(f"  round {r:4d}  test-acc {acc:.4f}")
    model.set(w)
    return dict(w=w, hist=hist, acc=model.accuracy(xte, yte), bytes_up=bytes_up,
                seconds=time.perf_counter() - t_start, n_params=model.n_params,
                secagg_seconds=secagg_time)


def personalise(clients, w, epochs=1, lr=0.05, seed=0):
    """Edge-layer personalisation: each headset fine-tunes the global model on its own
    data and is evaluated on its own held-out windows. Raw data never leaves the device."""
    rng = np.random.default_rng(seed)
    m = MLP(); accs_g, accs_p = [], []
    for c, d in clients.items():
        m.set(w); accs_g.append(m.accuracy(d["xte"], d["yte"]))
        wl = local_sgd(m, w.astype(np.float32), d["xtr"], d["ytr"], epochs, 16, lr, rng)
        m.set(wl); accs_p.append(m.accuracy(d["xte"], d["yte"]))
    return float(np.mean(accs_g)), float(np.mean(accs_p))


def train_centralised(clients, epochs=15, lr=0.1, bs=64, seed=0, noise_b=None):
    """Centralised baseline; optional Laplace local-DP noise on raw features (scale b)."""
    rng = np.random.default_rng(seed)
    x, y = pooled(clients, "tr")
    if noise_b:
        x = x + rng.laplace(0, noise_b, size=x.shape).astype(np.float32)
    m = MLP(seed=seed)
    w = m.get()
    hist = []
    xte, yte = pooled(clients, "te")
    for e in range(epochs):
        w = local_sgd(m, w, x, y, 1, bs, lr, rng)
        m.set(w); hist.append((e + 1, m.accuracy(xte, yte)))
    return dict(w=w, acc=hist[-1][1], hist=hist)


def train_local_only(clients, epochs=20, lr=0.1, seed=0):
    rng = np.random.default_rng(seed)
    m = MLP(seed=seed); w0 = m.get(); accs = []
    for d in clients.values():
        w = local_sgd(m, w0, d["xtr"], d["ytr"], epochs, 16, lr, rng)
        m.set(w); accs.append(m.accuracy(d["xte"], d["yte"]))
    return float(np.mean(accs))

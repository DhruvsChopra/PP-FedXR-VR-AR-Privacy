"""Privacy attacks used in the risk assessment."""
import numpy as np
from .model import MLP, local_sgd


def reidentification(clients, epochs=12, noise_b=None, seed=0, n_users=None):
    """Attacker with access to raw (centralised) telemetry trains a user-ID classifier on
    some windows of every user and tries to re-identify the held-out windows."""
    rng = np.random.default_rng(seed)
    ids = sorted(clients)[:n_users] if n_users else sorted(clients)
    remap = {u: i for i, u in enumerate(ids)}
    xtr = np.concatenate([clients[u]["xtr"] for u in ids])
    ytr = np.concatenate([np.full(len(clients[u]["ytr"]), remap[u]) for u in ids])
    xte = np.concatenate([clients[u]["xte"] for u in ids])
    yte = np.concatenate([np.full(len(clients[u]["yte"]), remap[u]) for u in ids])
    if noise_b:
        xtr = xtr + rng.laplace(0, noise_b, xtr.shape).astype(np.float32)
        xte = xte + rng.laplace(0, noise_b, xte.shape).astype(np.float32)
    m = MLP(48, 256, len(ids), seed=seed)
    w = m.get()
    for _ in range(epochs):
        w = local_sgd(m, w, xtr, ytr, 1, 64, 0.2, rng)
    m.set(w)
    p = m.predict_proba(xte)
    top1 = float((p.argmax(1) == yte).mean())
    top5 = float((np.argsort(-p, 1)[:, :5] == yte[:, None]).any(1).mean())
    # session-level: accumulate evidence over all held-out windows of the same user
    lp = np.log(p + 1e-12)
    hits = [int(lp[yte == k].sum(0).argmax() == k) for k in range(len(ids))]
    return top1, top5, float(np.mean(hits)), m


def auc(scores_pos, scores_neg):
    s = np.concatenate([scores_pos, scores_neg])
    lab = np.concatenate([np.ones(len(scores_pos)), np.zeros(len(scores_neg))])
    order = np.argsort(s)
    ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    npos, nneg = len(scores_pos), len(scores_neg)
    return float((ranks[lab == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def membership_inference(w, clients, n=4000, seed=0):
    """Loss-threshold membership inference (Yeom et al.): lower loss -> 'member'.
    Returns AUC and the best balanced attack advantage (TPR-FPR)."""
    rng = np.random.default_rng(seed)
    m = MLP(); m.set(w)
    xtr = np.concatenate([c["xtr"] for c in clients.values()])
    ytr = np.concatenate([c["ytr"] for c in clients.values()])
    xte = np.concatenate([c["xte"] for c in clients.values()])
    yte = np.concatenate([c["yte"] for c in clients.values()])
    i = rng.choice(len(ytr), min(n, len(ytr)), replace=False)
    j = rng.choice(len(yte), min(n, len(yte)), replace=False)
    lin = m.loss_per_sample(xtr[i], ytr[i]); lout = m.loss_per_sample(xte[j], yte[j])
    a = auc(-lin, -lout)
    th = np.quantile(np.concatenate([lin, lout]), np.linspace(0.01, 0.99, 99))
    adv = max(abs((lin <= t).mean() - (lout <= t).mean()) for t in th)
    return a, float(adv)

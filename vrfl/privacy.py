"""Privacy and security primitives: client-level DP, RDP accounting, secure aggregation,
robust aggregation and update quantisation."""
import math
import time
import numpy as np


# ---------------------------------------------------------------- differential privacy
def clip(update, C):
    n = np.linalg.norm(update)
    return update * min(1.0, C / (n + 1e-12)), n


def rdp_subsampled_gaussian(q, z, alpha):
    """RDP of the Poisson-subsampled Gaussian mechanism at integer order alpha
    (Mironov, Talwar & Zhang, 2019, Sec. 3.3)."""
    log_terms = []
    for k in range(alpha + 1):
        lc = math.lgamma(alpha + 1) - math.lgamma(k + 1) - math.lgamma(alpha - k + 1)
        t = lc + (alpha - k) * math.log(1 - q) + (k * math.log(q) if k > 0 else 0.0) \
            + (k * k - k) / (2 * z * z)
        log_terms.append(t)
    m = max(log_terms)
    return (m + math.log(sum(math.exp(t - m) for t in log_terms))) / (alpha - 1)


def epsilon(q, z, steps, delta, orders=range(2, 257)):
    best = float("inf")
    for a in orders:
        e = steps * rdp_subsampled_gaussian(q, z, a) + math.log(1 / delta) / (a - 1)
        best = min(best, e)
    return best


# ---------------------------------------------------------------- secure aggregation
MOD = 2 ** 32
SCALE = 2 ** 16


def _encode(v, clip_range=8.0):
    v = np.clip(v, -clip_range, clip_range)
    return np.mod(np.round(v * SCALE).astype(np.int64), MOD)


def _decode(s):
    s = np.where(s >= MOD // 2, s - MOD, s)
    return s.astype(np.float64) / SCALE


def secure_aggregate(updates, seed=0):
    """Pairwise-additive-masking secure aggregation (Bonawitz et al. style, honest-but-
    curious server, no dropouts). Each pair (i,j) derives a shared mask from a common seed;
    i adds it, j subtracts it, so masks cancel only in the sum. Returns (sum, masked
    individual vectors seen by the server, mask-generation seconds)."""
    n, d = len(updates), len(updates[0])
    enc = [_encode(u) for u in updates]
    masked = [e.copy() for e in enc]
    t0 = time.perf_counter()
    for i in range(n):
        for j in range(i + 1, n):
            prg = np.random.default_rng(hash((seed, i, j)) & 0xFFFFFFFF)
            m = prg.integers(0, MOD, size=d, dtype=np.int64)
            masked[i] = np.mod(masked[i] + m, MOD)
            masked[j] = np.mod(masked[j] - m, MOD)
    t_mask = time.perf_counter() - t0
    total = np.zeros(d, np.int64)
    for m in masked:
        total = np.mod(total + m, MOD)
    return _decode(total), masked, t_mask


def plain_quantised_sum(updates):
    total = np.zeros(len(updates[0]), np.int64)
    for u in updates:
        total = np.mod(total + _encode(u), MOD)
    return _decode(total)


# ---------------------------------------------------------------- robust aggregation
def agg_mean(U, w=None):
    U = np.asarray(U)
    if w is None:
        return U.mean(0)
    w = np.asarray(w, float); return (U * w[:, None]).sum(0) / w.sum()


def agg_median(U, w=None):
    return np.median(np.asarray(U), axis=0)


def agg_trimmed(U, w=None, beta=0.2):
    U = np.sort(np.asarray(U), axis=0)
    k = int(beta * len(U))
    return U[k:len(U) - k].mean(0)


def agg_normbound(U, w=None, C=1.0):
    return np.mean([clip(u, C)[0] for u in U], axis=0)


# ---------------------------------------------------------------- compression
def stochastic_quantise(v, bits=8, rng=None):
    lv = 2 ** bits - 1
    lo, hi = v.min(), v.max()
    if hi - lo < 1e-12:
        return v.copy()
    s = (v - lo) / (hi - lo) * lv
    f = np.floor(s)
    q = f + (rng.random(v.shape) < (s - f))
    return lo + q / lv * (hi - lo)

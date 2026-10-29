"""Tiny numpy MLP (48-64-8) with manual back-propagation, flat-parameter helpers."""
import numpy as np


class MLP:
    def __init__(self, d_in=48, d_h=64, d_out=8, seed=0):
        rng = np.random.default_rng(seed)
        self.shapes = [(d_in, d_h), (d_h,), (d_h, d_out), (d_out,)]
        self.w = [rng.normal(0, np.sqrt(2 / d_in), (d_in, d_h)).astype(np.float32),
                  np.zeros(d_h, np.float32),
                  rng.normal(0, np.sqrt(1 / d_h), (d_h, d_out)).astype(np.float32),
                  np.zeros(d_out, np.float32)]

    @property
    def n_params(self):
        return sum(int(np.prod(s)) for s in self.shapes)

    def get(self):
        return np.concatenate([p.ravel() for p in self.w])

    def set(self, flat):
        out, i = [], 0
        for s in self.shapes:
            n = int(np.prod(s)); out.append(flat[i:i + n].reshape(s).astype(np.float32)); i += n
        self.w = out

    def forward(self, x):
        h = np.maximum(0, x @ self.w[0] + self.w[1])
        z = h @ self.w[2] + self.w[3]
        return h, z

    def predict_proba(self, x):
        _, z = self.forward(x)
        z = z - z.max(1, keepdims=True)
        e = np.exp(z)
        return e / e.sum(1, keepdims=True)

    def loss_per_sample(self, x, y):
        p = self.predict_proba(x)
        return -np.log(p[np.arange(len(y)), y] + 1e-12)

    def accuracy(self, x, y):
        return float((self.predict_proba(x).argmax(1) == y).mean())

    def grad(self, x, y):
        h, z = self.forward(x)
        z = z - z.max(1, keepdims=True)
        p = np.exp(z); p /= p.sum(1, keepdims=True)
        p[np.arange(len(y)), y] -= 1
        p /= len(y)
        gW2 = h.T @ p; gb2 = p.sum(0)
        dh = (p @ self.w[2].T) * (h > 0)
        gW1 = x.T @ dh; gb1 = dh.sum(0)
        return np.concatenate([gW1.ravel(), gb1, gW2.ravel(), gb2])


def local_sgd(model, w0, x, y, epochs=2, bs=32, lr=0.1, rng=None, prox_mu=0.0):
    """Run local SGD from w0; returns new flat weights. Optional FedProx proximal term."""
    w = w0.copy()
    n = len(y)
    for _ in range(epochs):
        idx = rng.permutation(n)
        for s in range(0, n, bs):
            b = idx[s:s + bs]
            model.set(w)
            g = model.grad(x[b], y[b])
            if prox_mu > 0:
                g = g + prox_mu * (w - w0)
            w = w - lr * g
    return w

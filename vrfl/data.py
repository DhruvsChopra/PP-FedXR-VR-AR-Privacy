"""Synthetic VR/AR telemetry generator (VR-MotionPriv-Synth).

Each sample is a 2-second window of head-mounted display (HMD), hand-controller and
eye-tracking telemetry summarised into 48 features (8 sensor groups x 6 statistics).
The generator deliberately embeds two kinds of signal:
  * task signal   - which of 8 interaction activities the user is performing
  * identity signal - stable, user-specific body and behaviour traits (height, arm
    span, handedness, gaze habits) that make telemetry a behavioural biometric.
This mirrors what is reported for real headsets (users re-identifiable from motion),
while allowing the data to be released without any human-subject risk.
"""
import numpy as np

FEATURE_GROUPS = ["Head position", "Head rotation", "Left-hand position",
                  "Left-hand rotation", "Right-hand position", "Right-hand rotation",
                  "Eye gaze", "Kinematics (vel/acc)"]
STATS = ["mean_x", "mean_y", "mean_z", "std_x", "std_y", "std_z"]
ACTIVITIES = ["Idle", "Look-around", "Teleport", "Grab", "Throw", "Point-select",
              "Virtual typing", "Draw/Sketch"]
N_FEAT, N_CLASS = 48, 8
PROTO_S, STYLE_S, NOISE_S = 0.70, 0.55, 1.0

# how strongly each sensor group carries task vs identity information
TASK_W = np.array([0.4, 0.9, 0.9, 0.7, 1.3, 1.0, 1.1, 1.2])
IDEN_W = np.array([1.6, 0.6, 1.0, 0.5, 1.0, 0.5, 0.9, 0.4])


def make_dataset(n_users=1000, mean_samples=60, alpha=0.4, seed=7):
    rng = np.random.default_rng(seed)
    tw = np.repeat(TASK_W, 6)
    iw = np.repeat(IDEN_W, 6)
    # two sub-prototypes per activity -> non-linear class boundaries
    protos = rng.normal(0, PROTO_S, size=(N_CLASS, 2, N_FEAT)) * tw
    user_style = rng.normal(0, STYLE_S, size=(n_users, N_FEAT)) * iw
    mix = rng.normal(0, 1, size=(N_FEAT, N_FEAT)) / np.sqrt(N_FEAT)
    X, Y, U = [], [], []
    for u in range(n_users):
        n = int(np.clip(rng.lognormal(np.log(mean_samples), 0.45), 20, 4 * mean_samples))
        p = rng.dirichlet(alpha * np.ones(N_CLASS))           # non-IID label skew
        y = rng.choice(N_CLASS, size=n, p=p)
        sub = rng.integers(0, 2, size=n)
        x = protos[y, sub] + user_style[u] + rng.normal(0, NOISE_S, size=(n, N_FEAT))
        x = x + 0.35 * np.tanh(x @ mix)                         # mild sensor non-linearity
        X.append(x); Y.append(y); U.append(np.full(n, u))
    X = np.concatenate(X).astype(np.float32)
    Y = np.concatenate(Y).astype(np.int64)
    U = np.concatenate(U).astype(np.int64)
    mu, sd = X.mean(0), X.std(0) + 1e-6
    X = (X - mu) / sd
    return X, Y, U


def split_per_user(X, Y, U, test_frac=0.2, seed=11):
    rng = np.random.default_rng(seed)
    clients = {}
    for u in np.unique(U):
        idx = np.where(U == u)[0]
        rng.shuffle(idx)
        k = max(1, int(len(idx) * test_frac))
        clients[int(u)] = dict(xtr=X[idx[k:]], ytr=Y[idx[k:]], xte=X[idx[:k]], yte=Y[idx[:k]])
    return clients

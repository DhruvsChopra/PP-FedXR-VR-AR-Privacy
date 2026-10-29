# PP-FedXR — Federated Privacy-Preserving Learning for VR/AR

Source code for the BCSE318L Data Privacy case study
*"Federated Privacy-Preserving Learning in Virtual and Augmented Reality Ecosystems"*
by Dhruv Chopra (23BCE2266), VIT Vellore.

Every number, table entry and chart in the report is produced by this code.

## Contents

| Path | Purpose |
|---|---|
| `vrfl/data.py` | VR-MotionPriv-Synth generator: 1,000 users, 48 features (8 sensor groups), 8 activities, user-specific behavioural signatures, Dirichlet label skew |
| `vrfl/model.py` | NumPy MLP (48-64-8) with manual back-propagation; local SGD (optional FedProx term) |
| `vrfl/privacy.py` | Update clipping, RDP accountant for the subsampled Gaussian mechanism, pairwise-masking secure aggregation (mod 2^32), median / trimmed-mean / norm-bound aggregation, stochastic quantisation |
| `vrfl/fl.py` | Federated loop (FedAvg, FedProx, DP-FedAvg, PP-FedXR with distributed noise + SecAgg + server momentum), poisoning clients, edge personalisation, centralised and local-only baselines |
| `vrfl/attacks.py` | Re-identification attack (window and session level), loss-threshold membership inference |
| `run_all.py` | Runs experiments E1–E10 and writes `results/results.json` and `results/run_log.txt` |
| `figs/diagrams.py` | Architecture diagrams (Figures 1–21, 26–29, 31–34) at 600 DPI |
| `figs/charts.py` | Result charts (Figures 18, 22–25, 30, A1–A3) from `results/results.json` |

## Run

```bash
pip install -r requirements.txt
python run_all.py            # ~4 min on a 2-core CPU; writes results/
cd figs
python diagrams.py           # writes PNGs to ../diagrams (override with FIG_OUT)
python charts.py
```

All seeds are fixed (data 7, split 11, training 0), so results are reproducible.

## Key results (from `results/results.json`)

| Configuration | Test accuracy | ε (δ = 1e-4) | Accuracy, 20 % attackers |
|---|---|---|---|
| Centralised (no privacy) | 95.79 % | – | – |
| Local-only | 72.72 % (per user) | – | – |
| FedAvg | 92.33 % | – | 12.75 % |
| DP-FedAvg (z = 1.0) | 91.20 % | 10.95 | – |
| **PP-FedXR** | **91.94 %** | **10.95** | **86.35 %** |

Re-identification from centralised telemetry: 29.2 % per 2-s window, 85.2 % per session (chance 0.1 %).
Edge inference p95: 0.033 ms. Secure aggregation: exact sums, masked-vector correlation < 0.02.

## Notes and limitations

* The benchmark is synthetic by design (no human-subject data); see Section XII of the report.
* The secure-aggregation prototype is the honest-but-curious, no-dropout variant.
* Timing is measured on one CPU thread; network delays for cloud offload are modelled.

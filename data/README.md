# Datasets

* `vr_motionpriv_synth.npz` — VR-MotionPriv-Synth benchmark (X: 65,920 x 48 float32 features, Y: activity labels 0-7, U: user ids 0-999). Regenerate exactly with `vrfl.data.make_dataset(seed=7)`.
  Activities: Idle, Look-around, Teleport, Grab, Throw, Point-select, Virtual typing, Draw/Sketch.
  Feature order: 8 sensor groups (head position, head rotation, left-hand position, left-hand rotation, right-hand position, right-hand rotation, eye gaze, kinematics) x (mean_x, mean_y, mean_z, std_x, std_y, std_z).
* `results.json` — every number reported in the manuscript.
* `run_log.txt` — console log of the full experiment run.
* `global_model_proposed.npy` — trained PP-FedXR global model (3,656 parameters, flat vector).

The data are synthetic; no human participants were involved.

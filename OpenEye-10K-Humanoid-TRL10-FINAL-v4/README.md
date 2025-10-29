
# OpenEye-10K Humanoid TRL-10 — FINAL v4
**Complete humanoid-eye stack**, now with:
- ✅ ONNX model hooks (YOLO / MiDaS / FER) — optional, plug-in ready
- ✅ ROS2 hardware bridge (graceful fallback to SIM)
- ✅ Dashboard “Mode” indicator (SIM/LIVE) + Alerts + Audit + Mission
- ✅ AI triage everywhere (CI, Nightly/Watchdog, Orchestrator, manual)
- ✅ Self-heal, Semantic Watchdog, Feature Auditor, Policy Guard
- ✅ 30/90-day plan with daily Orchestrator

> Ships SIM-first. If hardware is connected (or `OPENEYE_MODE=live`), the stack switches to LIVE mode.

## Quickstart (SIM mode)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python server/main.py
# open http://localhost:8000/dashboard
python auditor/feature_auditor.py    # populate Feature Audit
```

## Live/Hardware Mode (optional)
```bash
export OPENEYE_MODE=live    # or plug hardware + run ROS bridge
python ros_bridge/ros_eye_bridge.py --mode live  # optional bridge process
python server/main.py
```

## ONNX Models (optional)
Uncomment `onnxruntime` & `opencv-python` in requirements, then:
```bash
pip install -r requirements.txt
python vision/test_onnx_inference.py  # runs tiny smoke tests
```

## AI Triage (optional but recommended)
```bash
export OPENAI_API_KEY=sk-...   # locally or GitHub Secrets
```
Failures trigger triage → patch → re-run, across CI, Nightly, Orchestrator, and manual runs.

## Optional: Vercel deploy
Add `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `VERCEL_TOKEN` to repo secrets, then run the workflow “Optional Vercel Deploy”.

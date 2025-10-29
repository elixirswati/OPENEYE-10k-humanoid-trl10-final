
import threading, time, random, os, json
from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="OpenEye-10K Humanoid TRL-10")

def detect_mode():
  # Live if env says so or if ros bridge heartbeat file exists
  if os.environ.get("OPENEYE_MODE","").lower() == "live":
    return "LIVE"
  hb = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts", "ros_heartbeat"))
  return "LIVE" if os.path.exists(hb) else "SIM"

STATE = {
  "mode": detect_mode(),
  "fps": 60.0, "latency_ms": 25.0, "depth_mean": 1.5,
  "roll_deg": 0.0, "pitch_deg": 0.0, "yaw_deg": 0.0,
  "left_servo": {"pan_deg": 0.0, "tilt_deg": 0.0},
  "right_servo": {"pan_deg": 0.0, "tilt_deg": 0.0},
  "emotion": "neutral",
  "targets": [],
  "ts": time.time()
}

def _sim_loop():
  while True:
    STATE["mode"] = detect_mode()
    # Vision/perception (simulated values)
    STATE["fps"] = 60.0 + random.uniform(-3,3)
    STATE["latency_ms"] = 25.0 + random.uniform(-4,4)
    STATE["depth_mean"] = 1.5 + 0.3*random.uniform(-1,1)
    # IMU-like
    STATE["yaw_deg"] = 5.0*random.uniform(-1,1)
    STATE["pitch_deg"] = 3.0*random.uniform(-1,1)
    STATE["roll_deg"] = 2.0*random.uniform(-1,1)
    # Gaze control (basic vergence-style wobble)
    STATE["left_servo"]["pan_deg"] = 5.0*random.uniform(-1,1)
    STATE["right_servo"]["pan_deg"] = -STATE["left_servo"]["pan_deg"]
    STATE["left_servo"]["tilt_deg"] = 2.0*random.uniform(-1,1)
    STATE["right_servo"]["tilt_deg"] = STATE["left_servo"]["tilt_deg"]
    # Emotion stub
    STATE["emotion"] = random.choice(["neutral","happy","focus","blink"])
    STATE["ts"] = time.time()
    time.sleep(0.05)

threading.Thread(target=_sim_loop, daemon=True).start()

# Static mount
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/healthz")
def healthz(): return {"status":"ok","time": time.time(),"mode": STATE["mode"]}

@app.get("/metrics")
def metrics(): return JSONResponse(STATE)

@app.get("/humanoid/status")
def humanoid_status():
  return {
    "mode": STATE["mode"],
    "left_eye": STATE["left_servo"],
    "right_eye": STATE["right_servo"],
    "imu": {"roll": STATE["roll_deg"], "pitch": STATE["pitch_deg"], "yaw": STATE["yaw_deg"]},
    "emotion": STATE["emotion"]
  }

@app.get("/mission/status")
def mission_status():
  return {"phase": "Phase 1 (0-30 days)", "progress": "orchestrator ready", "ts": time.time()}

@app.get("/feature/report")
def feature_report():
  path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "report", "feature_report.json"))
  if os.path.exists(path):
    with open(path, "r") as f:
      try: data = json.load(f)
      except Exception: data = {"error": "invalid JSON"}
    return JSONResponse(data)
  return JSONResponse({"summary": {}, "active": [], "missing": [], "note": "Run auditor/feature_auditor.py to generate report."})

@app.get("/alerts")
def alerts():
  path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts", "watchdog.json"))
  if os.path.exists(path):
    with open(path, "r") as f:
      try: data = json.load(f)
      except Exception: data = {"error": "invalid JSON"}
    return JSONResponse(data)
  return JSONResponse({"alerts": [], "note": "No alerts yet."})

@app.get("/dashboard")
def dashboard():
  index_path = os.path.join(static_dir, "dashboard.html")
  if os.path.exists(index_path):
    return FileResponse(index_path, media_type="text/html")
  return HTMLResponse("<h1>OpenEye Dashboard</h1><p>Add server/static/dashboard.html</p>")

if __name__ == "__main__":
  import uvicorn; uvicorn.run(app, host="0.0.0.0", port=8000)

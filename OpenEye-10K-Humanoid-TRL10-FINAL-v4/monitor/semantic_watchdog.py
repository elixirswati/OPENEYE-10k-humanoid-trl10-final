
#!/usr/bin/env python3
import time, requests, psutil, json, subprocess, os, statistics
TH = {"fps_min":50,"latency_max":40,"cpu_max":90,"mem_max":85,"drift_z":3.0}
hist=[]
def z(key):
  vals=[s[key] for s in hist if key in s]
  if len(vals)<5: return 0.0
  m=statistics.mean(vals); sd=statistics.pstdev(vals) or 1.0
  return abs((vals[-1]-m)/sd)
def fetch():
  try: return requests.get("http://localhost:8000/metrics",timeout=2).json()
  except: return {}
def loop():
  while True:
    m=fetch(); m["cpu"]=psutil.cpu_percent(); m["mem"]=psutil.virtual_memory().percent
    hist.append(m); hist[:]=hist[-120:]
    alerts=[]
    if m.get("fps",0)<TH["fps_min"]: alerts.append("Low FPS")
    if m.get("latency_ms",0)>TH["latency_max"]: alerts.append("High latency")
    if m.get("cpu",0)>TH["cpu_max"]: alerts.append("CPU")
    if m.get("mem",0)>TH["mem_max"]: alerts.append("MEM")
    if z("fps")>TH["drift_z"]: alerts.append("FPS drift")
    if alerts:
      os.makedirs("artifacts",exist_ok=True)
      with open("artifacts/watchdog.json","w") as f: json.dump({"alerts":alerts,"ts":time.time(),"last":m},f,indent=2)
      subprocess.call("python tools/self_heal.py --cmd 'pytest -q' || true", shell=True)
    time.sleep(5)
if __name__=="__main__": loop()

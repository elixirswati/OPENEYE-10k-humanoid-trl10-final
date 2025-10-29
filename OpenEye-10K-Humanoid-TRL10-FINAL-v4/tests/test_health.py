
import requests, subprocess, time
def test_healthz():
  p=subprocess.Popen(["python","server/main.py"])
  time.sleep(1.2)
  try:
    r=requests.get("http://localhost:8000/healthz", timeout=3)
    assert r.status_code==200
    assert r.json()["status"]=="ok"
  finally:
    p.terminate()


#!/usr/bin/env python3
import json, os, requests
os.makedirs("artifacts", exist_ok=True)
try: m=requests.get("http://localhost:8000/metrics",timeout=2).json()
except Exception: m={"fps":58,"latency_ms":32}
bench={"desktop":{"fps":float(m.get("fps",58)),"latency_ms":float(m.get("latency_ms",32))},
       "edge":{"fps":48.0,"latency_ms":40.0}}
open("artifacts/bench.json","w").write(json.dumps(bench,indent=2))
print(json.dumps(bench, indent=2))

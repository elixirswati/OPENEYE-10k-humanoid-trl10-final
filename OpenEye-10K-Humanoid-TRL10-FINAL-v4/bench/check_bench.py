
#!/usr/bin/env python3
import json, sys, os
gold=json.load(open("bench/golden.json"))
if not os.path.exists("artifacts/bench.json"): sys.exit(2)
cur=json.load(open("artifacts/bench.json"))
def ok(p): return cur[p]["fps"]>=gold[p]["fps_min"] and cur[p]["latency_ms"]<=gold[p]["latency_ms_max"]
sys.exit(0 if (ok("desktop") and ok("edge")) else 2)

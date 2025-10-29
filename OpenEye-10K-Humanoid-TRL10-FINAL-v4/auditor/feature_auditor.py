
#!/usr/bin/env python3
import os, yaml, requests, json
rep={"summary":{}, "missing":[], "active":[]}
spec=yaml.safe_load(open("auditor/stack_features.yaml"))
def f(path): return os.path.exists(path)
def a(endpoint):
  try: return requests.get("http://localhost:8000"+endpoint, timeout=2).status_code==200
  except: return False
for ft in spec["features"]:
  ok = f(ft["check"]) if ft["type"]=="file" else a(ft["check"])
  rep["summary"][ft["name"]]="✅ Active" if ok else "❌ Missing"
  (rep["active"] if ok else rep["missing"]).append(ft["name"])
os.makedirs("report",exist_ok=True)
open("report/feature_report.json","w").write(json.dumps(rep,indent=2))
print(json.dumps(rep,indent=2))

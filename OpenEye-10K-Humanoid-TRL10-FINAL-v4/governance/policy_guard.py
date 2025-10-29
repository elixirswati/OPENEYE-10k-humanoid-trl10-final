
#!/usr/bin/env python3
import os, re, sys, yaml, subprocess
POL=yaml.safe_load(open("governance/policy.yaml"))
def fail(m): print("❌ POLICY:",m); sys.exit(2)
def grep(pat):
  out=subprocess.check_output(["git","ls-files"]).decode().splitlines()
  rx=re.compile(pat)
  for f in out:
    try:
      t=open(f,"r",errors="ignore").read()
      if rx.search(t): return False,f
    except: pass
  return True,None
def lic(allowed):
  if not os.path.exists("LICENSE"): return False,"LICENSE missing"
  txt=open("LICENSE","r",errors="ignore").read()
  for a in allowed:
    if a.lower() in txt.lower(): return True,None
  return False,"LICENSE not matched"
for r in POL["rules"]:
  if r["type"]=="grep": ok,loc=grep(r["pattern"])
  elif r["type"]=="license": ok,loc=lic(r["allowed"])
  else: ok,loc=True,None
  if not ok:
    if r["action"]=="block": fail(f"{r['id']} at {loc}: {r['message']}")
    else: print(f"⚠️ POLICY REVIEW: {r['id']} at {loc}: {r['message']}")
print("✅ Policy check passed.")

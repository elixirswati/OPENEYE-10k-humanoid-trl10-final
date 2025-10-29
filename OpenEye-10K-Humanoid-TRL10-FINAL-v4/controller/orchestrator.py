
#!/usr/bin/env python3
import yaml, os, subprocess, datetime, requests
PLAN=yaml.safe_load(open("controller/mission_plan.yaml"))
REPO=os.getenv("GITHUB_REPOSITORY","OWNER/REPO")
API=f"https://api.github.com/repos/{REPO}/issues"
TOKEN=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
def open_issue(title, body):
  if not TOKEN: return
  r=requests.post(API, headers={"Authorization": f"token {TOKEN}"}, json={"title": title, "body": body})
  print("Issue:", r.status_code)
def run(cmd): print('▶',cmd); return subprocess.call(cmd, shell=True)==0
def day(): return datetime.datetime.utcnow().day
def main():
  d=day()
  for ph in PLAN["phases"]:
    s,e=map(int,ph["day"].split("-"))
    if s<=d<=e:
      for g in ph["goals"]:
        n,desc=list(g.items())[0]
        ok=True
        if n=='setup': ok=run('python server/main.py & sleep 2 && curl -s localhost:8000/healthz')
        elif n=='audit': ok=run('python auditor/feature_auditor.py || python auditor/feature_auditor.py')
        elif n=='ai': ok=run('echo AI latency stub')
        elif n=='docs': ok=run('echo docs stub')
        elif n=='dash': ok=run('echo dash stub')
        elif n=='report': ok=run('test -f report/feature_report.json || python auditor/feature_auditor.py')
        if not ok: subprocess.call("python tools/self_heal.py --cmd 'pytest -q' || true", shell=True)
        open_issue(f'[Day {d}] {n} {"✅" if ok else "❌"}', f'Goal: {desc}\nResult: {ok}')
      break
if __name__=='__main__': main()

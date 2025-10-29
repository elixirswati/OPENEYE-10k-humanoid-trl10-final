
#!/usr/bin/env python3
import os, sys, json, argparse, re
def read_log(path):
    try: return open(path,"r",encoding="utf-8",errors="ignore").read()[:200000]
    except: return ""
def simple_heuristic(log):
    rc={"summary":"heuristic triage","root_cause":"","diff":"","validation":["pytest -q"]}
    if "ModuleNotFoundError" in log:
        m=re.search(r"ModuleNotFoundError: No module named '([^']+)'",log); 
        rc["root_cause"]=f"Missing module: {m.group(1) if m else '?'}"
    elif "SyntaxError" in log: rc["root_cause"]="Syntax error"
    elif "AssertionError" in log: rc["root_cause"]="Test assertion failed"
    else: rc["root_cause"]="Unknown (fallback heuristic)"
    return rc
def with_openai(log, tree):
    try:
        from openai import OpenAI
        client=OpenAI()
        prompt=f"""You are a senior engineer. Given the repo tree and log, propose a minimal unified diff to fix the failure, or return empty diff.\nTREE:\n{tree}\nLOG:\n{log[:180000]}"""
        msg=client.chat.completions.create(model="gpt-4o-mini",messages=[{"role":"user","content":prompt}],temperature=0.2)
        text=msg.choices[0].message.content or ""
        import re as _r
        m=_r.search(r"```diff\n(.*?)\n```",text,_r.DOTALL); diff=m.group(1) if m else ""
        return {"summary":"ai-triage (openai)","root_cause":"See raw","diff":diff.strip(),"validation":["pytest -q"],"raw":text[:4000]}
    except Exception as e:
        return {"summary":"ai-triage error","root_cause":str(e),"diff":"","validation":["pytest -q"]}
def main():
    import subprocess
    ap=argparse.ArgumentParser(); ap.add_argument("--log",default="artifacts/ci.log"); ap.add_argument("--out",default="artifacts/triage.json"); args=ap.parse_args()
    log=read_log(args.log); tree=""
    try:
        out=subprocess.check_output(["git","ls-files"], text=True); tree="\n".join(out.strip().splitlines()[:200])
    except Exception: pass
    triage = with_openai(log, tree) if os.getenv("OPENAI_API_KEY") else simple_heuristic(log)
    os.makedirs(os.path.dirname(args.out), exist_ok=True); open(args.out,"w").write(json.dumps(triage,indent=2)); print(json.dumps(triage,indent=2))
if __name__=="__main__": main()

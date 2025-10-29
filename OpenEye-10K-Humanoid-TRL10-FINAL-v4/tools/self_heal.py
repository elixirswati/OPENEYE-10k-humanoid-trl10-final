
#!/usr/bin/env python3
import subprocess, sys, pathlib, os
ART=pathlib.Path("artifacts"); ART.mkdir(exist_ok=True)
def run(cmd):
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    with open(ART/"ci.log","w") as lf:
        for line in p.stdout: print(line,end=""); lf.write(line)
    return p.wait()
def self_heal(cmd, attempts=2):
    for i in range(attempts):
        rc=run(cmd)
        if rc==0: print("✅ Command passed."); return 0
        print(f"❌ Failure (attempt {i+1}/{attempts}). Triaging ...")
        subprocess.call("python tools/ai_triage.py --log artifacts/ci.log --out artifacts/triage.json", shell=True)
        subprocess.call("python tools/ai_apply_patch.py --json artifacts/triage.json", shell=True)
        print("Re-running after patch...")
    return run(cmd)
def main():
    cmd="pytest -q"
    if len(sys.argv)>2 and sys.argv[1]=="--cmd": cmd=" ".join(sys.argv[2:])
    sys.exit(self_heal(cmd,attempts=2))
if __name__=="__main__": main()

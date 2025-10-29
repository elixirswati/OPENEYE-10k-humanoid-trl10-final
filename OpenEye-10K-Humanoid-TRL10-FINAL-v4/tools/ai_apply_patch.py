
#!/usr/bin/env python3
import os, sys, json, subprocess, tempfile
def sh(cmd, check=False):
    print("+",cmd); code=subprocess.call(cmd,shell=True)
    if check and code!=0: raise SystemExit(code); return code
    return code
def main():
    jpath="artifacts/triage.json"
    if len(sys.argv)>2 and sys.argv[1]=="--json": jpath=sys.argv[2]
    triage=json.load(open(jpath)); diff=(triage.get("diff") or "").strip()
    if not diff: print("No diff proposed; nothing to apply."); return
    branch="ai-fix-"+str(os.getpid()); sh("git config user.email 'bot@example.com'"); sh("git config user.name 'openeye-bot'"); sh(f"git checkout -b {branch}",check=True)
    with tempfile.NamedTemporaryFile("w",delete=False,suffix=".patch") as f: f.write(diff); patch_path=f.name
    if sh(f"git apply --whitespace=fix {patch_path}")!=0: print("Patch did not apply cleanly."); return
    sh("git add -A",check=True); sh("git commit -m 'AI self-heal: apply patch' ",check=True)
    sh("pytest -q || true")
    token=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN"); repo=os.getenv("GITHUB_REPOSITORY")
    if token and repo:
        sh("git push origin HEAD || true")
        if subprocess.call("which gh >/dev/null 2>&1", shell=True)==0:
            sh("gh pr create --fill --title 'AI Self-Heal Patch' --body 'Automated patch from ai_triage' || true")
        else: print("gh CLI not found; branch pushed. Open PR manually.")
    else: print("No GH token/repo; patch committed locally only.")
if __name__=="__main__": main()

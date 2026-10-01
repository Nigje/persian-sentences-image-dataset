"""Back up and remove Dataset ZIPs from branch/tag history in GitHub Actions."""
import argparse, base64, json, os, subprocess
from pathlib import Path

def run(args, cwd=None, capture=False):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None)

def git(args, cwd, capture=False):
    header = "AUTHORIZATION: basic " + base64.b64encode(
        ("x-access-token:" + os.environ["GH_TOKEN"]).encode()).decode()
    return run(["git", "-c", "http.extraHeader=" + header, *args], cwd, capture)

p = argparse.ArgumentParser()
p.add_argument("stage", choices=["backup", "rewrite"])
p.add_argument("--work", type=Path, required=True)
a = p.parse_args()
repo = os.environ["GH_REPO"]
url = "https://github.com/" + repo + ".git"
mirror = a.work / "mirror.git"
audit = json.loads(Path("data/audit.json").read_text())
release = json.loads(run(["gh", "api", "repos/" + repo + "/releases/tags/v1.0.0"], capture=True).stdout)
if release["draft"]:
    raise SystemExit("Release must be published before cleanup")
assets = {x["name"]: x for x in release["assets"]}
for expected in audit["archives"]:
    asset = assets.get(expected["release_asset"])
    if not asset or asset["state"] != "uploaded" or asset["size"] != expected["bytes"] or asset.get("digest") != "sha256:" + expected["sha256"]:
        raise SystemExit("Unverified release asset: " + expected["filename"])

if a.stage == "backup":
    a.work.mkdir(parents=True, exist_ok=True)
    git(["clone", "--mirror", url, str(mirror)], None)
    refs = {}
    for line in run(["git", "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads", "refs/tags"], mirror, True).stdout.splitlines():
        ref, sha = line.split()
        refs[ref] = sha
    if "refs/heads/main" not in refs:
        raise SystemExit("Missing main branch")
    (a.work / "refs-before.json").write_text(json.dumps(refs, indent=2))
    run(["git", "bundle", "create", str(a.work / "before-cleanup.bundle"), "--all"], mirror)
    print("Full backup created before rewriting.")
else:
    refs = json.loads((a.work / "refs-before.json").read_text())
    run(["git", "filter-repo", "--path-glob", "Dataset/*.zip", "--invert-paths", "--force"], mirror)
    objects = run(["git", "rev-list", "--objects", "--all"], mirror, True).stdout
    if any(" Dataset/" in line and line.endswith(".zip") for line in objects.splitlines()):
        raise SystemExit("ZIP paths remain reachable after filtering")
    run(["git", "remote", "add", "origin", url], mirror)
    leases = ["--force-with-lease=" + ref + ":" + sha for ref, sha in refs.items()]
    refspecs = [ref + ":" + ref for ref in refs]
    git(["push", "--atomic", *leases, "origin", *refspecs], mirror)
    after = run(["git", "for-each-ref", "--format=%(refname) %(objectname)", "refs/heads", "refs/tags"], mirror, True).stdout
    (a.work / "refs-after.txt").write_text(after)
    print("Branch and tag history rewritten; release assets unchanged.")

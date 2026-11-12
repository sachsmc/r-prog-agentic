# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Run the scripted skill checks in eval/skill_checks.yml.

Each check sends one student message to Claude Code in headless mode
(`claude -p`) from the repo root and tests the reply against its rubric.

Run:  uv run eval/run_skill_checks.py [--only ID ...] [--keep]
Set CLAUDE_CMD to change the command, for example
  CLAUDE_CMD="claude -p --permission-mode acceptEdits"
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CMD = "claude -p --permission-mode acceptEdits"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", nargs="+", metavar="ID")
    ap.add_argument("--keep", action="store_true", help="save each reply under eval/replies/")
    args = ap.parse_args()

    cmd = shlex.split(os.environ.get("CLAUDE_CMD", DEFAULT_CMD))
    if not shutil.which(cmd[0]):
        print(f"'{cmd[0]}' was not found, so the skill checks cannot run here.")
        return 2
    checks = yaml.safe_load((ROOT / "eval" / "skill_checks.yml").read_text(encoding="utf-8"))
    if args.only:
        checks = [c for c in checks if c["id"] in args.only]
    have_refs = (ROOT / "refs").is_dir()
    progress = ROOT / "progress.md"
    saved = progress.read_text(encoding="utf-8") if progress.exists() else None

    failed = 0
    for c in checks:
        if c.get("needs_refs") and not have_refs:
            print(f"skip {c['id']}: refs/ is not built")
            continue
        r = subprocess.run([*cmd, c["message"]], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=900)
        reply = r.stdout
        problems = []
        if r.returncode != 0:
            problems.append(f"the command exited with code {r.returncode}: {r.stderr.strip()[:300]}")
        for pat in c.get("must", []):
            if not re.search(pat, reply):
                problems.append(f"missing: {pat}")
        for pat in c.get("must_not", []):
            if re.search(pat, reply):
                problems.append(f"should not be there: {pat}")
        if c.get("cite_check"):
            with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
                f.write(reply)
            cc = subprocess.run([sys.executable, str(ROOT / "bin" / "cite-check"), "--file", f.name],
                                capture_output=True, text=True, encoding="utf-8")
            os.unlink(f.name)
            if cc.returncode != 0:
                problems.append("cite-check failed:\n" + cc.stdout)
        if args.keep:
            out = ROOT / "eval" / "replies"
            out.mkdir(exist_ok=True)
            (out / f"{c['id']}.md").write_text(reply, encoding="utf-8")
        failed += bool(problems)
        print(f"{'FAIL' if problems else 'ok  '} {c['id']} ({c['skill']})")
        for p in problems:
            print(f"       {p}")
        # each check starts from the same state
        if saved is None:
            progress.unlink(missing_ok=True)
        else:
            progress.write_text(saved, encoding="utf-8")
    print(f"{len(checks) - failed} of {len(checks)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

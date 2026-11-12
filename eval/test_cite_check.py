"""Unit tests for bin/cite-check. They use course/ only, so they run without refs/."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "bin" / "cite-check"
LECTURE = "course/lectures/06-functions"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL), *args], capture_output=True, text=True,
                          encoding="utf-8", cwd=ROOT)


def find_line(_needle: str = "") -> tuple[int, str]:
    """A line of plain prose from the lecture, with its line number."""
    lines = (ROOT / f"{LECTURE}.md").read_text(encoding="utf-8").split(chr(10))
    fence = False
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if (not fence and len(line) > 60 and line[0].isalpha() and not line.startswith("    ")
                and not any(c in line for c in '"`<>|[]')):
            return n, line
    raise AssertionError("no prose line found in the lecture")


def test_correct_quote_passes():
    n, line = find_line("lazily")
    r = run(f"{LECTURE}:L{n}", line.strip())
    assert r.returncode == 0, r.stdout


def test_whitespace_and_emphasis_are_ignored():
    n, line = find_line("lazily")
    quote = "  ".join(line.replace("*", "").replace("_", "").split())
    r = run(f"{LECTURE}:L{n}-L{n}", quote)
    assert r.returncode == 0, r.stdout


def test_wrong_line_range_fails_and_shows_the_lines():
    n, line = find_line("lazily")
    r = run(f"{LECTURE}:L{n + 3}-L{n + 4}", line.strip())
    assert r.returncode == 1
    assert f"L{n + 3}:" in r.stdout


def test_paraphrase_fails():
    n, _ = find_line("lazily")
    r = run(f"{LECTURE}:L{n}", "R only works out the value of an argument when it is needed")
    assert r.returncode == 1


def test_missing_file_fails():
    r = run("course/lectures/99-nothing:L1-L2", "anything")
    assert r.returncode == 1
    assert "no such file" in r.stdout


def test_lines_outside_file_fail():
    r = run(f"{LECTURE}:L99990-L99999", "anything")
    assert r.returncode == 1
    assert "outside the file" in r.stdout


def test_file_mode(tmp_path):
    n, line = find_line("lazily")
    good = line.strip().replace('"', "")
    draft = tmp_path / "answer.md"
    draft.write_text(
        f'The lecture says "{good}" ({LECTURE}:L{n}).\n\n'
        f"> {good}\n\n({LECTURE}:L{n})\n\n"
        f'It also says "arguments are evaluated at once" ({LECTURE}:L{n}).\n\n'
        f"See also {LECTURE}:L1-L3.\n", encoding="utf-8")
    r = run("--file", str(draft))
    assert r.returncode == 1
    out = r.stdout
    assert out.count("ok  ") == 3 and out.count("FAIL") == 1
    assert "3 of 4 citations pass" in out

#!/usr/bin/env python3
"""Repository checks for deslop. Standard library only.

Run from the repository root:
    python3 tools/validate.py

Checks:
1. SKILL.md frontmatter (name matches the skill folder, description length,
   no angle brackets, valid YAML when PyYAML is installed).
0. The skill folder carries its own LICENSE.
2. Pattern codes: every code used in the language files exists in SKILL.md.
3. Examples: an "After" line adds no word missing from its "Before" line,
   except function words and words declared in a following
   <!-- new-words: ... --> comment.
4. No em or en dashes outside example lines, code and lines about dashes.
5. No AI attribution lines.
6. scripts/check.py finds the expected codes in tools/fixtures and stays
   quiet on the fixtures with correct usage.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "deslop"
SKILL = SKILL_DIR / "SKILL.md"
LANG_FILES = [SKILL_DIR / "references" / "es.md", SKILL_DIR / "references" / "en.md"]
ALL_DOCS = [SKILL, *LANG_FILES]

FUNCTION_WORDS = {
    "es": {"y", "e", "o", "u", "de", "del", "el", "la", "los", "las", "un", "una", "en", "a", "al",
           "que", "se", "es", "son", "tiene", "tienen", "incluye", "con", "por", "para"},
    "en": {"and", "or", "the", "a", "an", "of", "in", "to", "is", "are", "has", "have", "includes",
           "with", "for", "on", "at"},
}

EXPECTED = {
    "es.txt": {"R1/R2?", "R4", "R5", "N1", "N2", "N3", "N3/E8", "N4", "N5", "E8", "E10", "E21"},
    "en.txt": {"R1/R2?", "R4", "R5", "N2", "E8", "E10", "E21"},
}

# Texts with correct usage: these codes must not be reported (false-positive guard).
NOT_EXPECTED = {
    "es_ok.txt": {"N1", "N2", "N3", "N3/E8", "N4?", "E8", "E10", "R4"},
    "en_ok.txt": {"R5", "N2", "E8"},
}

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def check_frontmatter() -> set[str]:
    text = SKILL.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("SKILL.md must start with YAML frontmatter")
        return set()
    fm = m.group(1)
    try:
        import yaml  # optional: claude.ai's validator parses the frontmatter strictly
        yaml.safe_load(fm)
    except ImportError:
        pass
    except Exception as exc:  # noqa: BLE001
        fail(f"frontmatter is not valid YAML: {exc}")
    if not (SKILL_DIR / "LICENSE").is_file():
        fail("the skill folder needs its own LICENSE so the package carries the notice")
    name = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or name.group(1) != SKILL_DIR.name:
        fail(f"frontmatter name must match the skill folder: {SKILL_DIR.name}")
    if not desc:
        fail("frontmatter needs a one-line description")
    else:
        d = desc.group(1)
        if len(d) > 1024:
            fail(f"description is {len(d)} characters; keep it under 1024")
        if re.search(r"[<>]", d):
            fail("description must not contain angle brackets")
    return set(re.findall(r"^\*\*([RIE]\d+)\.", text, re.M)) | {f"N{i}" for i in range(1, 7)}


def check_codes(defined: set[str]) -> None:
    for f in LANG_FILES:
        text = f.read_text(encoding="utf-8")
        used = set(re.findall(r"^(?:### |\*\*)([RIEN]\d+)\.", text, re.M))
        for code in sorted(used - defined):
            fail(f"{f.name}: code {code} is not defined in SKILL.md")


def words(s: str) -> set[str]:
    s = s.split(":**", 1)[-1]
    s = re.sub(r"\(.*?\)", "", s)
    return set(re.findall(r"[\wáéíóúñü]+", s.lower()))


def check_examples() -> None:
    for f in LANG_FILES:
        lang = f.stem
        lines = f.read_text(encoding="utf-8").split("\n")
        for i, line in enumerate(lines):
            if not line.startswith("> **Before") or i + 1 >= len(lines):
                continue
            after = lines[i + 1]
            if not after.startswith("> **After"):
                continue
            declared: set[str] = set()
            if i + 2 < len(lines):
                m = re.match(r"<!--\s*new-words:\s*(.*?)\s*-->", lines[i + 2])
                if m:
                    declared = {w.strip().lower() for w in m.group(1).split(",") if w.strip()}
            new = words(after) - words(line) - FUNCTION_WORDS[lang] - declared
            if new:
                fail(f"{f.name}:{i + 2}: After adds words not in Before: {', '.join(sorted(new))}")


def check_dashes() -> None:
    allowed = re.compile(r"^>|`|raya|dash|Dialogue|Incisos|1990", re.I)
    for f in ALL_DOCS:
        for n, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            if ("—" in line or "–" in line) and not allowed.search(line):
                fail(f"{f.name}:{n}: dash outside an example or a rule about dashes")


def check_attribution() -> None:
    pattern = re.compile(r"co-authored-by|generated with|written by (?:ai|claude|chatgpt)", re.I)
    for f in ROOT.rglob("*"):
        if f.is_file() and ".git" not in f.parts and f.suffix in {".md", ".py", ".yml", ".txt", ""}:
            if f.resolve() == Path(__file__).resolve():
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if pattern.search(text):
                fail(f"{f.relative_to(ROOT)}: contains an AI attribution line")


def check_script() -> None:
    script = SKILL_DIR / "scripts" / "check.py"
    for name, expected in {**EXPECTED, **{k: set() for k in NOT_EXPECTED}}.items():
        fixture = ROOT / "tools" / "fixtures" / name
        lang = name.split(".")[0].split("_")[0]
        out = subprocess.run([sys.executable, "-I", str(script), str(fixture), "--lang", lang],
                             capture_output=True, text=True, check=False)
        if out.returncode != 0:
            fail(f"check.py failed on {name}: {out.stderr.strip()}")
            continue
        found = set(re.findall(r"· ([RIEN][\w/?]*) ·", out.stdout))
        for code in sorted(expected - found):
            fail(f"check.py did not report {code} on {name}")
        for code in sorted(NOT_EXPECTED.get(name, set()) & found):
            fail(f"check.py reported {code} on {name}, which has only correct usage")


def main() -> int:
    defined = check_frontmatter()
    check_codes(defined)
    check_examples()
    check_dashes()
    check_attribution()
    check_script()
    if errors:
        print("deslop: validation failed")
        for e in errors:
            print(f"- {e}")
        return 1
    print("deslop: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

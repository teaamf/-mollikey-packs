#!/usr/bin/env python3
"""Checks every pack in packs/ before it is published: the same file rules MolliKey applies when it opens a pack
(allowed entries, sizes and SHA-256 of every listed file, the manifest), plus this repository's own rules (an open
licence, one id per pack, listed in README.md). MolliKey still checks the configuration itself when a pack is
installed; this catches what would be refused, early, on the pull request.

Usage: python3 tools/check_packs.py [repository root]   (exit status 1 if anything is wrong)
"""
import hashlib, io, json, re, sys, zipfile
from pathlib import Path

MAX_BYTES = 96 * 1024 * 1024
MAX_ENTRIES = 512
ENTRY = re.compile(r"^(words|assets)/[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")
PACK_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{1,80}$")
FILE_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}\.mollikey$")
FORMAT, FORMAT_VERSION = "mollikey.pack", 1
# Open licences only (SPDX names). Add one here, in its own pull request, when a pack needs it.
OPEN_LICENCES = {"CC0-1.0", "CC-BY-4.0", "CC-BY-3.0", "CC-BY-SA-4.0", "CC-BY-SA-3.0", "MIT", "Apache-2.0",
                 "BSD-2-Clause", "BSD-3-Clause", "ODbL-1.0", "OFL-1.1", "Unlicense"}
ATTRIBUTION_NEEDED = ("CC-BY", "ODbL", "OFL", "MIT", "Apache", "BSD")


def check_pack(data: bytes):
    """Problems with one pack file, and its manifest when readable."""
    if len(data) > MAX_BYTES:
        return [f"larger than {MAX_BYTES // 1024 // 1024} MB"], None
    entries = {}
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            total = 0
            for info in z.infolist():
                if info.is_dir():
                    continue
                n = info.filename
                if n not in ("pack.json", "configuration.json") and not ENTRY.match(n):
                    return [f"unexpected file in the pack: {n}"], None
                if n in entries:
                    return [f"the pack lists {n} twice"], None
                if len(entries) >= MAX_ENTRIES:
                    return ["too many files"], None
                b = z.read(info)
                total += len(b)
                if total > MAX_BYTES:
                    return [f"expands to more than {MAX_BYTES // 1024 // 1024} MB"], None
                entries[n] = b
    except (zipfile.BadZipFile, OSError) as e:
        return [f"not a readable pack: {e}"], None
    if "pack.json" not in entries:
        return ["not a MolliKey pack (no pack.json)"], None
    try:
        m = json.loads(entries["pack.json"].decode("utf-8"))
        assert isinstance(m, dict)
    except Exception:
        return ["pack.json can't be read"], None
    if m.get("format") != FORMAT:
        return ["not a MolliKey pack (format)"], m
    problems = []
    if not isinstance(m.get("version"), int) or m["version"] > FORMAT_VERSION:
        problems.append(f"pack format {m.get('version')!r}: this MolliKey reads format {FORMAT_VERSION}")
    for field in ("id", "name", "licence"):
        if not isinstance(m.get(field), str) or not m[field].strip():
            problems.append(f"pack.json has no {field}")
    if not isinstance(m.get("packVersion"), int) or m["packVersion"] < 1:
        problems.append("packVersion must be a whole number, 1 or more")
    if isinstance(m.get("id"), str) and not PACK_ID.match(m["id"]):
        problems.append(f"id '{m['id']}' isn't valid (lower-case letters, digits, dots and dashes)")
    lic = m.get("licence")
    if isinstance(lic, str) and lic.strip() and lic not in OPEN_LICENCES:
        problems.append(f"licence '{lic}' isn't one this repository publishes ({', '.join(sorted(OPEN_LICENCES))})")
    if isinstance(lic, str) and lic.startswith(ATTRIBUTION_NEEDED) and not (m.get("attribution") or "").strip():
        problems.append(f"licence {lic} needs an attribution (who made the data)")
    if "configuration.json" in entries:
        try:
            json.loads(entries["configuration.json"].decode("utf-8"))
        except Exception:
            problems.append("configuration.json isn't readable JSON")
    listed = set()
    for kind in ("words", "assets"):
        for f in m.get(kind) or []:
            path = f.get("path") if isinstance(f, dict) else None
            listed.add(path)
            b = entries.get(path)
            if b is None or len(b) != f.get("size") or hashlib.sha256(b).hexdigest() != f.get("sha256"):
                problems.append(f"file {path} is missing or doesn't match its size and SHA-256")
    for n in entries:
        if n not in ("pack.json", "configuration.json") and n not in listed:
            problems.append(f"unlisted file in the pack: {n}")
    return problems, m


def main(root: Path) -> int:
    packs = sorted((root / "packs").glob("*"))
    readme = (root / "README.md").read_text(encoding="utf-8")
    failures, ids = 0, {}
    for p in packs:
        problems = []
        if not FILE_NAME.match(p.name):
            problems.append("file name must be lower-case letters, digits and dashes, ending in .mollikey")
        more, m = check_pack(p.read_bytes()) if p.is_file() else (["not a file"], None)
        problems += more
        pid = m.get("id") if isinstance(m, dict) else None
        if isinstance(pid, str):
            if pid in ids:
                problems.append(f"id '{pid}' is also used by {ids[pid]}")
            ids.setdefault(pid, p.name)
        if f"/raw/main/packs/{p.name})" not in readme:
            problems.append("not listed in README.md (add a row with its download link)")
        if problems:
            failures += 1
            print(f"FAIL {p.name}")
            for x in problems:
                print(f"  - {x}")
        else:
            print(f"ok   {p.name}  ({m['id']} v{m['packVersion']}, {m['licence']})")
    for link in re.findall(r"/raw/main/packs/([^)\s]+)\)", readme):
        if not (root / "packs" / link).is_file():
            failures += 1
            print(f"FAIL README.md links to packs/{link}, which isn't there")
    if not packs:
        print("no packs found")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))

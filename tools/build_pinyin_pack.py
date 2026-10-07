#!/usr/bin/env python3
"""Builds packs/chinese-pinyin.mollikey: a Pinyin dictionary for MolliKey's Pinyin keyboard.

Sources (download them yourself; nothing is fetched here):
  - CC-CEDICT, cedict_1_0_ts_utf-8_mdbg.txt (MDBG, CC BY-SA 4.0): which pinyin goes with which word.
  - jieba's dict.txt (Sun Junyi, MIT): how often each word is used, for the order of candidates.

Each entry is "toneless pinyin<TAB>simplified word<TAB>weight": pinyin without tones or spaces, ü written as v (nv → 女),
the weight from jieba's count on a log scale from 1 to 100 (1 for words jieba doesn't list). Only words written wholly
in Chinese characters are kept; entries that are only a "variant of" another are left out.

jieba counts a character, not its readings, so a character's rare reading would rank as high as its usual one (见 under
xian, not only jian). Where CC-CEDICT marks a reading as minor (its main sense archaic, literary, a variant, "see …" or
"used in …"; "also written" another way; or only bound forms), that entry's weight is cut to a third; a reading that
also has an unmarked entry keeps its full weight.
The zip uses fixed dates, so the same sources always give the same file.

Usage: python3 tools/build_pinyin_pack.py CEDICT.txt JIEBA_DICT.txt [out.mollikey]
"""
import hashlib, io, json, math, re, sys, zipfile

PACK_ID = "org.mollikey.lang.zh-pinyin"
PACK_VERSION = 1
LINE = re.compile(r"^(\S+) (\S+) \[([^\]]+)\] /(.*)/\s*$")
HAN = re.compile(r"^[㐀-䶿一-鿿豈-﫿\U00020000-\U0003134f]+$")
VARIANT = re.compile(r"^(old |archaic |erhua |Japanese |Korean |used in |same as )?variant of ", re.I)
SYLLABLE = re.compile(r"^[a-z]+$")
MINOR_SHARE = 0.3
# jieba's licence asks for its notice in every copy; the frequencies are in the dictionary, so the notice is too.
JIEBA_NOTICE = """The MIT License (MIT)

Copyright (c) 2013 Sun Junyi

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""


def minor(defs):
    """Whether CC-CEDICT marks this reading of a character as a minor one: its main (first) sense is archaic, literary,
    a variant or a pointer elsewhere; or it is "also written" another way; or every sense is a bound form."""
    senses = [d.strip() for d in defs.split("/") if d.strip()]
    if not senses:
        return False
    first = senses[0]
    if first.startswith(("see ", "used in ", "(literary)", "(old)", "(onom.)")) or "variant of" in first or re.search(r"\barchaic\b", first):
        return True
    return any("also written" in d for d in senses) or all(d.startswith("(bound form)") for d in senses)


def cedict(path, meta):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#!"):
                k, _, v = line[2:].strip().partition("=")
                meta[k.strip()] = v.strip()
                continue
            if line.startswith("#"):
                continue
            m = LINE.match(line.rstrip("\n"))
            if not m:
                continue
            _, simp, pinyin, defs = m.groups()
            if not HAN.match(simp):
                continue
            if all(VARIANT.match(d) for d in defs.split("/") if d):
                continue
            syllables = []
            for s in pinyin.split():
                s = s.lower().replace("u:", "v").replace("ü", "v").rstrip("012345")
                if not SYLLABLE.match(s):
                    break
                syllables.append(s)
            else:
                yield "".join(syllables), simp, len(simp) == 1 and minor(defs)


def jieba(path):
    counts = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                counts[parts[0]] = max(counts.get(parts[0], 0), int(parts[1]))
    return counts


def build(cedict_path, jieba_path):
    counts = jieba(jieba_path)
    top = math.log(max(counts.values()) + 1)
    best, meta = {}, {}
    entries = list(cedict(cedict_path, meta))
    readings = {}
    for key, word, _ in entries:
        if len(word) == 1:
            readings.setdefault(word, set()).add(key)
    for key, word, is_minor in entries:
        n = counts.get(word, 0)
        w = 100 * math.log(n + 1) / top if n else 1
        if is_minor and len(readings.get(word, ())) > 1:
            w *= MINOR_SHARE
        w = max(1, round(w))
        if best.get((key, word), 0) < w:
            best[(key, word)] = w
    lines = [f"{k}\t{w}\t{n}" for (k, w), n in sorted(best.items())]
    date = meta.get("date", "")[:10]
    head = (f"# Chinese Pinyin dictionary for MolliKey: toneless pinyin, simplified word, weight (1-100, higher first).\n"
            f"# Pinyin: CC-CEDICT ({date}), MDBG, CC BY-SA 4.0, https://www.mdbg.net/chinese/dictionary?page=cc-cedict\n"
            f"# Frequencies: jieba dict.txt, Copyright (c) 2013 Sun Junyi, MIT licence, https://github.com/fxsjy/jieba\n"
            f"# This list is licensed CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/\n"
            f"#\n# jieba's licence:\n" + "".join(f"# {l}".rstrip() + "\n" for l in JIEBA_NOTICE.splitlines()) + "#\n")
    return head + "\n".join(lines) + "\n", len(lines), date


def pack(text, count, date):
    data = text.encode("utf-8")
    manifest = {
        "format": "mollikey.pack", "version": 1, "id": PACK_ID, "name": "Chinese Pinyin dictionary",
        "packVersion": PACK_VERSION,
        "description": f"About {count // 1000}k words for the Pinyin keyboard, most used first: type nihao, get 你好.",
        "licence": "CC-BY-SA-4.0",
        "attribution": f"CC-CEDICT ({date}, MDBG, CC BY-SA 4.0); word frequencies from jieba (Sun Junyi, MIT)",
        "lexicons": [{"key": "pinyin", "path": "lexicons/pinyin.tsv", "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}],
    }
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, body in (("pack.json", json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")),
                           ("lexicons/pinyin.tsv", data)):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, body)
    return out.getvalue()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    text, count, date = build(sys.argv[1], sys.argv[2])
    target = sys.argv[3] if len(sys.argv) > 3 else "packs/chinese-pinyin.mollikey"
    with open(target, "wb") as f:
        f.write(pack(text, count, date))
    print(f"{target}: {count} entries (CC-CEDICT {date})")

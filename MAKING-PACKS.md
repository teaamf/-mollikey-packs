# Making a MolliKey pack

A pack is one file (`.mollikey`) that adds languages, keyboards, word lists, pictures and sounds to MolliKey. MolliKey
has no internet access: people download a pack with their browser (for example from this repository) and open it with
MolliKey, share it to MolliKey, or use Library › Packs › Open a pack. Library › Packs › Get packs opens the pack site in
the browser. MolliKey shows what the pack brings and its licence before installing.

Installed packs are read-only. A newer version of the same pack replaces the old one; an
older version is refused. Removing a pack keeps anything the person's own keyboards still use. Everything is undoable.

An example is in [`packs/runes-example.mollikey`](packs/runes-example.mollikey). It turns Latin letters into Elder
Futhark runes using rules only, on a keyboard that reuses MolliKey's built-in letters.

## The file

A zip with:

| Entry | What it is |
|---|---|
| `pack.json` | The manifest (below). Required. |
| `configuration.json` | A MolliKey workspace holding the pack's objects: keyboards, groups, keys, languages, writing systems, themes… Same format as the JSON editor. |
| `words/<file>.txt` | Word lists, one per language (below). |
| `assets/<file>` | Pictures (PNG, JPEG, WebP) and sounds (WAV, OGG, MP3, M4A) used by the pack's keys. |

Nothing else may be in the zip. Every file listed in `pack.json` must match its size and SHA-256. The whole pack may be
up to 96 MB.

### `pack.json`

```json
{
  "format": "mollikey.pack",
  "version": 1,
  "id": "org.example.lang.fr",
  "name": "French words",
  "packVersion": 3,
  "description": "Everyday French words for completion and corrections.",
  "licence": "CC-BY-4.0",
  "attribution": "Word counts: Example Corpus, 2024",
  "words": [ { "key": "fr", "path": "words/fr.txt", "size": 123456, "sha256": "…" } ],
  "assets": [ { "key": "img-sun", "path": "assets/sun.png", "size": 2048, "sha256": "…" } ]
}
```

- `id`: stable across versions; lower-case letters, digits, dots and dashes.
- `packVersion`: a whole number; raise it for each release.
- `licence`: required. Use an SPDX name. MolliKey's own packs use permissive licences only (CC0, CC BY, MIT…).
- `attribution`: who made the data. Required in practice for CC BY data, and shown to the person.
- `words[].key`: the language code the list is for (`en`, `fr`, `ar`, or `x-…` for a language of your own).
- `assets[].key`: the asset id in `configuration.json` that the file belongs to. Asset paths there start with `user/`.

### Word lists

Plain UTF-8 text, one entry per line:

```
# comment lines start with #
the	5000
wait	400
waiting	300
the wait	40
```

- `word<TAB>count`: how often the word is used. Without counts, earlier lines count as more frequent.
- `first second<TAB>count`: a word pair, for next-word suggestions.

MolliKey scales each list to the same range, so a person's own short list still comes first.

### A language made of rules

A language whose `inputMethod` is `RULES` types whatever its `rules` say: each rule is "typing `from` writes `to`".
The longest match wins (`sh` before `s`), and letters wait while a longer rule is still possible. This works for any
script, including an invented one. Use characters from the Unicode private-use area only together with a font that
has them.

```json
{ "id": "runes", "language": "x-runes", "writingSystemIds": ["runic"], "inputMethod": "RULES", "name": "Runes",
  "rules": [ { "from": "th", "to": "ᚦ" }, { "from": "a", "to": "ᚨ" } ] }
```

A keyboard in a pack may use MolliKey's built-in groups (`latin`, `symbols`, `toolbar`…) by id, as the example does.
If one of the person's objects already has an id the pack uses, the pack's object is renamed (never theirs).

## Adding a pack here

1. Put the `.mollikey` file in `packs/`, named after the pack (`packs/<name>.mollikey`).
2. Add a row to the table in `README.md`: name, what it brings, licence, and a download link of the form
   `https://github.com/teaamf/-mollikey-packs/raw/main/packs/<name>.mollikey`.
3. Open a pull request. The pack must say its licence and, for CC BY data, its attribution.

Every pull request runs `tools/check_packs.py` (you can run it yourself: `python3 tools/check_packs.py`). It refuses
what MolliKey would refuse when opening the file (unexpected or unlisted files, a size or SHA-256 that doesn't match,
a missing licence) and what this repository doesn't publish: a licence that isn't open, data needing attribution
without one, an id another pack already uses, or a pack missing from the table. MolliKey still checks the
configuration itself when the pack is installed.

For a new version, raise `packVersion` and replace the file under the same name: the download link stays the same, and
MolliKey replaces the older version when the new one is installed.

## Publishing elsewhere

A pack is just a file: attach it to a GitHub release or put it on any website. People tap it in their browser's
downloads and choose **Open with MolliKey**.

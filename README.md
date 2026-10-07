# MolliKey packs

Packs add languages, keyboards, word lists, pictures and sounds to MolliKey, the
keyboard you build yourself. This is where they are published.

MolliKey has **no internet access**, by design: a keyboard sees everything you type, so it never goes online. You get a
pack with your browser, and MolliKey reads it from the file.

## Installing a pack

1. On your phone, open this page (in MolliKey: **Library › Packs › Get packs**).
2. Tap a pack's **Download** link below.
3. Open the downloaded file and choose **MolliKey**: from the browser's downloads (*Open with MolliKey*), or share it to
   MolliKey from your files app. You can also pick it in **Library › Packs › Open a pack**.
4. MolliKey shows what the pack brings and its licence. Nothing is installed until you tap **Install**.

Every pack is checked when it is opened: only known kinds of files, each matching its listed size and SHA-256, and a
configuration that MolliKey validates before using. Removing a pack keeps anything your own keyboards still use, and
everything can be undone.

## Packs

| Pack | What it brings | Licence | Download |
|---|---|---|---|
| Chinese Pinyin dictionary | About 116,000 words for the Pinyin keyboard, most used first (type nihao, get 你好). Pinyin from CC-CEDICT; word frequencies from jieba ([notices](NOTICES.md)) | CC-BY-SA-4.0 | [chinese-pinyin.mollikey](https://github.com/teaamf/-mollikey-packs/raw/main/packs/chinese-pinyin.mollikey) |
| Runes (example) | A language made of rules: Latin letters write Elder Futhark runes (th → ᚦ, ng → ᛜ), with a keyboard and a few words | CC0-1.0 | [runes-example.mollikey](https://github.com/teaamf/-mollikey-packs/raw/main/packs/runes-example.mollikey) |

## Making a pack

See [MAKING-PACKS.md](MAKING-PACKS.md) for the file format, word lists and languages made of rules, and how to add a
pack here.

## Licences

This repository's own text and tools (this README, `MAKING-PACKS.md`, `tools/`) are dedicated to the public domain
under [CC0 1.0](LICENSE).

Each pack carries its own licence, shown in the table and inside the pack (`pack.json`), and MolliKey shows it before
installing. The sources packs were made from are credited in [NOTICES.md](NOTICES.md). Packs published here use open
licences only (CC0, CC BY, CC BY-SA, MIT and the like).

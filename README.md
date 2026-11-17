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
| Runes (example) | A language made of rules: Latin letters write Elder Futhark runes (th → ᚦ, ng → ᛜ), with a keyboard and a few words | CC0-1.0 | [runes-example.mollikey](https://github.com/teaamf/-mollikey-packs/raw/main/packs/runes-example.mollikey) |
| Français (AZERTY) | A mobile AZERTY layout with an É key, long-press accents, and MolliKey's shared symbols and emoji | CC0-1.0 | [french-azerty.mollikey](https://github.com/teaamf/-mollikey-packs/raw/main/packs/french-azerty.mollikey) |

After installing, open **Français (AZERTY)** on the keyboards page and tap **Use**. The built-in **Français** layout
remains selectable. In app revision `bbba14b` (17 November 2026), expand **Built-in** and scroll past the stock examples
to find the installed pack's keyboard. The pack uses MolliKey's shared key definitions and French accent popups
and requires ordinary key-width support on subdivided grids. Rebuild it with `python tools/build_french_azerty.py` and check its letter rows and
archive bytes with `python -m unittest discover -s tools -p test_french_azerty.py`.

## Making a pack

See [MAKING-PACKS.md](MAKING-PACKS.md) for the file format, word lists and languages made of rules, and how to add a
pack here.

## Licences

Each pack carries its own licence, shown in the table and inside the pack (`pack.json`), and MolliKey shows it before
installing. Packs published here use open licences only (CC0, CC BY, MIT and the like).

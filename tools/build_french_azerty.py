"""Build the mobile French AZERTY layout from MolliKey's shared controls and accents."""

import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo


PACK = Path(__file__).resolve().parents[1] / "packs" / "french-azerty.mollikey"
KEYBOARD = "fr-azerty"
GROUP = "fr-azerty-letters"
VARIANT = "fr-azerty-accents"
LAYOUT = "fr-azerty-grid"


def placement(button, row, column, width):
    return {"buttonId": button, "row": row, "column": column, "columnSpan": width}


def letter_row(letters, row, start=0):
    return [
        placement("key-e9" if letter == "é" else f"key-{letter}", row, start + 2 * index, 2)
        for index, letter in enumerate(letters)
    ]


def configuration():
    placements = letter_row("azertyuiop", 0) + letter_row("qsdfghjklm", 1)
    placements += [placement("shift", 2, 0, 3), *letter_row("wxcvbné", 2, 3), placement("delete", 2, 17, 3)]
    placements += [
        placement(button, 3, column, width)
        for button, column, width in (
            ("to-symbols", 0, 3),
            ("comma", 3, 2),
            ("space", 5, 8),
            ("period", 13, 2),
            ("enter", 15, 3),
            ("to-emoji", 18, 2),
        )
    ]
    return {
        "schemaVersion": 2,
        "keyboards": [{
            "id": KEYBOARD,
            "name": "Français (AZERTY)",
            "groupIds": [VARIANT, "symbols", "emoji"],
            "stateIds": ["case", "caps-lock"],
            "languageProfileId": "fr",
            "feedbackProfileId": "standard",
            "themeId": "dark",
            "toolbarGroupId": "toolbar",
        }],
        "layouts": [{"id": LAYOUT, "rows": 4, "columns": 20, "keyWidthUnit": 2}],
        "groups": [{"id": GROUP, "name": "Lettres AZERTY", "layoutId": LAYOUT, "placements": placements}],
        "groupVariants": [{
            "id": VARIANT,
            "name": "Lettres AZERTY (français)",
            "baseGroupId": GROUP,
            "overrides": [
                {"buttonId": f"key-{letter}", "trigger": "LONG_PRESS", "effectId": f"show-fr-{letter}-popup"}
                for letter in "ecauio"
            ],
        }],
    }


def build(destination=PACK):
    manifest = {
        "format": "mollikey.pack",
        "version": 1,
        "id": "org.mollikey.layout.fr-azerty",
        "name": "Français (AZERTY)",
        "packVersion": 1,
        "description": "French mobile AZERTY with an É key and accent popups.",
        "licence": "CC0-1.0",
    }
    with ZipFile(destination, "w") as archive:
        for name, data in (("pack.json", manifest), ("configuration.json", configuration())):
            entry = ZipInfo(name)
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            encoded = json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            archive.writestr(entry, encoded)


if __name__ == "__main__":
    build()

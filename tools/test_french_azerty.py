"""Check the checked-in French AZERTY package against its intended letter rows."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from build_french_azerty import PACK, build


class FrenchAzertyPackTest(unittest.TestCase):
    def test_archive_contains_every_letter_in_the_expected_row_order(self):
        with ZipFile(PACK) as archive:
            workspace = json.loads(archive.read("configuration.json"))

        placements = workspace["groups"][0]["placements"]
        rows = []
        for row in range(3):
            ordered = sorted(
                (key for key in placements if key["row"] == row and key["buttonId"].startswith("key-")),
                key=lambda key: key["column"],
            )
            rows.append("".join("é" if key["buttonId"] == "key-e9" else key["buttonId"][4:] for key in ordered))
        self.assertEqual(rows, ["azertyuiop", "qsdfghjklm", "wxcvbné"])
        self.assertEqual(sorted(char for char in "".join(rows) if "a" <= char <= "z"), list("abcdefghijklmnopqrstuvwxyz"))

    def test_builder_reproduces_the_published_archive(self):
        with TemporaryDirectory() as directory:
            rebuilt = Path(directory) / PACK.name
            build(rebuilt)
            self.assertEqual(rebuilt.read_bytes(), PACK.read_bytes())


if __name__ == "__main__":
    unittest.main()

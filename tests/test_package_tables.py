# ABOUTME: The README's two package tables list exactly the packages of accepted-packages.json (both are written by the
# ABOUTME: organizers' `lcbench intake accepted-packages` from their intake config); a hand edit of one is caught here.
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"`([0-9a-f]{64})`")


def block(readme: str, name: str) -> list[str]:
    """The table rows between the generator's markers for one block."""
    start = re.search(rf"^<!-- begin {name} .*-->$", readme, re.M)
    end = re.search(rf"^<!-- end {name} -->$", readme, re.M)
    if not start or not end or end.start() < start.end():
        raise AssertionError(f"README.md has no {name} block between its markers")
    return [line for line in readme[start.end():end.start()].splitlines() if line.startswith("| `")]


def pairs(rows: list[str]) -> set[tuple[str, str]]:
    out = set()
    for row in rows:
        found = SHA.findall(row)
        if len(found) != 2:
            raise AssertionError(f"a table row without a package and a task sha256: {row}")
        out.add((found[0], found[1]))
    return out


class PackageTables(unittest.TestCase):
    def setUp(self):
        self.readme = (ROOT / "README.md").read_text()
        self.listing = json.loads((ROOT / "accepted-packages.json").read_text())

    def test_accepted_table_lists_the_accepted_packages(self):
        want = {(p["package_sha256"], p["task_sha256"]) for rows in self.listing["tasks"].values() for p in rows}
        self.assertEqual(pairs(block(self.readme, "accepted-packages")), want)

    def test_retired_table_lists_the_retired_packages(self):
        want = {(p["package_sha256"], p["task_sha256"]) for rows in self.listing.get("retired", {}).values()
                for p in rows}
        self.assertEqual(pairs(block(self.readme, "retired-packages")), want)

    def test_every_accepted_task_is_named_in_its_table(self):
        rows = block(self.readme, "accepted-packages")
        for task in self.listing["tasks"]:
            self.assertTrue(any(row.startswith(f"| `{task}` |") for row in rows), task)


if __name__ == "__main__":
    unittest.main()

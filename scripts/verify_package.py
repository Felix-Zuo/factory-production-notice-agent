from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


BLOCKED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", "output", "data", "build", "dist"}
BLOCKED_SUFFIXES = (".pyc", ".pyo", ".sqlite", ".db", ".exe", ".zip")


def unsafe_archive_entries(archive: Path) -> list[str]:
    with zipfile.ZipFile(archive) as package:
        unsafe: list[str] = []
        for name in package.namelist():
            parts = Path(name).parts
            if any(part in BLOCKED_PARTS for part in parts):
                unsafe.append(name)
            elif any(part.startswith("output_") for part in parts):
                unsafe.append(name)
            elif any(part.endswith(".egg-info") for part in parts):
                unsafe.append(name)
            elif name.endswith(BLOCKED_SUFFIXES):
                unsafe.append(name)
        return unsafe


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive")
    args = parser.parse_args()

    archive = Path(args.archive)
    unsafe = unsafe_archive_entries(archive)
    if unsafe:
        print("Unsafe archive entries:")
        for entry in unsafe:
            print(f"- {entry}")
        raise SystemExit(1)
    print(f"Package verified: {archive}")


if __name__ == "__main__":
    main()

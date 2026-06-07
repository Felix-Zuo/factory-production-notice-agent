from __future__ import annotations

import argparse
import fnmatch
import zipfile
from pathlib import Path


EXCLUDE_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", "output", "data", "build", "dist"}
EXCLUDE_PATTERNS = ["*.pyc", "*.pyo", "*.sqlite", "*.db", "*.exe", "*.zip"]


def should_skip(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return True
    if any(part.endswith(".egg-info") for part in path.parts):
        return True
    return any(fnmatch.fnmatch(path.name, pattern) for pattern in EXCLUDE_PATTERNS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="factory-production-notice-agent")
    parser.add_argument("--output", default="output")
    args = parser.parse_args()

    root = Path.cwd()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{args.name}.zip"

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as package:
        for path in root.rglob("*"):
            rel = path.relative_to(root)
            if path.is_file() and not should_skip(rel):
                package.write(path, Path(args.name) / rel)

    print(archive)


if __name__ == "__main__":
    main()

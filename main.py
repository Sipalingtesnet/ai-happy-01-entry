#!/usr/bin/env python3
"""
main.py - Deterministic entry copier and verifier for make.fun competition entry 'ai-happy-01'.
Copies entry.png from the repository root to MAKEFUN_OUTPUT_DIR (defaulting to /output/entry.png),
ensures the output directory exists, and cryptographically verifies SHA-256 integrity.
"""

import os
import sys
import hashlib
import shutil
from pathlib import Path

def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    source_path = Path(__file__).resolve().parent / 'entry.png'

    if not source_path.exists():
        print(f"Error: Critical source image '{source_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    dest_path = os.path.join(output_dir, "entry.png")

    # Deterministically copy entry.png to the target output location
    shutil.copyfile(source_path, dest_path)

    # Verify cryptographic integrity
    src_hash = hash_file(source_path)
    dest_hash = hash_file(dest_path)

    if src_hash != dest_hash:
        print(f"Error: SHA-256 hash mismatch! source={src_hash}, destination={dest_hash}", file=sys.stderr)
        sys.exit(1)

    print(f"Verified & copied entry.png -> {dest_path} [SHA-256: {src_hash}]")

if __name__ == "__main__":
    main()

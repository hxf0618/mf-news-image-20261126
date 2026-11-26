#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261126.

Copies the pre-drawn front-page image entry.png (in this repository)
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
Standard library only; no network.
"""
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_DIM = 1024


def validate_png(path):
    """Check the copied file is a real PNG, <=1 MiB, <=1024x1024."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"{path} is {size} bytes, over the 1 MiB limit")
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != PNG_SIGNATURE:
        raise ValueError(f"{path} is not a PNG file")
    # IHDR chunk: length (4) + "IHDR" (4) + width (4) + height (4).
    if header[12:16] != b"IHDR":
        raise ValueError(f"{path} has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"{path} is {width}x{height}, over 1024x1024")
    return size, width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    size, width, height = validate_png(dest)
    print(f"wrote {dest} ({width}x{height}, {size} bytes)")


if __name__ == "__main__":
    main()

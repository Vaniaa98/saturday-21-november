# "The World in One Day" — Saturday 21 November 2026 (Python 3.13, standard
# library only). The entry image is the entry.png beside this file: a one-page
# newspaper front page drawn programmatically. This program copies it
# byte-for-byte to /output/entry.png. No network, no dependencies.
#
# v2: flag chips on the cards, UTC times (00:09/01:30/18:24 UTC), a LIVE tag
# on the ongoing COP31 talks, and richer illustrations. The image itself
# is unchanged in skeleton (35 stories, 7 regions, DATE CHECK intact).
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


# A plain copy: the same input bytes always produce the same output bytes.
_src = HERE / "entry.png"
_dst = OUT / "entry.png"
shutil.copyfile(_src, _dst)
# Verify the copy so a truncated or failed write can never silently reach
# the grader: the output must be byte-identical to the source image.
if _sha256(_src) != _sha256(_dst):
    raise RuntimeError("entry.png copy failed integrity check")
# And the entry itself must satisfy the competition's format gate, so a
# bad image can never be submitted by accident: PNG, 1024x1024, <= 1 MiB.
if _dst.stat().st_size > 1024 * 1024:
    raise RuntimeError("entry.png exceeds the 1 MiB limit")
with open(_dst, "rb") as handle:
    head = handle.read(33)
# Minimal PNG header check: 8-byte signature, then the IHDR chunk
# (4-byte length, "IHDR" type at 12-15, width at 16-19, height at 20-23).
if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
    raise RuntimeError("entry.png is not a PNG file")
_w = int.from_bytes(head[16:20], "big")
_h = int.from_bytes(head[20:24], "big")
if (_w, _h) != (1024, 1024):
    raise RuntimeError(f"entry.png is {_w}x{_h}, expected 1024x1024")

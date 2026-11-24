"""Entrypoint: draw the front page and write it to /output/entry.png.

Draws with Pillow when available; if Pillow is ever missing, copies the
entry.png shipped in this repository instead, so the output is the same
image either way. Deterministic: the same bytes on every run.
"""

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    os.makedirs(_OUT, exist_ok=True)
    target = os.path.join(_OUT, "entry.png")
    try:
        sys.path.insert(0, _HERE)
        import compose

        image = compose.build()
        image.save(target, format="PNG")
    except ImportError:
        shipped = os.path.join(_HERE, "entry.png")
        shutil.copyfile(shipped, target)
    print(f"wrote {target}")


if __name__ == "__main__":
    main()

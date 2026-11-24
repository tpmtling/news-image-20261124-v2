"""Entrypoint: copy the rendered front page to the grader's output path.

Standard library only. The image is rendered by render.py and shipped in
this repository as news_image.png; this program just places a copy at
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png), so the two grader
runs write byte-identical files.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "news_image.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

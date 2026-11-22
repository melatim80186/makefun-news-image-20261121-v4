# main.py — entrypoint for news-image-20261121 v4.
# Copies the entry image (drawn by build_entry.py) to the output dir.
# Deterministic: same bytes on every run, no network, stdlib only.
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    if size > 1048576:
        sys.exit(f"entry.png too large: {size} bytes")
    print(f"wrote {dst} ({size} bytes)")


if __name__ == "__main__":
    main()

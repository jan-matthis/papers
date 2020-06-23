import os
import shutil
import sys
from pathlib import Path


def preview(
    fname_in: str,
    fname_out: str,
    num_pages: int = 8,
    quality: int = 95,
    resize: str = "x230",
) -> int:
    if not shutil.which("montage"):
        print("ERROR: ImageMagick is required")
        return 1
    cmd = f"montage {fname_in}[0-{num_pages-1}] -mode Concatenate -tile x1 -quality {quality} -resize {resize} -colorspace sRGB {fname_out}"
    return os.system(cmd)

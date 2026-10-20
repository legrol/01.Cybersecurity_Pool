# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rdel-olm <rdel-olm@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/23 18:11:51 by rdel-olm          #+#    #+#              #
#    Updated: 2026/03/23 20:15:16 by rdel-olm         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


# Scorpion inspects one or more image files and prints their metadata.
#
# Workflow summary:
# 1) Read one or multiple file paths from the command line.
# 2) Validate supported extensions (jpg/jpeg, png, gif, bmp).
# 3) Open each image safely and display core file/image information.
# 4) Print EXIF tags when present and include extra embedded metadata if available.
#
# The tool is designed for quick forensic-style inspection from terminal output,
# with clear per-file sections and non-blocking error handling for invalid inputs.

import argparse
import os
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")


def parse_args():
    parser = argparse.ArgumentParser(
        prog="./scorpion",
        description="Display EXIF and basic metadata from one or more images.",
    )
    parser.add_argument("files", nargs="+", help="Image files to inspect")
    return parser.parse_args()


def format_ts(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def is_supported(path):
    return path.lower().endswith(SUPPORTED_EXTENSIONS)


def print_basic_metadata(path, image):
    stats = os.stat(path)
    print(f"{'File':28}: {os.path.basename(path)}")
    print(f"{'Path':28}: {os.path.abspath(path)}")
    print(f"{'Dimensions':28}: {image.size[0]} x {image.size[1]}")
    print(f"{'Format':28}: {image.format}")
    print(f"{'Mode':28}: {image.mode}")
    print(f"{'Created':28}: {format_ts(stats.st_ctime)}")
    print(f"{'Modified':28}: {format_ts(stats.st_mtime)}")


def print_exif_data(image):
    exif_data = image.getexif()
    if not exif_data:
        print(f"{'EXIF':28}: No EXIF data found")
        return

    print("EXIF data:")
    for exif_id in exif_data:
        tag_name = TAGS.get(exif_id, f"Unknown({exif_id})")
        value = exif_data.get(exif_id)
        print(f"  {tag_name:26}: {value}")


def print_other_metadata(image):
    if not image.info:
        return

    print("Other metadata:")
    for key, value in image.info.items():
        print(f"  {key:26}: {value}")


def inspect_files(paths):
    for path in paths:
        print("=" * 80)
        print(f"Inspecting: {path}")

        if not is_supported(path):
            print(
                "Error: Unsupported extension "
                f"(allowed: {', '.join(SUPPORTED_EXTENSIONS)})"
            )
            continue

        if not os.path.exists(path):
            print("Error: File does not exist")
            continue

        try:
            with Image.open(path) as image:
                print_basic_metadata(path, image)
                print_exif_data(image)
                print_other_metadata(image)
        except Exception as exc:
            print(f"Error: Could not open or parse image ({exc})")


if __name__ == "__main__":
    args = parse_args()
    inspect_files(args.files)

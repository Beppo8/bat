#!/usr/bin/env python

import subprocess
import glob
import sys
import os.path as path
import os
import argparse


BAT_OPTIONS = [
    "--no-config",
    "--style=plain",
    "--color=always",
    "--theme='1337'",
    "--italic-text=always",
]


def create_highlighted_versions(output_basepath):
    root = os.path.dirname(os.path.abspath(__file__))

    for source in glob.glob(path.join(root, "source", "*", "*")):
        try:
            bat_output = subprocess.check_output(
                ["bat"] + BAT_OPTIONS + [source], stderr=subprocess.PIPE,
            )

            source_dirname = path.basename(path.dirname(source))
            source_filename = path.basename(source)

            output_dir = path.join(output_basepath, source_dirname)
            output_path = path.join(output_dir, source_filename)

            os.makedirs(output_dir, exist_ok=True)

            with open(output_path, "wb") as output_file:
                output_file.write(bat_output)

            relative_path = path.relpath(output_path, root)
            print("Created '{}'".format(relative_path))
        except subprocess.CalledProcessError as err:
            print(
                "=== Error: Could not highlight source file '{}".format(source),
                file=sys.stderr,
            )
            print(
                "=== bat stdout:\n{}".format(err.stdout.decode("utf-8")),
                file=sys.stderr,
            )
            print(
                "=== bat stderr:\n{}".format(err.stderr.decode("utf-8")),
                file=sys.stderr,
            )
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script creates syntax-highlighted versions of all "
        "files in the 'source' directory."
    )
    parser.add_argument(
        "--output",
        "-O",
        metavar="PATH",
        help="Output directory",
        required=True,
        type=str,
    )

    args = parser.parse_args()

    create_highlighted_versions(output_basepath=args.output)

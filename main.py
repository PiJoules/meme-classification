#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
from memeclass import MemeClassifier


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser("Meme classifier")

    parser.add_argument("memes", nargs="+",
                        help="Memes to classify.")
    parser.add_argument("--templates_dir", default="templates",
                        help="Directory to search for meme templates to "
                        "compare against.")
    parser.add_argument("-v", "--verbose", default=False, action="store_true",
                        help="Verbose output. (default: %(default)s).")

    return parser.parse_args()


def main():
    args = get_args()

    mc = MemeClassifier(args.templates_dir)
    for img_fname in args.memes:
        meme_name = mc.classify(img_fname, debug=args.verbose)
        if meme_name is None:
            print("Could not find meme match for {}.".format(img_fname))
        else:
            print(img_fname, meme_name)

    return 0


if __name__ == "__main__":
    sys.exit(main())


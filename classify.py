from __future__ import print_function

import cv2
import glob
import urllib
import re
import numpy as np


def fname_to_name(fname, dirname):
    fname = re.sub('^' + dirname + '\/', '', fname)
    fname = re.sub('\.(jpg|png|jpeg)', '', fname)
    fname = re.sub('-', ' ', fname)
    return fname


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image


def euclidean_distance(img1, img2):
    # Distance as sum of square of differences
    dist = np.sum((img1.astype("float") - img2.astype("float")) ** 2)

    # Normalize
    dist /= (img1.shape[0] * img1.shape[1] * 1.0)

    # Do not need to take the sqrt since we are comparing relatively
    # and do not need to know absolute values.
    return dist


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument("img")
    parser.add_argument("--url", action="store_true", default=False)
    parser.add_argument("--comparisons_dir", default="comparisons")
    parser.add_argument("-v", "--verbose", default=False, action="store_true")

    return parser.parse_args()


def main():
    args = get_args()

    dirname = args.comparisons_dir
    filenames = glob.glob(dirname + '/*')
    img = args.img

    if args.url:
        img = url_to_image(img)
    else:
        img = cv2.imread(img)
    best = None
    best_val = float("Inf")
    for filename in filenames:
        img_ = cv2.imread(filename)
        img_ = cv2.resize(img_, (img.shape[1], img.shape[0]))
        dist = euclidean_distance(img, img_)

        if args.verbose:
            print(filename, dist)

        if dist < best_val:
            best_val = dist
            best = filename
    print("best:", fname_to_name(best, dirname), best_val)

    return 0


if __name__ == "__main__":
    main()


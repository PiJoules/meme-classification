#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vendor
vendor.add("lib")

# Import the Flask Framework
from flask import Flask, render_template, request
app = Flask(__name__)

import StringIO
import cv2
import glob
import classify
import base64
import requests
import numpy as np

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
COMPARISONS_DIR = "comparisons"


def allowed_file(filename):
    """Just check if the file is one of the allowed file types."""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = requests.get(url)
    image = np.asanyarray(bytearray(resp.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image


def stringio_to_image(img_stream, cv2_img_flag=0):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, 1)


def img_to_base64(img):
    content = cv2.imencode('.png', img)[1]
    b64 = base64.encodestring(content)
    return b64


def best_meme(img):
    filenames = glob.glob(COMPARISONS_DIR + "/*")
    best = None
    best_val = float("Inf")
    for filename in filenames:
        img_ = cv2.imread(filename)
        img_ = cv2.resize(img_, (img.shape[1], img.shape[0]))
        dist = classify.euclidean_distance(img, img_)
        if dist < best_val:
            best_val = dist
            best = filename
    return classify.fname_to_name(best, COMPARISONS_DIR)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            url = request.form.get("url")
            f = request.files['file']
            if url:
                img = url_to_image(url)
            elif f and allowed_file(f.filename.lower()):
                # Can get the image file data without having to save it
                # on the system.
                img = stringio_to_image(StringIO.StringIO(f.read()))
            else:
                return render_template("index.html", meme=None, b64=None)

            meme = "I classify this meme as: " + best_meme(img).upper()
            b64 = img_to_base64(img)
            return render_template("index.html", meme=meme, b64=b64)
        except Exception as e:
            return render_template("index.html", meme="Error: " + str(e), b64=None)
    return render_template("index.html", meme=None, b64=None)


if __name__ == '__main__':
    app.run()  # For production


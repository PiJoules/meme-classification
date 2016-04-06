# Meme Classification

The ultimate goal of this repo is to (as the title suggests) classify memes.


## How it works
Currently, the the algorithm works by comparing a provided image to one of many memes
provided in he `comparisons/` directory. The atual comparsion is essentially just comparing the
individual rgb values for each pixel after resizing the comparison image to the dimensions of
the meme I would like to classify. This could loosely be defined as a euclidean distance
classifier since I'm only comparing against 1 sample per class.

Hopefully this will go into further development the further my class advances into the Pattern
Recognition class I'm in.


## Dependencies
Both numpy and opencv are dependencies for this project. Since I have trouble installing numpy
in particular to a virtualenv, I would suggest installing it into your global pip:
```sh
$ sudo apt-get install python-opencv
$ sudo pip instal numpy
```

If you plan to run the flask server, you will also need to install whatever is listed in
`requirements.txt`:
```sh
$ sudo pip install -r requirements.txt
```


## Usage
There is currently a web interface for classifying memes at `http://memeclassifier.3341b.com/`, 
but a script is also provided that can run on a bash termial.

### Command line
To classify an image on your local machine:
```sh
$ python classify.py /path/to/image
```

To classify an image at a url, just add the `--url` flag:
```sh
$ python classify.py http://image.ur/path/to/image --url
```

### Server
To start the flask server like the one that's running on the website:
```sh
$ python __init__.py
```


## Future Work
- I would like to develop this enough that I could use it as my term project for my pattern recognition class.
- Instead of comparing against 1 image, collect data (from, lets say, reddit) to compare against training data
  via a bayesian or k-nearest-neighbors classifier.
- See if it's possible to eveolve this to a point that memes could be generated from this.
- If a meme is classified as a Pepe, also display it's rarity in how frequently it appears.




import os
import logging
import traceback
import argparse 

# Set logging level=DEBUG
logging.basicConfig(level=0)

# How to use argparse:
# https://www.pyimagesearch.com/2018/03/12/python-argparse-command-line-arguments/
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help="Path to video file")
ap.add_argument("-b", "--style", action='store_true', help="ON/OFF blur filter")
args = vars(ap.parse_args())

file_name = os.path.abspath(args['file'])
if not os.path.isfile(file_name):
    raise ValueError('File {} not exists'.format(file_name))

style = args['style']

app = App({"filename": 'video.mpg'})
app.start()
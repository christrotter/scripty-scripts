#!/usr/bin/env python3

"""_summary_
This script renames photos in a directory to a specific naming convention.
e.g. 2023-10-15 08.15.13-2.jpg
date time sequence extension

We want to get the date and time the photo was taken from the metadata of the photo.
We will use the exifread library to get the metadata.

"""

from datetime import date
import exifread
from pprint import pprint
import os
import re

path_name = '/Users/christrotter/Dropbox/PhotoAlbum/bird-pics/'

# we want to get this field and turn that into the filename
#  e.g. 'Image DateTime': (0x0132) ASCII=2023:07:01 09:47:26 @ 226,
dirs_to_process = []
reg_compile = re.compile("^\d{8}$")
for dirpath, dirnames, filenames in os.walk(path_name):
    dirs_to_process = dirs_to_process + [dirname for dirname in dirnames if  reg_compile.match(dirname)]

i = 0
for dir in dirs_to_process:
    # print(dir)
    os.chdir(path_name + dir)
    for filename in os.listdir('.'):
        if i == 100:
            break
        i+=1
        if filename.endswith('.JPG'):
            f = open(filename, 'rb')
            tags = exifread.process_file(f)
            print(filename, ': ', tags['Image DateTime'])
            # output e.g. 2023:06:30 07:41:08
            # we want to turn this into 2023-06-30 07.41.08-1.jpg
            old_filepath = os.path.join(path_name + dir, filename)
            print(old_filepath)
            new_filename = tags['Image DateTime'].values.replace(':', '-').replace(' ', '.') + '.jpg'
            print(new_filename)
            new_filepath = os.path.join(path_name, new_filename)
            print(new_filepath)
            os.rename(old_filepath, new_filepath)
            f.close()



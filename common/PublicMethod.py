#!usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import os
import re


def get_format_currenttime():
    currenttime = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    return currenttime


def get_fullfile_from_path(path, ext=None):
    allfiles = []
    needExtFilter = (ext != None)
    for root, dirs, files in os.walk(path):
        for filespath in files:
            filepath = os.path.join(root, filespath)
            extension = os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles


def get_file_name_from_path(path, ext=None):
    allfilenames = []
    needExtFilter = (ext != None)
    for root, dirs, files in os.walk(path):
        for filespath in files:
            filename, suffix = os.path.splitext(filespath)
            extension = os.path.splitext(filespath)[1][1:]
            if needExtFilter and extension in ext:
                allfilenames.append(filename)
            elif not needExtFilter:
                allfilenames.append(filename)
    return allfilenames


def clean_brackets_from_str(string):
    final_string = re.sub(r'[\(（][\s\S]*[\)）]', "", string)
    return final_string

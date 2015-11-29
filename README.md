Concurrent Http Downloader
==========
A command line program with Python that downloads files over the network and store them on the local file system. 

The program will receive two inputs:

1. The URL of an RSS Feed containing links to the files to be downloaded (a sample is given below)
2. The path to the directory where the downloaded files are going to be stored is

python downloader.py --feed=RSS-Feed-URL --output=PATH-TO-DIRECTORY

Features
=========

1. This program remember if a file has been downloaded previously. So if the file has been downloaded once, it skips downloading it again.
2. If a file has been downloaded partially, it can resume from the point where it left off.
3. This program is be able to log its activities in a text file.
4. This program supports HTTP.
5. The program should be designed in a way so that it can be easily extended to support additional protocols.
6. This program is capable of downloading multiple files in parallel.
7. This program is capable donwnload single file in parallel mode.

Installation
==========

pip install virtualenv

virtualenv .env 

python setup.py

python db_create.py

Test URL
============

Here is a link to the sample RSS Feed: https://dl.dropboxusercontent.com/u/6160850/downloads.rss





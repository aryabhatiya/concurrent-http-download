#!.env/bin/python
import os
import unittest
from downloads import Downloads


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_config(self):
        Downloads.config( url =   'https://dl.dropboxusercontent.com/u/6160850/downloads.rss', path =  '/usr/local/src/testdownload' )
#        conf = Downloads.config()
        assert Downloads.proto == 'https'
        
if __name__ == '__main__':
        unittest.main()

#!.env/bin/python
import os
import unittest
from downloads import Downloads


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_config(self):
        Downloads.config( url = 'https://dl.dropboxusercontent.com/u/6160850/downloads.rss', path = '/usr/local/src/testdownload' )
        assert Downloads._url.scheme == 'https'
        assert Downloads._url.host == 'dl.dropboxusercontent.com'
        assert Downloads._url.last == 'downloads.rss'


if __name__ == '__main__':
        unittest.main()

#!.env/bin/python
import os
import unittest
from downloads import Downloads
from db_create import prepare
from db_create import runmachine
import filecmp

class TestCase(unittest.TestCase):
    def setUp(self):
        prepare()
        pass

    def test_config(self):
        Downloads.config( url = 'https://dl.dropboxusercontent.com/u/6160850/downloads.rss', path = '/usr/local/src/testdownload' )
        assert Downloads._url.scheme == 'https'
        assert Downloads._url.host == 'dl.dropboxusercontent.com'
        assert Downloads._url.last == 'downloads.rss'

    def test_fulldownload(self):
        runmachine()
        assert filecmp('/usr/local/src/testdownload/downloads.rss','/usr/local/src/test/downloads.rss') == True

    def test_fulldownloadafter(self):
        Downloads.config( url = 'https://dl.dropboxusercontent.com/u/6160850/downloads.rss', path = '/usr/local/src/testdownload' )
        assert Downloads.run() == False

    def test_partialdownload(self):
        runmachine(False)
        assert filecmp('/usr/local/src/testdownload/downloads.rss','/usr/local/src/testdownload/downloads.rss') == False
        runmachine(True)
        assert filecmp('/usr/local/src/testdownload/downloads.rss','/usr/local/src/test/downloads.rss') == True
        
    


if __name__ == '__main__':
        unittest.main()

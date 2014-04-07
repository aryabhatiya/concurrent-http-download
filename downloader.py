#!.env/bin/python
# parse command line argument and call file download module
from downloads import Downloads
from downloads import log2 , log
import feedparser
import sys
from optparse import OptionParser


def arguments():
    """ Parse command line arguments """
    parser = OptionParser(usage="usage: %prog [options] --feed=<RSS-Feed-URL>\
                                --output=<PATH-TO-DIRECTORY>",
                          version="%prog 1.0")
    parser.add_option("-f", "--feed",
                      dest="feed",
                      help="rss feed link")
    parser.add_option("-o", "--output",
                      action="store",
                      dest="output",
                      help="download directory")
    (options, args) = parser.parse_args()
    return options


if __name__ == '__main__':
    option = arguments()
    ''' checking for missing argument '''
    log2('getting feed ...' +  option.feed )
    d = feedparser.parse(option.feed) 
    log2('urls are ...' +  str([ en['link']  for en in d.entries ]) )
    Downloads.config( urls = [ en['link']  for en in d.entries ] , path = option.output )
    Downloads.run()

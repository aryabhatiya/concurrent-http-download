#!.env/bin/python
# parse command line argument and call file download module
from downloads import Downloads
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
    Downloads.config( url = option.feed,path = option.output )
    Downloads.run()

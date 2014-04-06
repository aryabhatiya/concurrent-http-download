#import gevent
#from gevent import Greenlet

class Download(object):
    
    def __init__(self, url, filestat, log):
        self.filestat = filestat
        self.url = url
        self.log = log

    def isdownloaded(self):
        if self.filestat.block == self.filestat.splits:
            self.filestat.isdownloaded = 1 
            self.filestat.update()

    def ispartial(self):
        if self.filestat.block > 0:
            self.filestat.partial = 1 
            self.filestat.update()

    def filesize(self):
        raise NotImplementedError("Subclass must implement abstract method")

    # def run(self):
    #     raise NotImplementedError("Subclass must implement abstract method")

    @property 
    def splits(self):
        return self._split

    @splits.getter
    def splits(self,num):
        self._split=num
    

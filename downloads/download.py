class Download(object):
    
    def __init__(self):
        self.filestat = filestat
        self.url = url

    def isdownloaded(self):
        pass
    def ispartial(self):
        pass
    def filesize(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def run(self):
        raise NotImplementedError("Subclass must implement abstract method")


    @property 
    def splits(self):
        return self._split

    @splits.getter
    def splits(self,num):
        self._split=num
    

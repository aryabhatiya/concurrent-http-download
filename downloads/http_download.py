from download import Download
import httplib

class HttpDownload(Download):
    def __init__(self, url, filestat, log):
        super(HttpDownload, self).__init__(url, filestat, log)
#        Download.__init__(url, filestat, log)
#        self.port = len(self.url.host.split(":")) > 0 and self.url.host.split(":")[1] or 0 
        self.port = 0
        self.conn = self.port and httplib.HTTPSConnection(self.url.host.split(":")[0],self.port) \
            or httplib.HTTPSConnection(self.url.host)

    def filesize(self):
        self.conn.request("HEAD", self.url.path)
        response = self.conn.getresponse()
        headers = response.getheaders()
        fsize = filter(lambda (x,y): x == 'content-length',  headers)[0][1]
        self.filestat.size = int(fsize)
        self.filestat.update()

    def http_range(self,block):
        step = self.filestat.size / self.filestat.splits
        lower = step * block
        upper = block == self.filestat.splits and   self.filestat.size or (block + 1) * step - 1 
        range = 'bytes=' + str(lower) + '-' + str(upper)
        return { 'Range': range }

    def run(self,block):        
        self.conn = self.port and httplib.HTTPSConnection(self.url.host.split(":")[0],self.port) \
            or httplib.HTTPSConnection(self.url.host)

        self.conn.request("GET", self.url.path, headers=self.http_range(block)) 
        print self.http_range(block)
        print self.url.path
        resp = self.conn.getresponse()
        assert resp.status == 206
        assert resp.status == httplib.PARTIAL_CONTENT
        # >>> resp.getheader('content-range')
        # 'bytes 0-299/612'
        content = resp.read()
        self.filestat.writefs(content)
#        if block == filestat.split:
#            self.filestat.wiret
        #len(content) 300

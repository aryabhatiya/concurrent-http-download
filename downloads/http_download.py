from download import Download
import httplib
from downloads import log , log2
class HttpDownload(Download):
    def __init__(self, url, filestat, msg):
        super(HttpDownload, self).__init__(url, filestat, msg)
#        Download.__init__(url, filestat, log)
#        self.port = len(self.url.host.split(":")) > 0 and self.url.host.split(":")[1] or 0 
        self.port = 0


    def filesize(self):
        conn = self.port and httplib.HTTPSConnection(self.url.host.split(":")[0],self.port) \
            or httplib.HTTPSConnection(self.url.host)
        conn.request("HEAD", self.url.path)
        response = conn.getresponse()
        headers = response.getheaders()
        fsize = filter(lambda (x,y): x == 'content-length',  headers)[0][1]
        self.filestat.size = int(fsize)
        self.filestat.update()

    def http_range(self,sector):
        range = 'bytes=' + str(sector.start) + '-' + str(sector.end)
        return { 'Range': range }

    def run(self,sector):        
        success = True
        log2("connecting ... " + self.url.host)
        conn = self.port and httplib.HTTPSConnection(self.url.host.split(":")[0],self.port) \
            or httplib.HTTPSConnection(self.url.host)
        if conn:
            log2("connecting success ... " + self.url.host)
            conn.request("GET", self.url.path, headers=self.http_range(sector)) 
#        log(self.http_range(sector))
            resp = conn.getresponse()
#        assert resp.status == 206
#        assert resp.status == httplib.PARTIAL_CONTENT
        # >>> resp.getheader('content-range')
        # 'bytes 0-299/612'
            content = resp.read()
            self.sector.write(content)
#       sector.isdownloaded = 1
#        sector.update()
#        self.filestat.status('Partial Downloaded')
#        log(sector)
            self.msg.put_nowait(str(sector.id))
        else:
            log2("connecting failed ... " + self.url.host)
            self.msg.put_nowait(str(-sector.id))
#        if block == filestat.split:
#            self.filestat.wiret
        #len(content) 300

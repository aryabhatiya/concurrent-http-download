from http_download import HttpDownload
from ftp_download import FtpDownload
from file_manager import FileManager
from url import URL
from downloads import log

class FileDownloader(object):
    ''' scheme http / ftp '''
    _service = {}

    def __init__(self):
        ''' initiate the corresponding service according to protocol '''
        self._service['http'] = self._service['https'] = self.load_http
        self._service['ftp'] = self.load_ftp
        self.fileManager = FileManager()

    def config(self, **config):
        self._config = config
        for key, value in config.items():
            self.__dict__[key] = value

        if not self.path:
            raise ValueError("Path is Missing")

        if not self.url:
            raise ValueError("Uri is Missing")
        self._url = URL(self.url)

        self.init_service()

    def init_service(self):
        if self._url.scheme in self._service:
            self.filestat = self.fileManager.infs(self.path, self._url.last)
            if not self.filestat:
                self.service = self._service[self._url.scheme] 
                self.filestat = self.fileManager.add(self.path, self._url.last)
                self.filestat.status('new ' + self._url.scheme )
            else:
                self.service = self.filestat and not self.filestat.isdownloaded \
                    and self._service[self._url.scheme] or None

        else:
            raise ValueError('protocol: ' + self.scheme + ' not supported')

    def load_ftp(self):
        return FtpDownload(self._url, self.filestat,log)

    def load_http(self):
        return HttpDownload(self._url, self.filestat,log)

    def run(self):
        """ run the corresponding service according to protocol """        
        if not self.service:
            self.filestat.status('already downloaded')
        dload = self.service()        
        dload.filesize()
        self.filestat.status('filesize')
        
        for i in range(self.filestat.partial,self.filestat.splits):
            dload.run(i)
            self.filestat.partial = i+1
            self.filestat.update()
            self.filestat.status('Partial Downloaded')

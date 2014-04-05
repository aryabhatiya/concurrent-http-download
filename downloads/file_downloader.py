from http_download import HttpDownload
from ftp_download import FtpDownload
from file_manager import FileManager
from url import URL

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
        if self._url.proto in self._service:
            self.filestat = self.fileManager.infs(self.path, self._url.last)
            self.service = self.filestat and not self.filestat.isdownloaded \
                and self._service[self._url.proto] or None
        else:
            raise ValueError('protocol: ' + self.proto + ' not supported')

    def load_ftp(self):
        return FtpDownload(self._url, self.filestat)

    def load_http(self):
        return HttpDownload(self._url, self.filestat)

    def run(self):
        """ run the corresponding service according to protocol """
        return self.filestat and not self.filestat.isdownloaded \
            and self.service().run() or None

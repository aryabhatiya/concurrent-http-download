import gevent
from gevent.queue import Queue
from gevent.pool import Group
from gevent import monkey
# patches stdlib (including socket and ssl modules) to cooperate with other greenlets
monkey.patch_all()
from http_download import HttpDownload
from ftp_download import FtpDownload
from file_manager import Filemanager
from file_manager import Sector
from url import URL
from downloads import log
from itertools import cycle

class FileDownloader(object):
    ''' scheme http / ftp '''
    _service = {}
    
    def __init__(self):
        ''' initiate the corresponding service according to protocol '''
        self._service['http'] = self._service['https'] = self.load_http
        self._service['ftp'] = self.load_ftp
        self.fileManager = Filemanager()
        self.group = Group()
        self.message = Queue()
        self.total_precess = 4

    def config(self, **config):
        self._config = config
        for key, value in config.items():
            self.__dict__[key] = value

        if not self.path:
            raise ValueError("Path is Missing")

        if not self.urls:
            raise ValueError("Uri is Missing")
        self._urls = [ URL(url) for url in self.urls ]

        self.init_service()

    def init_service(self):
        # if self._url.scheme in self._service:
        self.services  = [ url.scheme in self._service and self._service[url.scheme] \
                               or None for url in self._urls ] 
        self.filestats = [ self.fileManager.infs(self.path, url.last) or \
                               self.fileManager.add(self.path, url.last) \
                               for url in self._urls ]
            # if not self.filestat:
            #     self.filestat = self.fileManager.add(self.path, self._url.last)
            #     log('New file:' + str(self.filestat))
        # else:
        #     raise ValueError('protocol: ' + self.scheme + ' not supported')

    def load_ftp(self):
        return FtpDownload(self._url, self.filestat, self.message)

    def load_http(self):
        return HttpDownload(self._url, self.filestat, self.message)

    def producer(self,sects):
        sect = Sector()
        passed = 0
        for i in range(0,sects):
            id = self.message.get()
            completed_sector = sect.query.filter_by(id = str(id)).first()
            completed_sector.isdownloaded = 1
            completed_sector.update()
#            log(completed_sector)
            complete = True
            partialsize = 0 
            for sector in completed_sector.fname.sectors.all():
                if not sector.isdownloaded: 
                    completed = False
                else:
                    partialsize += sector.size
            completed_sector.fname.partialsize = partialsize
            completed_sector.fname.isdownloaded = complete
            log(completed_sector.fname)
            
        # for green in self.greenthreads:
        #     self.group.add(green)
        #     self.group.join()
        #     passed += 1
        #     if passed > self.total_precess:           
        #         msg = self.message.get()

    def run_url(self):
        if not self.service:
            log(str(self.filestat))
            return False

        dload = self.service()
        if self.filestat.isdownloaded:
            return

        if self.filestat.size == 0:   
            dload.filesize()
            log(str(self.filestat))
            self.filestat.add_sectors()
            self.filestat.writefs('1'*self.filestat.size)
  
        self.greenthreads = []
        self.greenthreads.append(gevent.spawn(self.producer,self.filestat.total_sectors))      
        for sector in self.filestat.sectors.all():
            self.greenthreads.append(gevent.spawn(dload.run, sector))

        gevent.joinall(self.greenthreads)
        return True
            

    def run(self):
        """ run the corresponding service according to protocol """        
        stat = cycle(self.filestats)
        url = cycle(self._urls)
        for service in self.services:
            self.service = service
            self.filestat = next(stat)
            self._url = next(url)
            self.run_url()

import re
# from http_download import HttpDownload
# from ftp_download import FtpDownload
# parse URI

class FileDownloader(object):
     _syntax = re.compile('^(?P<scheme>[a-zA-Z][a-zA-Z0-9\+\-\.]*)://'  # scheme http / ftp
                          + '(?P<path>.+)')
     _service = {}
     def __init__(self):
         ''' initiate the corresponding service according to protocol ''' 
         self._service['http'] = self._service['https'] = self.load_http
         self._service['ftp']  = self.load_ftp


     def config(self, **config):
         self._config = config
         for key,value in config.items():
             self.__dict__[key] = value
         if not self.url:
             raise ValueError, "Uri is Missing"
         
         if not self.path:
             raise ValueError, "Path is Missing"

         m = self._syntax.match(self.url)
         if not m: 
             raise ValueError, 'Invalid URI(' + value + ')'
         self.proto, self.urlpath = m.groups()
         
         if self.proto not in self._service:
             raise ValueError, 'protocol: ' + self.proto  + ' not supported'
         self.service = self._service[self.proto]

     def load_ftp(self):
         pass
     def load_http(self):
         pass
                                     
     def run(self):
         """ run the corresponding service according to protocol """
         self.service()
         

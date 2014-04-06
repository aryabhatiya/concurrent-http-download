import re
from urlparse import urlparse

class URL(object):
    ''' experimenating url parser  '''
    _syntax = re.compile('^(?P<scheme>[a-zA-Z][a-zA-Z0-9\+\-\.]*)://'  # scheme
                         + '(?:(?:(?P<user>[a-zA-Z0-9\-\_\.\!\~\*\'\(\)&=\+\$,;\?\/\%]+)' # user
                         + '(?::(?P<password>[^:@;\?]+))?)@)?' # password
                         + '(?:(?:(?P<host>[^;\?:]*)(?::(?P<port>[\d]+))?))'  # host, port
                         + '(?:/?(?P<paths>[a-zA-Z0-9\-\_\.]+)+)?/?$') 
                         # + '(?:/(?P<params>[^\?]*))?' # parameters
                         # + '(?:\?(?P<headers>.*))?$') # headers

    def __init__(self, value=''):
        # m = URL._syntax.match(value)
        # if not m: raise ValueError('Invalid URI(' + value + ')')
        # self.scheme, self.user, self.password, self.host, self.port, body = m.groups()
        url = urlparse(value)
        self.scheme = url.scheme
        self.host = url.netloc
        self.path = url.path
        self.paths = [nv for nv in url.path.split('/')] if url.path else []
        if len(self.paths):
            self.last = self.paths[-1]
        else:
            self.last = self.url.netloc

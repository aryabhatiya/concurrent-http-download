import re
class URL(object):
    _syntax = re.compile('^(?P<proto>[a-zA-Z][a-zA-Z0-9\+\-\.]*)://'  # scheme
                         + '(?:(?:(?P<user>[a-zA-Z0-9\-\_\.\!\~\*\'\(\)&=\+\$,;\?\/\%]+)' # user
                         + '(?::(?P<password>[^:@;\?]+))?)@)?' # password
                         + '(?:(?:(?P<host>[^;\?:]*)(?::(?P<port>[\d]+))?))'  # host, port
                         + '(?:/(?P<paths>[a-zA-Z0-9\-\_\.]+)+)?/?$') 
                         # + '(?:/(?P<params>[^\?]*))?' # parameters
                         # + '(?:\?(?P<headers>.*))?$') # headers

    def __init__(self, value=''):
        m = URL._syntax.match(value)
        if not m: raise ValueError('Invalid URI(' + value + ')')
        self.proto, self.user, self.password, self.host, self.port, body = m.groups()
        self.paths = [nv for nv in body.split('/')] if body else []
        if len(self.paths):
            self.last = self.paths[:-1]
        elif self.port:
            self.last = self.host + ":" + self.port
        else:
            self.last = self.host

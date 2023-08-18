from requests.adapters import TimeoutSauce
from requests.auth import AuthBase

from Config import Config


class TestTimeout(TimeoutSauce):
    """Attaches Timers to the given Request object"""

    def __init__(self, **kwargs):
        config = Config().host
        connect = kwargs.get('connect') if kwargs.get('connect') else config.wait_conn
        read = kwargs.get('read') if kwargs.get('read') else config.wait_read
        super(TestTimeout, self).__init__(connect=connect, read=read)


class ApiKey(AuthBase):
    """Attaches HTTP ApiKey Authentication to the given Request object"""

    def __init__(self, apikey):
        """- setup any auth-related data"""
        self.apikey = apikey

    def __call__(self, r):
        """- modify and return the request"""
        r.headers['ApiKey'] = self.apikey
        return r

#!/usr/bin/env python

"""
Script to check the status of a Netgear AirCard router.
"""

try:
    import requests
    from bs4 import BeautifulSoup
    ext_deps = True
except ImportError:
    ext_deps = False
import sys
import json
import urllib
import random
import time

class AirCard(object):
    def __init__(self, host="netgear.aircard", password='password'):
        self.timeout = 3
        self.host = host
        self.password = password
        self.base_url = 'http://{}/'.format(self.host)
        self.calls = 0
        self.start_session()

    def start_session(self):
        url = urllib.parse.urljoin(self.base_url, '/index.html')
        try:
            r = requests.get(url, timeout=self.timeout)
        except requests.exceptions.ConnectTimeout:
            raise AirCardException()
        self.calls += 1
        # If you try to get a URL without providing a session ID, you will be
        # redirected twice and the first redirect sets the cookie. Use the
        # requests history to get the cookie from that first request:
        self.cookies = r.history[0].cookies

    def login(self):
        model = self.get_model()
        login_data = {
          'token': model['session']['secToken'],
          'session.password': self.password,
          'ok_redirect': '/index.html',
          'err_redirect': '/index.html'
        }
        r = self.post('/Forms/config', data=login_data)

    def get_model(self):
        r = self.get('/api/model.json', params=dict(internalapi=1, x=random.randint(0,99999)))
        #r = self.get('/api/model.json')
        return json.loads(r.text)

    def post(self, url, *args, **kwargs):
        self.calls += 1
        url = urllib.parse.urljoin(self.base_url, url)
        kwargs.update({'timeout': self.timeout, 'cookies': self.cookies})
        return requests.post(url, *args, **kwargs)

    def get(self, url, *args, **kwargs):
        self.calls += 1
        url = urllib.parse.urljoin(self.base_url, url)
        kwargs.update({'timeout': self.timeout, 'cookies': self.cookies})
        return requests.get(url, *args, **kwargs)

class AirCardException(Exception):
    pass

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-login', '-n', action='store_true', help="Don't log in to the router")
    parser.add_argument('--password', '-p', default='password', help='Admin Password.')
    parser.add_argument('host', default='netgear.aircard', nargs='?', help='Host name/IP Address of the AirCard')

    if not ext_deps: parser.error("Missing at least one of the python modules 'requests' or 'beautifulsoup4'.")

    args = parser.parse_args()

    try:
        ac = AirCard(host=args.host, password=args.password)
    except AirCardException:
        sys.stderr.write("Couldn't connect to the IP {}.\n".format(args.host))
        sys.exit(1)
    if not args.no_login: ac.login()
    #start = time.perf_counter()
    print(json.dumps(ac.get_model(), sort_keys=True, indent=2, separators=(',', ': ')))
    #sys.stderr.write('time to call get_model(): {}'.format(time.perf_counter() - start))

if __name__ == "__main__":
    main()

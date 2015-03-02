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
import json
from pprint import pprint
import urllib

class AirCard(object):
    def __init__(self, ip="192.168.170.1", password='webadmin'):
        self.ip = ip
        self.password = password
        self.base_url = 'http://{}/'.format(self.ip)
        self.start_session()

    def start_session(self):
        r = requests.get(urllib.parse.urljoin(self.base_url, '/index.html'))
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

    def detailed_info(self):
        idx_page = BeautifulSoup(self.get('/index.html').text)
        try:
            return idx_page.select('textarea#about_text')[0].text
        except IndexError:
            return None

    def get_model(self):
        r = self.get('/api/model.json')
        return json.loads(r.text)

    def post(self, url, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url)
        kwargs.update({'cookies': self.cookies})
        return requests.post(url, *args, **kwargs)

    def get(self, url, *args, **kwargs):
        url = urllib.parse.urljoin(self.base_url, url)
        kwargs.update({'cookies': self.cookies})
        return requests.get(url, *args, **kwargs)

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ip', default='192.168.170.1', help='IP Address of the AirCard')
    parser.add_argument('--password', '-p', default='webadmin', help='Admin Password.')
    parser.add_argument('--no-login', '-n', action='store_true', help="Don't log in to the router")

    if not ext_deps: parser.error("Missing at least one of the python modules 'requests' or 'beautifulsoup4'.")

    args = parser.parse_args()

    ac = AirCard(ip=args.ip, password=args.password)
    if not args.no_login: ac.login()
    print(ac.detailed_info())
    pprint(ac.get_model())

if __name__ == "__main__":
    main()

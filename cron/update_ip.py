#!/usr/bin/python
import sys
sys.path.append('../')

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

import logging
import os

from lists.tools import ParseYandexInternetometr

PROJECT_LOG_DIR = '/var/log/tdd'
REPORT_LOG_FILE = os.path.join(PROJECT_LOG_DIR, 'ip_updater.log')
logger = logging.getLogger('ip_updater')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(name)s : %(message)s',
                              datefmt='%Y.%m.%d %H:%M:%S')
handler = logging.FileHandler(REPORT_LOG_FILE)
handler.setFormatter(formatter)
logger.addHandler(handler)

    
TOKEN = '8ec754e207797feeec889958f48757fb676e278a1641d60876c8e1e1'
DOMAIN = 'bernardito.tk'
RECORD_ID = 27769469
RECORD_ID_WWW = 27769470

# class ParseYandexInternetometr(HTMLParser):
    # def __init__(self):
        # HTMLParser.__init__(self)
        # self.tricky_flag = 0
        # self.ip = ''
        # connection = urlopen('http://yandex.ru/internet')
        # page = connection.read().decode('utf-8')
        # self.feed(page)
    # def handle_starttag(self, tag, attrs):
        # tag_class = dict(attrs).get('class')
        # if tag_class and tag_class == 'data__item data__item_type_ip':
            # self.tricky_flag = 2
    # def handle_endtag(self, tag):
        # if self.tricky_flag:
            # self.tricky_flag -= 1
    # def handle_data(self, data):
        # if self.tricky_flag == 1:
            # self.ip = data


def reconfigure_yandex_dns(new_ip):
    change_ip_req = (
        "https://pddimp.yandex.ru/nsapi/edit_a_record.xml?token=%s&domain=%s&record_id=%s&content=%s" % 
        (TOKEN, DOMAIN, RECORD_ID, new_ip)
    )
    urlopen(change_ip_req)
    change_ip_req = (
        "https://pddimp.yandex.ru/nsapi/edit_a_record.xml?token=%s&domain=%s&subdomain=www&record_id=%s&content=%s" % 
        (TOKEN, DOMAIN, RECORD_ID_WWW, new_ip)
    )
    ans = urlopen(change_ip_req)
            
if __name__ == '__main__':
    parser = ParseYandexInternetometr()
    reconfigure_yandex_dns(parser.ip)
    logger.info('IP changed')


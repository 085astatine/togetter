# -*- coding: utf-8 -*-

import datetime
import logging
import time
import requests
import lxml.etree
from .togetter_data import TogetterData
from .togetter_page import TogetterPage

class TogetterPageParser(object):
    def __init__(self, page_id, session= None, logger= None):
        # logger設定
        if logger is None:
            logger = logging.getLogger(__name__)
        # get Initial Page
        self._initial_page = TogetterPage(
                    page_id,
                    page= 1,
                    session= session,
                    logger= logger)
        # Page List
        self._page_list = None
        # Tweet List
        self._tweet_list = None
    
    def load_page(self, wait_time= 1.0):
        if self._page_list is None:
            self._page_list = []
            self._page_list.append(self._initial_page)
            while True:
                next_page = self._page_list[-1].next_page()
                if next_page is None:
                    break
                self._page_list.append(next_page)
                time.sleep(wait_time)
    
    def get_tweet_list(self):
        if self._tweet_list is None:
            if self._page_list is None:
                self.load_page()
            self._tweet_list = []
            for page in self._page_list:
                self._tweet_list.extend(page.get_tweet_list())
        return self._tweet_list
    
    def parse(self):
        # root
        root = lxml.etree.Element('togetter')
        etree = lxml.etree.ElementTree(root)
        # title
        title = lxml.etree.SubElement(root, 'title')
        title.text = self._initial_page.title
        # id
        page_id = lxml.etree.SubElement(root, 'id')
        page_id.text = str(self._initial_page.id)
        # URL
        url = lxml.etree.SubElement(root, 'URL')
        url.text = self._initial_page.url
        # AccessTime
        now_time = datetime.datetime.today()
        access_time = lxml.etree.SubElement(root, 'access_time')
        access_time.text = str(now_time)
        access_time.set('timestamp', str(now_time.timestamp()))
        # tweet data
        tweet_list = lxml.etree.SubElement(root, 'tweet_list')
        for i, tweet in enumerate(self.get_tweet_list()):
            tweet_data = tweet.to_element()
            tweet_data.set('index', str(i))
            tweet_list.append(tweet_data)
        return TogetterData(etree)

def to_xml(id, xml_path, logger= None):
    page = TogetterPage(id, logger= logger)
    page.parse().save_as_xml(xml_path)

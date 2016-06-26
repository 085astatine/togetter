# -*- coding: utf-8 -*-

import datetime
import logging
import time
import requests
import lxml.etree
from .tweet_data import TweetData
from .togetter_data import TogetterData
from .togetter_page_base import TogetterPage
from .xml_tools import save_as_xml

class TogetterPageParser(TogetterPage):
    def __init__(self, id, page= 1, session= None, logger= None):
        # logger設定
        if logger is None:
            logger = logging.getLogger(__name__)
        TogetterPage.__init__(
                    self,
                    id,
                    page= 1,
                    session= session,
                    logger= logger)
        # TweetsList
        self._tweet_list = None
        # 全pageのList
        self._page_list = []
        # データ読み込み済みか否か
        self._is_loaded = False
    
    def load_tweets(self):
        if not self._is_loaded:
            next_page = self.next_page()
            while not next_page is None:
                self._page_list.append(next_page)
                time.sleep(0.2)
                next_page = self._page_list[-1].next_page()
            self._is_loaded = True
    
    def get_tweet_list(self):
        if self._tweet_list is None:
            if not self._is_loaded:
                self.load_tweets()
            tweet_list = []
            tweet_list.extend(TogetterPage.get_tweet_list(self))
            for page in self._page_list:
                tweet_list.extend(page.get_tweet_list())
            self._tweet_list = tweet_list
        return self._tweet_list
    
    def to_element_tree(self):
        # root
        root = lxml.etree.Element('togetter')
        etree = lxml.etree.ElementTree(root)
        # title
        title = lxml.etree.SubElement(root, 'title')
        title.text = self.title
        # id
        page_id = lxml.etree.SubElement(root, 'id')
        page_id.text = str(self.id)
        # URL
        url = lxml.etree.SubElement(root, 'URL')
        url.text = self.url
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
        return etree
    
    def to_togetter_data(self):
        return TogetterData(self.to_element_tree())
    
    def save_as_xml(self, xml_path, pretty_print= True):
        save_as_xml(self.to_element_tree(), xml_path, pretty_print)

def to_xml(id, xml_path, logger= None):
    page = TogetterPage(id, logger= logger)
    page.save_as_xml(xml_path)

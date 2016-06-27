# -*- coding: utf-8 -*-

import datetime
import logging
import time
import pathlib
from typing import List, Optional, Union
import requests
import lxml.etree
from .togetter_data import TogetterData
from .togetter_page import TogetterPage
from .tweet_data import TweetData

class TogetterPageParser(object):
    def __init__(
                self,
                page_id: int,
                session: requests.sessions.Session = None,
                logger: logging.Logger = None) -> None:
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
        self._page_list = None # type: Optional[List[TogetterPage]]
        # Tweet List
        self._tweet_list = None # type: Optional[List[TweetData]]
    
    def load_page(self, wait_time: float= 1.0) -> List[TogetterPage]:
        if self._page_list is None:
            self._page_list = []
            self._page_list.append(self._initial_page)
            while True:
                next_page = self._page_list[-1].next_page()
                if next_page is None:
                    break
                self._page_list.append(next_page)
                time.sleep(wait_time)
    
    def get_tweet_list(self) -> List[TweetData]:
        if self._tweet_list is None:
            if self._page_list is None:
                self.load_page()
            self._tweet_list = []
            for page in self._page_list:
                self._tweet_list.extend(page.get_tweet_list())
        return self._tweet_list
    
    def parse(self) -> TogetterData:
        # root
        root = lxml.etree.Element('togetter')
        etree = lxml.etree.ElementTree(root)
        # title
        title = lxml.etree.SubElement(root, 'title')
        title.text = self._initial_page.title
        # id
        page_id = lxml.etree.SubElement(root, 'id')
        page_id.text = str(self._initial_page.page_id)
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

def to_xml(page_id: int,
           xml_path: Union[str, pathlib.Path],
           logger: logging.Logger = None):
    parser = TogetterPageParser(page_id, logger= logger)
    parser.parse().save_as_xml(xml_path)

# -*- coding: utf-8 -*-

import datetime
import logging
import time
import requests
import lxml.etree
from .tweet_data import TweetData
from .togetter_data import TogetterData
from .togetter_page_base import _TogetterPage, parse_tweet_data
from .xml_tools import save_as_xml

class TogetterPage(_TogetterPage):
    def __init__(self, id, page= 1, session= None, logger= None):
        # logger設定
        if logger is None:
            logger = logging.getLogger(__name__)
        _TogetterPage.__init__(self, id,
                               page= 1,
                               session= session,
                               logger= logger)
        # 「残りを読む」で得られるTweet
        self._more_tweets_data = None
        # TweetsList
        self._tweet_list = None
        # 全pageのList
        self._page_list = []
        # データ読み込み済みか否か
        self._is_loaded = False
    
    def load_tweets(self):
        if not self._is_loaded:
            if self.exists_more_tweets() and (self._more_tweets_data is None):
                self._more_tweets_data = get_more_tweets(self)
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
            tweet_list.extend(_TogetterPage.get_tweet_list(self))
            if not self._more_tweets_data is None:
                tweet_list.extend(parse_tweet_data(self._more_tweets_data))
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

def get_more_tweets(self):
    url = r'http://togetter.com/api/moreTweets/{0}'.format(self._id)
    data = {'page': 1,
            'csrf_token': self.csrf_token}
    response = self._session.post(url, data= data)
    tweet_data = lxml.html.fromstring(response.content.decode('utf-8'))
    # logger出力
    self._logger.info('getMoreTweets')
    self._logger.info('  URL: {0}'.format(response.url))
    self._logger.debug('  csrfToken : {0}'.format(self.csrf_token))
    self._logger.debug('  csrfSecret: {0}'.format(self.csrf_secret))
    return tweet_data

def to_xml(id, xml_path, logger= None):
    page = TogetterPage(id, logger= logger)
    page.save_as_xml(xml_path)

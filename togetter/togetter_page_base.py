# -*- coding: utf-8 -*-

import datetime
import logging
import time
import requests
import lxml.etree
from .tweet_data import _TweetData
from .webpage import WebPage

class _TogetterPage(WebPage):
    def __init__(self, id, page, session, logger= None):
        # logger設定
        if logger is None:
            logger = logging.getLogger(__name__)
        # 値設定
        self._id = id
        self._page = page
        # 接続設定
        self._session = session
        url = r'http://togetter.com/li/{0}'.format(id)
        params = {'page': page} if page != 1 else {}
        WebPage.__init__(self, url,
                         logger= logger,
                         params= params,
                         session= self._session)
        # logger出力
        self._logger.info('{0}'.format(self.__class__.__name__))
        self._logger.info('  title: {0}'.format(self.title))
        self._logger.info('  URL  : {0}'.format(self.url))
    
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        xpath = r'head/meta[@property="og:title"]'
        result = self.html.xpath(xpath)
        if len(result) == 1:
            return result[0].get('content')
        else:
            return None
    
    @property
    def csrf_token(self):
        xpath = 'head/meta[@name="csrf_token"]'
        result = self.html.xpath(xpath)
        if len(result) == 1:
            return result[0].get('content')
        else:
            return None
    
    @property
    def csrf_secret(self):
        return self._session.cookies.get('csrf_secret', None)
    
    @property
    def creator(self):
        xpath = r'head/meta[@name="twitter:creator"]'
        data = self.html.xpath(xpath)
        if len(data) == 1:
            return data[0].get('content')
        else:
            return None
    
    def getTweetList(self):
        return getTweetData(self.html)
    
    def existsMoreTweets(self):
        xpath = r'body//div[@class="more_tweet_box"]'
        return len(self.html.xpath(xpath)) == 1
    
    def nextPage(self):
        # 次のページが存在するか確認する
        xpath = r'head/link[@rel="next"]'
        is_exists = (len(self.html.xpath(xpath)) == 1)
        if is_exists:
            return _TogetterPage(self.id,
                                 page= self._page + 1,
                                 session= self._session,
                                 logger= self._logger)
        else:
            return None
    
    def prevPage(self):
        # 前のページが存在するか否か確認する
        xpath = r'head/link[@rel="prev"]'
        is_exists = (len(self.html.xpath(xpath)) == 1)
        if is_exists:
            return _TogetterPage(self.id,
                                 page= self._page - 1,
                                 session= self._session,
                                 logger= self._logger)
        else:
            return None

def getTweetData(html_data):
    xpath = r'//body//ul[./li[@class="list_item"]]'
    tweet_data = html_data.xpath(xpath)
    if len(tweet_data) == 1:
        return parseTweetData(tweet_data[0])
    else:
        return []

def parseTweetData(tweet_data):
    xpath = r'//li[@class="list_item"]/div[@class="list_box type_tweet"]'
    data_list = tweet_data.xpath(xpath)
    return [_TweetData(data) for data in data_list]

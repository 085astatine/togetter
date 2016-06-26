# -*- coding: utf-8 -*-

import datetime
import logging
import time
import requests
import lxml.etree
from .tweet_data import TweetDataParser
from .webpage import WebPage

class TogetterPage(WebPage):
    def __init__(self, id, page, session= None, logger= None):
        # logger設定
        if logger is None:
            logger = logging.getLogger(__name__)
        # 値設定
        self._id = id
        self._page_number = page
        self._tweet_list = None
        # 接続設定
        url = r'http://togetter.com/li/{0}'.format(id)
        params = {'page': page} if page != 1 else {}
        WebPage.__init__(self, url,
                         logger= logger,
                         params= params,
                         session= session)
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
        return self.session.cookies.get('csrf_secret', None)
    
    @property
    def creator(self):
        xpath = r'head/meta[@name="twitter:creator"]'
        data = self.html.xpath(xpath)
        if len(data) == 1:
            return data[0].get('content')
        else:
            return None
    
    def get_tweet_list(self):
        if self._tweet_list is None:
            self._tweet_list = []
            # Tweet
            xpath = r'//body//ul[./li[@class="list_item"]]'
            tweet_data = self.html.xpath(xpath)
            if len(tweet_data) == 1:
                self._tweet_list.extend(
                            _parse_tweet_data(tweet_data[0]))
            # More Tweets
            if self.more_tweets_exists():
                self._tweet_list.extend(
                            _parse_tweet_data(_get_more_tweets(self)))
        return self._tweet_list
    
    def more_tweets_exists(self):
        xpath = r'body//div[@class="more_tweet_box"]'
        return len(self.html.xpath(xpath)) == 1
    
    def next_page(self):
        # 次のページが存在するか確認する
        xpath = r'head/link[@rel="next"]'
        if (len(self.html.xpath(xpath)) == 1):
            return TogetterPage(
                        self.id,
                        page= self._page_number + 1,
                        session= self.session,
                        logger= self._logger)
        else:
            return None
    
    def prev_page(self):
        # 前のページが存在するか否か確認する
        xpath = r'head/link[@rel="prev"]'
        if (len(self.html.xpath(xpath)) == 1):
            return TogetterPage(
                        self.id,
                        page= self._page_number - 1,
                        session= self.session,
                        logger= self._logger)
        else:
            return None

def _get_more_tweets(self):
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

def _parse_tweet_data(tweet_etree):
    xpath = r'//li[@class="list_item"]/div[@class="list_box type_tweet"]'
    data_list = tweet_etree.xpath(xpath)
    return [TweetDataParser(data).parse() for data in data_list]

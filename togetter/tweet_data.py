# -*- coding: utf-8 -*-

import datetime
from collections import OrderedDict
import lxml.etree

class _TweetData(object):
    def __init__(self, element):
        self._element = element
    
    @property
    def element(self):
        return self._element
    
    @property
    def tweet(self):
        xpath = r'.//div[@class= "tweet emj"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return ''.join(result[0].itertext())
        else:
            return None
    
    @property
    def user_name(self):
        xpath = r'.//a[@class= "user_link"]/strong'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].text
        else:
            return ''
    
    @property
    def user_id(self):
        xpath = r'.//a[@class= "user_link"]/span[@class= "status_name"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].text
        else:
            return None
    
    @property
    def user_link(self):
        xpath = r'.//a[@class= "user_link"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('href')
        else:
            return None
    
    @property
    def tweet_link(self):
        xpath = r'.//a[@class= "timestamp"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('href')
        else:
            return None
    
    @property
    def timestamp(self):
        xpath = r'.//a[@class= "timestamp"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return int(result[0].get('data-timestamp'))
        else:
            return None
    
    @property
    def datetime(self):
        timestamp = self.timestamp
        if not timestamp is None:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return None
    
    def toElement(self):
        root = lxml.etree.Element('tweet_data')
        # user
        user_attribute = OrderedDict([
                    ('id', self.user_id),
                    ('name', self.user_name),
                    ('link', self.user_link),
                    ])
        user = lxml.etree.SubElement(root, 'user', attrib= user_attribute)
        # link
        link = lxml.etree.SubElement(root, 'link')
        link.text = self.tweet_link
        # tweet
        tweet = lxml.etree.SubElement(root, 'tweet')
        tweet.text = self.tweet
        # datetime
        date = lxml.etree.SubElement(root, 'datetime')
        date.text = str(self.datetime)
        date.set('timestamp', str(self.timestamp))
        return root

class TweetData(_TweetData):
    def __init__(self, element):
        _TweetData.__init__(self, element)
    
    @property
    def tweet(self):
        xpath = r'./tweet'
        data = self.element.xpath('./tweet')
        if len(data) == 1:
            return data[0].text
        else:
            None
    
    @property
    def user_name(self):
        xpath = r'./user'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('name')
        else:
            return None
    
    @property
    def user_id(self):
        xpath = r'./user'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('id')
        else:
            return None
    
    @property
    def user_link(self):
        xpath = r'./user'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('link')
        else:
            return None
    
    @property
    def tweet_link(self):
        xpath = r'./link'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].text
        else:
            return None
    
    @property
    def timestamp(self):
        xpath = r'./datetime'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return int(result[0].get('timestamp'))
        else:
            return None

# -*- coding: utf-8 -*-

import datetime
from collections import OrderedDict
from typing import Optional, Union
import lxml.etree

class TweetData(object):
    def __init__(self, element: lxml.etree._Element) -> None:
        self._element = element
    
    @property
    def element(self) -> lxml.etree._Element:
        return self._element
    
    @property
    def tweet(self) -> Optional[str]:
        xpath = r'./tweet'
        data = self.element.xpath('./tweet')
        if len(data) == 1:
            return data[0].text
        else:
            None
    
    @property
    def user_name(self) -> Optional[str]:
        xpath = r'./user'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('name')
        else:
            return None
    
    @property
    def user_id(self) -> Optional[str]:
        xpath = r'./user'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('id')
        else:
            return None
    
    @property
    def user_link(self) -> Optional[str]:
        xpath = r'./user'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('link')
        else:
            return None
    
    @property
    def tweet_link(self) -> Optional[str]:
        xpath = r'./link'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].text
        else:
            return None
    
    @property
    def timestamp(self) -> Optional[int]:
        xpath = r'./datetime'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return int(result[0].get('timestamp'))
        else:
            return None
    
    @property
    def datetime(self) -> Optional[datetime.datetime]:
        timestamp = self.timestamp
        if not timestamp is None:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return None
    
    def to_element(self) -> lxml.etree._Element:
        return _to_element(self)

class TweetDataParser(object):
    def __init__(self, element: lxml.etree._Element) -> None:
        self._element = element
    
    @property
    def element(self) -> lxml.etree._Element:
        return self._element
    
    @property
    def tweet(self) -> Optional[str]:
        xpath = r'.//div[@class= "tweet emj"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return ''.join(result[0].itertext())
        else:
            return None
    
    @property
    def user_name(self) -> Optional[str]:
        xpath = r'.//a[@class= "user_link"]/strong'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].text
        else:
            return ''
    
    @property
    def user_id(self) -> Optional[str]:
        xpath = r'.//a[@class= "user_link"]/span[@class= "status_name"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].text
        else:
            return None
    
    @property
    def user_link(self) -> Optional[str]:
        xpath = r'.//a[@class= "user_link"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('href')
        else:
            return None
    
    @property
    def tweet_link(self) -> Optional[str]:
        xpath = r'.//a[@class= "timestamp"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return result[0].get('href')
        else:
            return None
    
    @property
    def timestamp(self) -> Optional[int]:
        xpath = r'.//a[@class= "timestamp"]'
        result = self.element.xpath(xpath)
        if len(result) == 1:
            return int(result[0].get('data-timestamp'))
        else:
            return None
    
    @property
    def datetime(self) -> Optional[datetime.datetime]:
        timestamp = self.timestamp
        if not timestamp is None:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return None
    
    def to_element(self) -> lxml.etree._Element:
        return _to_element(self)
    
    def parse(self) -> TweetData:
        return TweetData(self.to_element())

def _to_element(
            data: Union[TweetDataParser, TweetData]) -> lxml.etree._Element:
    root = lxml.etree.Element('tweet_data')
    # user
    user_attribute = OrderedDict([
                ('id', data.user_id),
                ('name', data.user_name),
                ('link', data.user_link),
                ])
    user = lxml.etree.SubElement(root, 'user', attrib= user_attribute)
    # link
    link = lxml.etree.SubElement(root, 'link')
    link.text = data.tweet_link
    # tweet
    tweet = lxml.etree.SubElement(root, 'tweet')
    tweet.text = data.tweet
    # datetime
    date = lxml.etree.SubElement(root, 'datetime')
    date.text = str(data.datetime)
    date.set('timestamp', str(data.timestamp))
    return root

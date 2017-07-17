# -*- coding: utf-8 -*-


import datetime
from collections import OrderedDict
from typing import Optional, Union
import lxml.etree


class TweetData(object):
    def __init__(self,
                 tweet: str,
                 tweet_link: str,
                 user_id: str,
                 user_name: str,
                 user_link: str,
                 timestamp: int) -> None:
        """Initialize

        Args:
        element (lxml.etree._Element):
            Element representing the tweet"""
        self._tweet = tweet
        self._tweet_link = tweet_link
        self._user_id = user_id
        self._user_name = user_name
        self._user_link = user_link
        self._timestamp = timestamp

    @property
    def tweet(self) -> str:
        return self._tweet

    @property
    def tweet_link(self) -> Optional[str]:
        return self._tweet_link

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def user_name(self) -> str:
        return self._user_name

    @property
    def user_link(self) -> str:
        return self._user_link

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._timestamp)

    def to_element(self) -> lxml.etree._Element:
        """Create etree element"""
        return _to_element(self)

    @staticmethod
    def from_element(etree: lxml.etree._Element):
        tweet = etree.xpath('./tweet')[0].text
        tweet_link = etree.xpath('./link')[0].text
        user_id = etree.xpath('./user')[0].get('id')
        user_name = etree.xpath('./user')[0].get('name')
        user_link = etree.xpath('./user')[0].get('link')
        timestamp = int(etree.xpath('./datetime')[0].get('timestamp'))
        return TweetData(tweet,
                         tweet_link,
                         user_id,
                         user_name,
                         user_link,
                         timestamp)


class TweetDataParser(object):
    """Initialize

    Args:
    element (lxml.etree._Element):
        HTML element representing the tweet"""
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
        if timestamp is not None:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return None

    def to_element(self) -> lxml.etree._Element:
        """Create etree element for TweetData class"""
        return _to_element(self)

    def parse(self) -> TweetData:
        """Create TweetData class"""
        return TweetData(self.tweet,
                         self.tweet_link,
                         self.user_id,
                         self.user_name,
                         self.user_link,
                         self.timestamp)


def _to_element(
            data: Union[TweetDataParser, TweetData]) -> lxml.etree._Element:
    root = lxml.etree.Element('tweet_data')
    # user
    user_attribute = OrderedDict([
                ('id', data.user_id),
                ('name', data.user_name),
                ('link', data.user_link),
                ])
    user = lxml.etree.SubElement(root, 'user', attrib=user_attribute)
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

# -*- coding: utf-8 -*-


import datetime
from collections import OrderedDict
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
    def tweet_link(self) -> str:
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
        root = lxml.etree.Element('tweet_data')
        # user
        user_attribute = OrderedDict([
                    ('id', self.user_id),
                    ('name', self.user_name),
                    ('link', self.user_link),
                    ])
        user = lxml.etree.SubElement(root, 'user', attrib=user_attribute)
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

    @staticmethod
    def from_element(etree: lxml.etree._Element) -> 'TweetData':
        assert etree.tag == 'tweet_data'
        kwargs = {}
        kwargs['tweet'] = etree.find('tweet').text
        kwargs['tweet_link'] = etree.find('link').text
        kwargs['user_id'] = etree.find('user').get('id')
        kwargs['user_name'] = etree.find('user').get('name')
        kwargs['user_link'] = etree.find('user').get('link')
        kwargs['timestamp'] = int(etree.find('datetime').get('timestamp'))
        return TweetData(**kwargs)


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
    def tweet(self) -> str:
        xpath = r'.//div[@class= "tweet emj"]'
        result = self.element.xpath(xpath)
        assert len(result) == 1
        return ''.join(result[0].itertext())

    @property
    def user_name(self) -> str:
        xpath = r'.//a[@class= "user_link"]/strong'
        result = self.element.xpath(xpath)
        assert len(result) == 1
        return result[0].text

    @property
    def user_id(self) -> str:
        xpath = r'.//a[@class= "user_link"]/span[@class= "status_name"]'
        result = self.element.xpath(xpath)
        assert len(result) == 1
        return result[0].text

    @property
    def user_link(self) -> str:
        xpath = r'.//a[@class= "user_link"]'
        result = self.element.xpath(xpath)
        assert len(result) == 1
        return result[0].get('href')

    @property
    def tweet_link(self) -> str:
        xpath = r'.//a[@class= "timestamp"]'
        result = self.element.xpath(xpath)
        assert len(result) == 1
        return result[0].get('href')

    @property
    def timestamp(self) -> int:
        xpath = r'.//a[@class= "timestamp"]'
        result = self.element.xpath(xpath)
        assert len(result) == 1
        return int(result[0].get('data-timestamp'))

    @property
    def datetime(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.timestamp)

    def parse(self) -> TweetData:
        """Create TweetData class"""
        kwargs = {}
        kwargs['tweet'] = self.tweet
        kwargs['tweet_link'] = self.tweet_link
        kwargs['user_id'] = self.user_id
        kwargs['user_name'] = self.user_name
        kwargs['user_link'] = self.user_link
        kwargs['timestamp'] = self.timestamp
        return TweetData(**kwargs)

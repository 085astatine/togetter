# -*- coding: utf-8 -*-

import copy
import datetime
import pathlib
from typing import List, Union
import lxml.etree
from .tweet_data import Tweet
from .xml_tools import save_as_xml as _save_as_xml


class TogetterData(object):
    def __init__(self,
                 title: str,
                 page_id: int,
                 url: str,
                 access_timestamp: float,
                 tweet_list: List[Tweet]) -> None:
        """Initialize"""
        self._title = title
        self._page_id = page_id
        self._url = url
        self._access_timestamp = access_timestamp
        self._tweet_list = tweet_list

    @property
    def title(self) -> str:
        return self._title

    @property
    def page_id(self) -> int:
        return self._page_id

    @property
    def url(self) -> str:
        return self._url

    @property
    def access_timestamp(self) -> float:
        return self._access_timestamp

    @property
    def access_time(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self.access_timestamp)

    @property
    def tweet_list(self) -> List[Tweet]:
        return self._tweet_list

    def to_etree(self) -> lxml.etree._ElementTree:
        # root
        root = lxml.etree.Element('togetter')
        etree = lxml.etree.ElementTree(root)
        # title
        title = lxml.etree.SubElement(root, 'title')
        title.text = self.title
        # id
        page_id = lxml.etree.SubElement(root, 'id')
        page_id.text = str(self.page_id)
        # URL
        url = lxml.etree.SubElement(root, 'URL')
        url.text = self.url
        # AccessTime
        access_time = lxml.etree.SubElement(root, 'access_time')
        access_time.text = str(self.access_time)
        access_time.set('timestamp', str(self.access_timestamp))
        # tweet data
        tweet_list = lxml.etree.SubElement(root, 'tweet_list')
        for i, tweet in enumerate(self.tweet_list):
            tweet_data = tweet.to_element()
            tweet_data.set('index', str(i))
            tweet_list.append(tweet_data)
        return root

    @staticmethod
    def from_etree(etree: lxml.etree._ElementTree) -> 'TogetterData':
        assert etree.tag == 'togetter'
        kwargs = {}
        kwargs['title'] = etree.find('title').text
        kwargs['page_id'] = etree.find('id').text
        kwargs['url'] = etree.find('URL').text
        kwargs['access_timestamp'] = float(
                    etree.find('access_time').get('timestamp'))
        kwargs['tweet_list'] = [Tweet.from_element(element)
                                for element
                                in etree.find('tweet_list').iterchildren()]
        return TogetterData(**kwargs)

    def save_as_xml(self,
                    filepath: Union[str, pathlib.Path],
                    pretty_print: bool = True) -> None:
        """Save TogetterData in the file as XML

        Args:
        filepath (str, pathlib.Path): The path of file to be output as XML
        pretty_print (bool) optional:
            Whether or not to output in pretty print
            Defaults to True.
        """
        _save_as_xml(self.to_etree(), filepath, pretty_print)

    @classmethod
    def load_xml(cls, filepath: Union[str, pathlib.Path]) -> "TogetterData":
        """load TogetterData from XML file

        Args:
        filepath (str, pathlib.Path):
            The path of the XML file that represents TogetterData

        Returns:
            TogetterData: that has been generated from the XML file"""
        if not isinstance(filepath, pathlib.Path):
            filepath = pathlib.Path(filepath)
        xml_parser = lxml.etree.XMLParser(remove_blank_text=True)
        etree = lxml.etree.XML(
                    filepath.open(encoding='utf-8').detach().read(),
                    parser=xml_parser)
        return TogetterData.from_etree(etree)

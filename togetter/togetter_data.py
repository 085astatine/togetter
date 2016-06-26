# -*- coding: utf-8 -*-

import copy
import datetime
import pathlib
from typing import List, Optional, Union
import lxml.etree
from .tweet_data import TweetData
from .xml_tools import save_as_xml as _save_as_xml

class TogetterData(object):
    def __init__(self, element_tree: lxml.etree._Element) -> None:
        """Initialize

        Args:
        element_tree (lxml.etree._Element):
            the etree element representing TogetterData"""
        self._etree = element_tree
        self._tweet_list = [
                    TweetData(data) for data
                    in self._etree.xpath(r'/togetter/tweet_list/tweet_data')]
    
    @property
    def etree(self) -> lxml.etree._Element:
        return self._etree
    
    @property
    def title(self) -> Optional[str]:
        xpath = r'/togetter/title'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        else:
            return None
    
    @property
    def id(self) -> Optional[int]:
        xpath = r'/togetter/id'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        else:
            return None
    
    @property
    def url(self) -> Optional[str]:
        xpath = r'/togetter/URL'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        else:
            return None
    
    @property
    def access_timestamp(self) -> Optional[float]:
        xpath = r'/togetter/access_time'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return float(data[0].get('timestamp'))
        else:
            return None
    
    @property
    def access_time(self) -> Optional[datetime.datetime]:
        timestamp = self.access_timestamp
        if not timestamp is None:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return None
    
    @property
    def tweet_list(self) -> List[TweetData]:
        return self._tweet_list
    
    def copied(self) -> 'TogetterData':
        """Returns deep copied self"""
        return TogetterData(copy.deepcopy(self.etree))
    
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
        _save_as_xml(self.etree, filepath, pretty_print)

def load_xml(filepath: Union[str, pathlib.Path]) -> TogetterData:
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
                filepath.open(encoding= 'utf-8').detach().read(),
                parser= xml_parser)
    return TogetterData(etree)

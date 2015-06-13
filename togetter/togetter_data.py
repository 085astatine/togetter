# -*- coding: utf-8 -*-

import copy
import datetime
import pathlib
import lxml.etree
from .tweet_data import TweetData
from .xml_tools import saveXML

class TogetterData(object):
    def __init__(self, element_tree):
        self._etree = element_tree
        self._tweet_list = [
                    TweetData(data) for data
                    in self._etree.xpath(r'/togetter/tweet_list/tweet_data')]
    
    @property
    def etree(self):
        return self._etree
    
    @property
    def title(self):
        xpath = r'/togetter/title'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        else:
            return None
    
    @property
    def id(self):
        xpath = r'/togetter/id'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        else:
            return None
    
    @property
    def url(self):
        xpath = r'/togetter/URL'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        else:
            return None
    
    @property
    def access_timestamp(self):
        xpath = r'/togetter/access_time'
        data = self.etree.xpath(xpath)
        if len(data) == 1:
            return float(data[0].get('timestamp'))
        else:
            return None
    
    @property
    def access_time(self):
        timestamp = self.access_timestamp
        if not timestamp is None:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return None
    
    @property
    def tweet_list(self):
        return self._tweet_list
    
    def copy(self):
        return TogetterData(copy.deepcopy(self.etree))
    
    def saveAsXML(self, xml_path, pretty_print= True):
        saveXML(self.etree, xml_path, pretty_print)

def fromXML(xml_path):
    if not isinstance(xml_path, pathlib.Path):
        xml_path = pathlib.Path(xml_path)
    xml_parser = lxml.etree.XMLParser(remove_blank_text=True)
    etree = lxml.etree.XML(
                xml_path.open(encoding= 'utf-8').detach().read(),
                parser= xml_parser)
    return TogetterData(etree)

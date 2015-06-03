# -*- coding:utf-8 -*-

import logging
import pathlib
import lxml.html
import requests

class WebPage:
    def __init__(self, url, session= None, params= None, logger= None):
        """constructor
        url(str): WebページのURL
        session(requests.sessions.Session): URLを開くためのsession
                                            (default None)
        params(dict): URLに渡されるparameter (default None)
        logger(logging.Logger): logger (default None)"""
        # logger設定
        if logger is None:
            logger = logging.getLogger(__name__)
            logger.addHandler(logging.NullHandler())
        self._logger = logger
        # 値設定
        if session is None:
            session = requests.session()
        self._response = session.get(url, params= params)
        self._html = lxml.html.fromstring(self.response.content)
    
    def page_title(self):
        """header部に書かれているtitleを返す"""
        xpath = r'head//title'
        return self.html.xpath(xpath)[0].text
    
    @property
    def url(self):
        return self._response.url
    
    @property
    def response(self):
        return self._response
    
    @property
    def html(self):
        return self._html
    
    def save(self, filepath):
        """page内容を保存する
        filepath(str, pathlib.Path): 保存先となるfile"""
        if isinstance(filepath, str):
            filepath = pathlib.Path(filepath)
        with filepath.open(mode= 'wb') as file:
            file.write(self.response.content)

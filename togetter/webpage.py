# -*- coding:utf-8 -*-

import logging
import pathlib
from typing import Union
import lxml.html
import requests

class WebPage:
    def __init__(
                self,
                url: str,
                session: requests.sessions.Session = None,
                params: dict = None,
                logger: logging.Logger = None) -> None:
        """Initialize

        Arguments:
        url (str): URL to send.
        session (requests.sessions.Session, optional):
            A Requests session.
            Defaults to None. Then new Session will be Createed.
        params (dict, optional):
            dictonary of URL parameters to append to the URL.
            Defaults to None.
        logger (logging.Logger, optional):
            Logger
            Defauults to None, then new Logger will be Created"""
        self._logger = (logger
                    if logger is not None else logging.getLoger(__name__))
        self._session = session if session is not None else requests.Session()
        self._response = self._session.get(url, params= params)
        self._html = lxml.html.fromstring(self.response.content)
    
    @property
    def session(self) -> requests.sessions.Session:
        return self._session

    @property
    def url(self) -> str:
        return self._response.url
    
    @property
    def response(self) -> requests.Response:
        return self._response
    
    @property
    def html(self) -> lxml.html.HtmlElement:
        return self._html
    
    def page_title(self) -> str:
        """Get page title from HTML header"""
        xpath = r'head//title'
        return self.html.xpath(xpath)[0].text
    
    def save(self, filepath: Union[str, pathlib.Path]) -> None:
        """Save the contents of the pages in the file

        Args:
        filepath (str, pathlib.Path): Filepath to save the contents
        """
        if isinstance(filepath, str):
            filepath = pathlib.Path(filepath)
        with filepath.open(mode= 'wb') as file:
            file.write(self.response.content)

# -*- coding: utf-8 -*-


import logging
import re
import time
import requests
from .webpage import WebPage
from .togetter_page_parser import TogetterPageParser


class TogetterUserPage(WebPage):
    def __init__(self, user_id, page=1, session=None, logger=None):
        # logger設定
        if logger is None:
            logger = logging.getLoger(__name__)
        # 値設定
        self._user_id = user_id
        self._page_number = page
        # 接続
        url = r'http://togetter.com/id/{0}'.format(user_id)
        params = {'page': page} if page != 1 else {}
        if session is None:
            session = requests.session()
        self._session = session
        WebPage.__init__(self, url,
                         params=params,
                         session=self._session,
                         logger=logger)
        # logger出力
        self._logger.info('{0}'.format(self.__class__.__name__))
        self._logger.info('  user id: {0}'.format(self._user_id))
        self._logger.info('  page   : {0}'.format(self._page_number))
        self._logger.info('  URL    : {0}'.format(self.url))

    @property
    def user_id(self):
        return self._user_id

    @property
    def page_number(self):
        return self._page_number

    def get_page_list(self):
        xpath = r'//ul[@class="simple_list"]/li[@class]'
        return [TogetterPageInfo(data) for data in self.html.xpath(xpath)]

    def next_page(self):
        xpath = r'head/link[@rel="next"]'
        if (len(self.html.xpath(xpath)) == 1):
            return TogetterUserPage(self.user_id,
                                    page=self.page_number + 1,
                                    session=self._session,
                                    logger=self._logger)
        else:
            return None

    def prev_page(self):
        xpath = r'head/link[@rel="prev"]'
        if (len(self.html.xpath(xpath)) == 1):
            return TogetterUserPage(self.user_id,
                                    page=self.page_number - 1,
                                    session=self._session,
                                    logger=self._logger)
        else:
            return None


class TogetterPageInfo(object):
    def __init__(self, element):
        self._element = element

    @property
    def element(self):
        return self._element

    @property
    def url(self):
        xpath = r'./div[@class="inner"]/a[@href]'
        data = self.element.xpath(xpath)
        if len(data) == 1:
            return data[0].get('href')
        else:
            return None

    @property
    def title(self):
        xpath = r'./div[@class="inner"]/a[@href]/h3[@title]'
        data = self.element.xpath(xpath)
        if len(data) == 1:
            return data[0].text
        else:
            return None

    @property
    def page_id(self):
        url = self.url
        if url is not None:
            regex = re.match(r'http://togetter.com/li/(?P<id>[0-9]+)', url)
            if regex:
                return int(regex.group('id'))
            else:
                return None
        else:
            return None

    def open(self, session=None, logger=None):
        page_id = self.page_id
        if page_id is not None:
            return TogetterPageParser(
                        page_id,
                        session=session,
                        logger=logger)
        else:
            return None


def get_all_page_from_user(
            user_id,
            session=None,
            logger=None,
            wait_time=0.2):
    user_page = TogetterUserPage(user_id, session=session, logger=logger)
    while user_page is not None:
        for page_data in user_page.get_page_list():
            yield page_data
        user_page = user_page.next_page()
        time.sleep(wait_time)

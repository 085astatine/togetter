# -*- coding: utf-8 -*-


import datetime
import logging
import time
from typing import List, Optional
import requests
import lxml.etree
from .tweet_data import TweetData, TweetDataParser
from .webpage import WebPage


class TogetterPage(WebPage):
    def __init__(
                self,
                page_id: int,
                page_number: int = 1,
                session: requests.sessions.Session = None,
                logger: logging.Logger = None) -> None:
        """Initialize

        Args:
        page_id (int): the ID of the togetter page.
        page_number (int) optional:
            The page number of this page.
            Defaults to 1.
        session (requests.sessions.Session) optional:
            A Requests Session.
            Defaults to None. Then new Session will be created.
        logger (logging.Logger) optional:
            Logger.
            Defaults to None. Then new Logger will be created."""
        # logger設定
        if logger is None:
            logger = logging.getLogger(__name__)
        # 値設定
        self._page_id = page_id
        self._page_number = page_number
        self._tweet_list = None  # type: Optional[List[TweetData]]
        # 接続設定
        url = r'http://togetter.com/li/{0}'.format(self._page_id)
        params = {'page': self._page_number} if self._page_number != 1 else {}
        WebPage.__init__(
                    self,
                    url,
                    session=session,
                    params=params,
                    logger=logger)
        # logger出力
        self._logger.info('{0}'.format(self.__class__.__name__))
        self._logger.info('  title: {0}'.format(self.title))
        self._logger.info('  URL  : {0}'.format(self.url))

    @property
    def page_id(self) -> int:
        return self._page_id

    @property
    def page_number(self) -> int:
        return self._page_number

    @property
    def title(self) -> Optional[str]:
        xpath = r'head/meta[@property="og:title"]'
        result = self.html.xpath(xpath)
        if len(result) == 1:
            return result[0].get('content')
        else:
            return None

    @property
    def csrf_token(self) -> Optional[str]:
        xpath = 'head/meta[@name="csrf_token"]'
        result = self.html.xpath(xpath)
        if len(result) == 1:
            return result[0].get('content')
        else:
            return None

    @property
    def csrf_secret(self) -> Optional[str]:
        return self.session.cookies.get('csrf_secret', None)

    @property
    def creator(self) -> Optional[str]:
        xpath = r'head/meta[@name="twitter:creator"]'
        data = self.html.xpath(xpath)
        if len(data) == 1:
            return data[0].get('content')
        else:
            return None

    def get_tweet_list(self) -> List[TweetData]:
        """TweetData list in this page.

        If 「残りを読む」 exists in this page, then load more tweets.

        Returns:
            list[TweetData]
        """
        if self._tweet_list is None:
            self._tweet_list = []
            # Tweet
            xpath = r'//body//ul[./li[@class="list_item"]]'
            tweet_data = self.html.xpath(xpath)
            if len(tweet_data) == 1:
                self._tweet_list.extend(
                            _parse_tweet_data(tweet_data[0]))
            # More Tweets
            if self.more_tweets_exists():
                self._tweet_list.extend(
                            _parse_tweet_data(_get_more_tweets(self)))
        return self._tweet_list

    def more_tweets_exists(self) -> bool:
        """Return that whether or not 「残りを読む」 exists in this page."""
        xpath = r'body//div[@class="more_tweet_box"]'
        return len(self.html.xpath(xpath)) == 1

    def next_page(self) -> Optional['TogetterPage']:
        """Return the next page, if next page exists.

        Returns:
            TogetterPage: If next page exists.
            None: If next page does not exist."""
        xpath = r'head/link[@rel="next"]'
        if (len(self.html.xpath(xpath)) == 1):
            return TogetterPage(
                        self.page_id,
                        page_number=self.page_number + 1,
                        session=self.session,
                        logger=self._logger)
        else:
            return None

    def prev_page(self) -> Optional['TogetterPage']:
        """Return the previous page, if previous page exists.

        Returns:
            TogetterPage: If previous page exists.
            None: If previsous page does not exist."""
        xpath = r'head/link[@rel="prev"]'
        if (len(self.html.xpath(xpath)) == 1):
            return TogetterPage(
                        self.page_id,
                        page_number=self.page_number - 1,
                        session=self.session,
                        logger=self._logger)
        else:
            return None


def _get_more_tweets(self: TogetterPage) -> lxml.etree._Element:
    url = r'http://togetter.com/api/moreTweets/{0}'.format(self.page_id)
    data = {'page': 1,
            'csrf_token': self.csrf_token}
    response = self._session.post(url, data=data)
    tweet_data = lxml.html.fromstring(response.content.decode('utf-8'))
    # logger出力
    self._logger.info('getMoreTweets')
    self._logger.info('  URL: {0}'.format(response.url))
    self._logger.debug('  csrfToken : {0}'.format(self.csrf_token))
    self._logger.debug('  csrfSecret: {0}'.format(self.csrf_secret))
    return tweet_data


def _parse_tweet_data(tweet_etree: lxml.etree._Element) -> List[TweetData]:
    xpath = r'//li[@class="list_item"]/div[@class="list_box type_tweet"]'
    data_list = tweet_etree.xpath(xpath)
    return [TweetDataParser(data).parse() for data in data_list]

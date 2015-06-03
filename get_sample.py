# -*- coding: utf-8 -*-

import logging
from togetter import TogetterData, TogetterPage, fromXML

if __name__=='__main__':
    print('TogetterSample')
    # logger setting
    logger = logging.getLogger('TogetterSample')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.formatter = logging.Formatter(
                 fmt='%(name)s::%(levelname)s: %(message)s')
    logger.addHandler(handler)
    # get tweet from togetter
    togetter_id = XXXXXXX
    page = TogetterPage(togetter_id, logger= logger)
    page.loadTweets()
    # save as XML
    xml_file = 'togetter_{0}.xml'.format(togetter_id)
    page.saveAsXML(xml_file)
    # load from XML
    togetter_data = fromXML(xml_file)
    print(togetter_data.title)
    print(togetter_data.url)
    for tweet in togetter_data.tweet_list:
        print(tweet.user_name)
        print(tweet.tweet)
        print()

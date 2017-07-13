#! /usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import togetter


if __name__ == '__main__':
    print('TogetterSample')
    # logger setting
    logger = logging.getLogger('TogetterSample')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.formatter = logging.Formatter(
                 fmt='%(name)s::%(levelname)s: %(message)s')
    logger.addHandler(handler)
    # input togetter id
    while True:
        input_id = input("input TogetterPage ID >")
        try:
            togetter_id = int(input_id)
            break
        except ValueError as error:
            print("your input<{0}> is invalid".format(repr(input_id)))
            print(str(error))
    # get tweet from togetter
    parser = togetter.TogetterPageParser(togetter_id, logger=logger)
    parser.wait_time = 1.0
    # save as XML
    xml_file = 'togetter_{0}.xml'.format(togetter_id)
    parser.parse().save_as_xml(xml_file)
    # load from XML
    togetter_data = togetter.TogetterData.load_xml(xml_file)
    print(togetter_data.title)
    print(togetter_data.url)
    for tweet in togetter_data.tweet_list:
        print(tweet.user_name)
        print(tweet.tweet)
        print()

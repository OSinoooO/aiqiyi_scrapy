# -*- coding:utf-8 -*-
from scrapy import cmdline
import redis


def run():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
    start_url = 'http://list.iqiyi.com/www/1/-------------24-1-1-iqiyi--.html'
    r.lpush('aiqiyi:start_urls', start_url)
    cmdline.execute('scrapy crawl aiqiyi'.split())


if __name__ == '__main__':
    run()
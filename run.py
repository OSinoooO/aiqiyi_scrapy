# -*- coding:utf-8 -*-
from scrapy import cmdline


def run():
    cmdline.execute('scrapy crawl aiqiyi'.split())


if __name__ == '__main__':
    run()
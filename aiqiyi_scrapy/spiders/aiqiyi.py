# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urljoin
from copy import deepcopy
from ..items import *
import re
import json
from scrapy_redis.spiders import RedisCrawlSpider


class AiqiyiSpider(RedisCrawlSpider):
    name = 'aiqiyi'
    allowed_domains = ['iqiyi.com']
    # start_urls = ['http://list.iqiyi.com/www/1/-------------24-1-1-iqiyi--.html']
    redis_key = 'aiqiyi:start_urls'
    host_url = 'http://list.iqiyi.com/'

    rules = (
        # 标签首页
        Rule(LinkExtractor(allow=r'list.iqiyi.com/www/1/-------------24-1-1-iqiyi--.html', unique=False), callback='parse_tag', follow=True),
        # 电影列表页，并实现翻页
        Rule(LinkExtractor(allow=r'www/1/-------------24-\d+-1-iqiyi--.html'), callback='parse_mv_info', follow=True),
        # 电影详情页
        Rule(LinkExtractor(restrict_xpaths='//div[@class="site-piclist_pic"]/a'), callback='parse_mv_detail_info', follow=True),
        # 演员详情页
        Rule(LinkExtractor(restrict_xpaths='//ul[@class="intro-detail"]/li[2]//a'), callback='parse_actor_info'),
    )

    def parse_tag(self, response):  # 提取标签分类
        div_list = response.xpath('//div[@class="mod_sear_menu mt20 mb30"]/div[not(@id="block-B")]')[1:]
        for div in div_list:
            item = TagItem()
            item['b_cate'] = div.xpath('./h3/text()').extract_first().replace('：', '')
            li_list = div.xpath('./ul/li[not(@class="selected") and not(@class="close-mod_btn")]')
            for li in li_list:
                item['s_cate'] = li.xpath('./a/text()').extract_first()
                item['s_cate_href'] = urljoin(self.host_url, li.xpath('./a/@href').extract_first())
                yield deepcopy(item)

    def parse_mv_info(self, response):  # 提取电影基本信息
        li_list = response.xpath('//div[@class="wrapper-piclist"]//li')
        for li in li_list:
            item = MovieInfoItem()
            item['mv_id'] = li.xpath('.//a[@class="site-piclist_pic_link"]/@data-qidanadd-tvid').extract_first()
            item['mv_name'] = li.xpath('.//a[@class="site-piclist_pic_link"]/@title').extract_first()
            item['mv_href'] = li.xpath('.//a[@class="site-piclist_pic_link"]/@href').extract_first()
            item['mv_duration'] = li.xpath('.//span[@class="icon-vInfo"]/text()').extract_first().strip()
            item['mv_img'] = li.xpath('.//a[@class="site-piclist_pic_link"]/img/@src').extract_first()
            item['mv_score'] = ''.join(li.xpath('.//span[@class="score"]//text()').extract())
            yield item

    def parse_mv_detail_info(self, response):  # 提取电影详情信息
        item = MovieDetailInfoItem()
        tvid = re.findall(r"param\['tvid'\] = \"(\d+)\"", response.body.decode(), re.S)[0]
        item['mv_id'] = tvid
        director = response.xpath('//div[@class="intro-right"]//em[text()="导演："]/following-sibling::span//a/text()').extract()
        if len(director):
            item['mv_director'] = ','.join(director) if len(director) > 1 else director[0]
        else:
            item['mv_director'] = ''
        item['mv_cates'] = re.findall(r'"categories":"(.*?)"', response.body.decode(), re.S)[0] if len(re.findall(r'"categories":"(.*?)"', response.body.decode(), re.S)) else None
        item['mv_desc'] = response.xpath('//span[@class="content-paragraph"]/text()').extract_first()
        # 获取看点标签
        hot_url = 'https://qiqu.iqiyi.com/apis/video/tags/get?area=azalea&entity_id={}&limit=10'.format(tvid)
        yield scrapy.Request(hot_url, callback=self.parse_hot, meta={'item': item})

        # 提取演员和角色对应关系
        span_list = response.xpath('//ul[@class="intro-detail"]/li[2]//span[@class="name-wrap"]')
        for span in span_list:
            item = ActorPlayItem()
            item['mv_id'] = tvid
            item['actor'] = span.xpath('./a/text()').extract_first()
            item['character'] = span.xpath('./span/text()').extract_first()
            yield item

    def parse_hot(self, response):  # 提取看点标签
        item = response.meta['item']
        html = json.loads(response.body.decode())
        tag_list = []
        try:
            for tag in html['data']:
                tag_list.append(tag['tag'])
            item['mv_tag'] = ','.join(tag_list)
        except:
            item['mv_tag'] = None
        yield item

    def parse_actor_info(self, response):  # 提取演员信息
        item = ActorInfoItem()
        item['actor_name'] = response.xpath('//h1/text()').extract_first()
        item['actor_en_name'] = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[text()="外文名"]/following-sibling::dd/text()').extract_first()
        item['actor_gender'] = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[text()="性别"]/following-sibling::dd/text()').extract_first()
        item['actor_height'] = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[text()="身高"]/following-sibling::dd/text()').extract_first()
        item['actor_weight'] = response.xpath('//span[text()="体重："]/../text()').extract_first()
        item['actor_birthday'] = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[text()="出生日期"]/following-sibling::dd/text()').extract_first()
        item['actor_birth_area'] = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[text()="出生地"]/following-sibling::dd/text()').extract_first()
        item['actor_school'] = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[text()="毕业院校"]/following-sibling::dd/text()').extract_first()
        item['actor_fame'] = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dt[text()="成名年代"]/following-sibling::dd/text()').extract_first()
        item['actor_alias'] = response.xpath('//dl[@class="basicInfo-block basicInfo-right"]/dt[text()="别名"]/following-sibling::dd/text()').extract_first()
        item['actor_blood_group'] = response.xpath('//dl[@class="basicInfo-block basicInfo-right"]/dt[text()="血型"]/following-sibling::dd/text()').extract_first()
        item['actor_local'] = response.xpath('//dl[@class="basicInfo-block basicInfo-right"]/dt[text()="地区"]/following-sibling::dd/text()').extract_first()
        item['actor_constellation'] = response.xpath('//dl[@class="basicInfo-block basicInfo-right"]/dt[text()="星座"]/following-sibling::dd/text()').extract_first()
        item['actor_life_area'] = response.xpath('//dl[@class="basicInfo-block basicInfo-right"]/dt[text()="现居地"]/following-sibling::dd/text()').extract_first()
        item['actor_agency'] = response.xpath('//dl[@class="basicInfo-block basicInfo-right"]/dt[text()="经纪公司"]/following-sibling::dd/text()').extract_first()
        item['actor_hobby'] = response.xpath('//dl[@class="basicInfo-block basicInfo-right"]/dt[text()="爱好"]/following-sibling::dd/text()').extract_first()
        item['actor_desc'] = response.xpath('//p[@class="introduce-info"]/text()').extract_first()
        item['actor_img'] = response.xpath('//img[@itemprop="image"]/@src').extract_first().strip()
        yield item

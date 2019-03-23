# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TagItem(scrapy.Item):  # 标签信息
    s_cate = scrapy.Field()
    b_cate = scrapy.Field()
    s_cate_href = scrapy.Field()


class MovieInfoItem(scrapy.Item):  # 电影基本信息
    mv_id = scrapy.Field()
    mv_name = scrapy.Field()
    mv_href = scrapy.Field()
    mv_duration = scrapy.Field()
    mv_img = scrapy.Field()
    mv_score = scrapy.Field()


class MovieDetailInfoItem(scrapy.Item):  # 电影详情信息
    mv_id = scrapy.Field()
    mv_director = scrapy.Field()
    mv_cates = scrapy.Field()
    mv_actors = scrapy.Field()
    mv_characters = scrapy.Field()
    mv_desc = scrapy.Field()
    mv_tag = scrapy.Field()


class ActorPlayItem(scrapy.Item):  # 演员与扮演角色信息
    mv_id = scrapy.Field()
    actor = scrapy.Field()
    character = scrapy.Field()


class ActorInfoItem(scrapy.Item):   # 演员详情信息
    actor_name = scrapy.Field()
    actor_en_name = scrapy.Field()
    actor_gender = scrapy.Field()
    actor_height = scrapy.Field()
    actor_weight = scrapy.Field()
    actor_birthday = scrapy.Field()
    actor_birth_area = scrapy.Field()
    actor_school = scrapy.Field()
    actor_fame = scrapy.Field()
    actor_alias = scrapy.Field()
    actor_blood_group = scrapy.Field()
    actor_local = scrapy.Field()
    actor_constellation = scrapy.Field()
    actor_life_area = scrapy.Field()
    actor_agency = scrapy.Field()
    actor_hobby = scrapy.Field()
    actor_desc = scrapy.Field()
    actor_img = scrapy.Field()
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .items import *
import re
from pymysql import connect
from scrapy.log import logger


class AiqiyiPipeline(object):
    def __init__(self):
        self.conn = connect(host='localhost', port=3306, user='root', password='123456', database='aiqiyi', charset='utf8')
        self.cs = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, TagItem):
            params = [item['s_cate'], item['b_cate'], item['s_cate_href']]
            if not self.cs.execute('select * from cate where small_cate_name=%s;', item['s_cate']):
                self.cs.execute('insert into cate(small_cate_name, big_cate_name, small_cate_url) value(%s, %s, %s);', params)
                self.conn.commit()
        elif isinstance(item, MovieInfoItem):
            params = [item['mv_id'], item['mv_name'], item['mv_duration'], item['mv_img'], item['mv_score'], item['mv_href']]
            try:
                if not self.cs.execute('select * from mv_info where id=%s;', item['mv_id']):
                    self.cs.execute('insert into mv_info(id, mv_name, mv_duration, mv_img, mv_score, mv_url) value(%s, %s, %s, %s, %s, %s);', params)
                    self.conn.commit()
            except:
                logger.debug('数据重复')
        elif isinstance(item, MovieDetailInfoItem):
            # 以id进行去重
            try:
                params = [item['mv_id'], item['mv_director'], item['mv_cates'], item['mv_tag'], item['mv_desc']]
                if not self.cs.execute('select * from mv_detail_info where id=%s;', item['mv_id']):
                    self.cs.execute('insert into mv_detail_info(id, mv_director, mv_cates, mv_tag, mv_desc) value(%s, %s, %s, %s, %s);', params)
                    self.conn.commit()
            except:
                logger.debug('数据重复')
        elif isinstance(item, ActorInfoItem):
            if item['actor_name'] is not None:
                item['actor_name'] = item['actor_name'].strip()
            if item['actor_en_name'] is not None:
                item['actor_en_name'] = item['actor_en_name'].strip()
            if item['actor_gender'] is not None:
                item['actor_gender'] = item['actor_gender'].strip()
            if item['actor_height'] is not None:
                item['actor_height'] = item['actor_height'].strip()
            if item['actor_weight'] is not None:
                item['actor_weight'] = item['actor_weight'].strip()
            if item['actor_birthday'] is not None:
                item['actor_birthday'] = item['actor_birthday'].strip()
            if item['actor_birth_area'] is not None:
                item['actor_birth_area'] = item['actor_birth_area'].strip()
            if item['actor_school'] is not None:
                item['actor_school'] = item['actor_school'].strip()
            if item['actor_fame'] is not None:
                item['actor_fame'] = item['actor_fame'].strip()
            if item['actor_alias'] is not None:
                item['actor_alias'] = item['actor_alias'].strip()
            if item['actor_blood_group'] is not None:
                item['actor_blood_group'] = item['actor_blood_group'].strip()
            if item['actor_local'] is not None:
                item['actor_local'] = item['actor_local'].strip()
            if item['actor_constellation'] is not None:
                item['actor_constellation'] = item['actor_constellation'].strip()
            if item['actor_life_area'] is not None:
                item['actor_life_area'] = item['actor_life_area'].strip()
            if item['actor_agency'] is not None:
                item['actor_agency'] = item['actor_agency'].strip()
            if item['actor_hobby'] is not None:
                item['actor_hobby'] = item['actor_hobby'].strip()
            if item['actor_desc'] is not None:
                item['actor_desc'] = re.sub(r"\s+|\n|'|\\xa0|\[\d+\]", '', item['actor_desc'].strip())
            if item['actor_img'] is not None:
                item['actor_img'] = item['actor_img'].strip()
            params = [
                item['actor_name'],
                item['actor_en_name'],
                item['actor_gender'],
                item['actor_height'],
                item['actor_weight'],
                item['actor_birthday'],
                item['actor_birth_area'],
                item['actor_school'],
                item['actor_fame'],
                item['actor_alias'],
                item['actor_blood_group'],
                item['actor_local'],
                item['actor_constellation'],
                item['actor_life_area'],
                item['actor_agency'],
                item['actor_hobby'],
                item['actor_img'],
                item['actor_desc']
            ]
            try:
                if not self.cs.execute('select * from actor where actor_name=%s;', item['actor_name']):
                    self.cs.execute(
                        'insert into actor(actor_name,actor_en_name,actor_gender,actor_height,actor_weight,\
                        actor_birthday,actor_birth_area,actor_school,actor_fame,actor_alias,actor_blood_group,\
                        actor_local,actor_constellation,actor_life_area,actor_agency,actor_hobby,actor_img,\
                        actor_desc) value(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
                        params
                    )
                    self.conn.commit()
            except:
                logger.debug('数据重复')
        elif isinstance(item, ActorPlayItem):
            if item['character'] is not None:
                item['character'] = item['character'][2:]
            params = [item['mv_id'], item['actor'], item['character']]
            if not self.cs.execute('select * from player where id=%s;', item['mv_id']):
                self.cs.execute('insert into player(id, mv_actor, mv_character) value(%s, %s, %s);', params)
                self.conn.commit()
        return item

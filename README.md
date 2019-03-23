# aiqiyi_scrapy
爱奇艺电影信息爬虫（rediscrawlscrapy）

## 程序简介
使用rediscrawlscrapy框架，爬取爱奇艺电影信息及演员信息（不包含电影video资源），可实现分布式（但没必要- -，数据不多）

数据保存至mysql，已做备份（aiqiyi.sql）

## 运行
### 首次运行请执行 first_run.py

或者

redis(0) 中把 start_url 写入 aiqiyi:start_url (确保开启 redis 服务)

```
cmd: redis-cli

redis: select 0
redis: lpush aiqiyi:start_url 'http://list.iqiyi.com/www/1/-------------24-1-1-iqiyi--.html'
redis: exit
```

再运行 scrapy
```
cmd: scrapy crawl aiqiyi
```

### 再次运行直接执行 run.py 即可
或者
```
cmd: scrapy crawl aiqiyi
```

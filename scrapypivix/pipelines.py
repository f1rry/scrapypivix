# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import requests
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class ImagesPivixPipeline(ImagesPipeline):
	def get_media_requests(self,item,info):
		#没有refer会报403
		referer='https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+item['illust_id']
		headers={
			'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
			'referer':referer
		}
		yield Request(item['url'],headers=headers,dont_filter=True)

	def item_completed(self,results,item,info):
		image_paths=[x['path'] for ok,x in results if ok]
		if not image_paths:
			raise DropItem
		return item

	def file_path(self, request, response=None, info=None):
		url = request.url
		file_name = url.split('/')[-1]
		return file_name

class MySqlPipeline():
	"""docstring for MySqlPipeline"""
	def __init__(self,user,password,host,port,database,table):
		self.user=user
		self.password=password
		self.host=host
		self.port=port
		self.database=database
		self.table=table

	@classmethod
	def from_crawler(cls, crawler):
		user=crawler.settings['MYSQL_USER']
		password=crawler.settings['MYSQL_PASSWORD']
		host=crawler.settings['MYSQL_HOST']
		port=crawler.settings['MYSQL_PORT']
		database=crawler.settings['MYSQL_DATABASE']
		table=crawler.settings['MYSQL_TABLE']
		return cls(user,password,host,port,database,table)

	def open_spider(self,spider):
		self.db=pymysql.connect(self.host,self.user,self.password,self.database,self.port,charset='utf8')
		self.cursor=self.db.cursor()

	def close_spider(self,spider):
		self.db.close() 

	def process_item(self,item,spider):
		data=dict(item)
		keys=','.join(data.keys())
		values=','.join(['%s']*len(data.values()))
		sql="insert into %s(%s) values(%s)"%(self.table,keys,values)
		print(sql)
		self.cursor.execute(sql,tuple(data.values()))
		self.db.commit()
		return item

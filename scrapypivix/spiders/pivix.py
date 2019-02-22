# -*- coding: utf-8 -*-
import scrapy
import win32api
import json
import re
from urllib.parse import urlencode
from scrapypivix.items import ScrapypivixItem

class PivixSpider(scrapy.Spider):
	name = 'pivix'
	allowed_domains = ['www.pivix.net']
	start_urls = ['http://www.pivix.net/']

	def parse(self, response):
		contents=json.loads(response.text).get('contents')
		for content in contents:
			item=ScrapypivixItem()
			item['user_id']=str(content.get('user_id'))
			item['user_name']=content.get('user_name')
			item['title']=content.get('title')
			item['tags']=",".join(content.get('tags'))
			item['illust_id']=str(content.get('illust_id'))
			#爬取缩略图
			item['url']=content.get('url')
			yield item

	def start_requests(self):
		SSR_POSITION=self.settings.get('SSR_POSITION')
		win32api.ShellExecute(0, 'open', SSR_POSITION, '','',1)
		base_url='https://www.pixiv.net/ranking.php?'
		params={
		'mode': 'daily',
		'content': 'illust',
		'p':1,
		'format': 'json',
		}
		MAX_PAGE=self.settings.get('MAX_PAGE',5)
		for i in range(1,MAX_PAGE+1):
			params['p']=i
			url=base_url+urlencode(params)
			yield scrapy.Request(url,self.parse)


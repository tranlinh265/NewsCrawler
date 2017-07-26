# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.item import Item, Field
import scrapy
import html2text
import time
import datetime
from bs4 import BeautifulSoup

table={ "c4 90" : u'\u0110',"c3 a0" : u'\u00E0',
        "c3 80" : u'\u00C0',"c3 81" : u'\u00C1',
        "c3 82" : u'\u00C2',"c3 83" : u'\u00C3',
        "c3 88" : u'\u00C8',"c3 89" : u'\u00C9',
        "c3 8a" : u'\u00CA',"c3 8c" : u'\u00CC',
        "c3 8d" : u'\u00CD',"c3 92" : u'\u00D2',
        "c3 93" : u'\u00D3',"c3 94" : u'\u00D4',
        "c3 95" : u'\u00D5',"c3 99" : u'\u00D9',
        "c3 9a" : u'\u00DA',"c3 9d" : u'\u00DD',
        "c3 a0" : u'\u00E0',"c3 a1" : u'\u00E1',
        "c3 a2" : u'\u00E2',"c3 a3" : u'\u00E3',
        "c3 a8" : u'\u00E8',"c3 a9" : u'\u00E9',
        "c3 aa" : u'\u00EA',"c3 ac" : u'\u00EC',
        "c3 ad" : u'\u00ED',"c3 b2" : u'\u00F2',
        "c3 b2" : u'\u00F2',"c3 b3" : u'\u00F3',
        "c3 b4" : u'\u00F4',"c3 b5" : u'\u00F5',
        "c3 b9" : u'\u00F9',"c3 ba" : u'\u00FA',
        "c3 bd" : u'\u00FD'}
def convert_string(string):
    arr = string.split('%')
    for x in xrange(1,len(arr)-1):
        if x % 2 == 1:
            tmp1 = "%"+arr[x][:2]+"%"+arr[x+1][:2]
            tmp = ""+arr[x][:2]+" "+arr[x+1][:2]
            for k,v in table.items():
                if tmp.lower() == k:
                    string = string.replace(tmp1,v)
    return string

def replace_href_link(context):
    context = context.replace(" target=\"_blank\"",'')
    soup = BeautifulSoup(context,"html.parser")
    for link in soup.findAll('a'):
        try:
            href = str(link.get('href'))
            tmp1 = href.split("Keyword=")[1]
            tmp2 = tmp1.split("&")[0]
            # tmp = tmp2.split(' '.decode("utf8"))
            tmp = tmp2.split("%C2%A0")
            tmp3 = tmp[0]
            tmp4 = "<a href="+"/articles/so_ki_hieu/"+tmp3+">"+str(tmp3).decode('utf8')+"</a>"
            if len(tmp)==2:
                tmp4 = tmp4 + " "+tmp[1] + " "
            context = context.replace(str(link),str(tmp4))
        except IndexError:
            pass
    return context.decode("utf-8","ignore")

from vbpl_news_crawler.items import VbplNewsCrawlerItem
class NewsSpider(Spider):
    name = "vbpl_news"
    allowed_domains = ['vbpl.vn', 'www.vbpl.vn','http://vbpl.vn']
    start_urls = [
        "http://vbpl.vn/noidung/news/Lists/ThongBao/View_Detail.aspx",
    ]

    def parse(self,response):
        news_items = Selector(response).xpath('//div[@class="news-item"]')
        for news_item in news_items:
            meta = {}
            meta['doc_title'] = news_item.xpath('p[@class="title"]/a/text()').extract()[0]
            meta['doc_url'] = news_item.xpath('p[@class="title"]/a/@href').extract()[0]
            meta['doc_id'] = str(meta['doc_url']).split('=')[1]
            meta['doc_date'] = news_item.xpath('p[@class="title"]/span/text()').extract()[0]
            meta['doc_description'] = news_item.xpath('div[@class="description"]/text()').extract()[0]
            url = "http://vbpl.vn/" + str(meta['doc_url'])
            yield scrapy.Request(url, callback = self.parse_document, meta = meta)

    def parse_document(self,response):
    	meta = response.meta
    	item = VbplNewsCrawlerItem()
<<<<<<< HEAD
    	item['doc_id'] = str(meta['doc_id']).encode('utf-8')
    	item['title'] = meta['doc_title'].encode('utf-8').strip()
    	item['url'] ="http://vbpl.vn/" + str(meta['doc_url']).encode('utf-8')
    	item['public_date'] = str(meta['doc_date']).encode('utf-8')
    	item['description'] = meta['doc_description'].encode('utf-8').strip()
=======
    	item['doc_id'] = str(meta['doc_id']).encode('utf-8',"ignore")
    	item['doc_title'] = meta['doc_title'].encode('utf-8',"ignore").strip()
    	item['doc_url'] ="http://vbpl.vn/" + str(meta['doc_url']).encode('utf-8',"ignore")
    	item['doc_date'] = str(meta['doc_date']).encode('utf-8',"ignore")
    	item['doc_description'] = meta['doc_description'].encode('utf-8',"ignore").strip()
>>>>>>> cbc9a45a704f1b4794db991318547b30f264f3ce

    	news_content = response.xpath('//div[@class="box-news box-news-home "]//div[@class="content"]')
    	
    	news_content_html = news_content.extract()[0]
    	news_other_html = news_content.xpath('//div[@class="news-other"]').extract()[0]
<<<<<<< HEAD
        news_content = str(news_content_html.encode('utf-8')).replace(str(news_other_html.encode('utf-8')),'')
        item['content'] = replace_href_link(news_content).strip()
=======

    	# config_html = html2text.HTML2Text()
    	# config_html.ignore_links = True

    	# news_other = config_html.handle(news_other_html)
    	# news_content = config_html.handle(news_content_html)
    	# news_content = news_content.replace(news_other,'')
    	# news_content = news_content.replace('*','')
        news_content = str(news_content_html.encode('utf-8',"ignore")).replace(str(news_other_html.encode('utf-8',"ignore")),'')
        news_content_tmp = replace_href_link(news_content).strip()
        item['doc_content'] = convert_string(news_content_tmp)
>>>>>>> cbc9a45a704f1b4794db991318547b30f264f3ce
        item['updated_at'] = str(datetime.datetime.now())
        item['created_at'] = str(datetime.datetime.now())

    	yield item
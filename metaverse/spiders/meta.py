import re

import scrapy
import lxml.html

from metaverse.items import MetaverseItem
from bs4 import BeautifulSoup


class MetaSpider(scrapy.Spider):
    name = 'metav'
    allowed_domains = ['coinonpro.com']
    start_urls = ['https://www.coinonpro.com/category/nft/page/1']

    def parse(self, response):
        articles = response.xpath("(//div[@class='sec-panel-body']/ul)[1]/li").getall()
        # print(articles)
        for article in articles:
            # item = article.xpath("//div[@class='item-content']")
            item = lxml.html.fromstring(article)
            title = item.xpath("(((//div[@class='item-content'])[1]/h2[@class='item-title'])[1]/a)[1]/text()")
            str_title = title[0].strip("\n")
            str_title = str_title.strip()
            hrefs = item.xpath("(((//div[@class='item-content'])[1]/h2[@class='item-title'])[1]/a)[1]/@href")
            print(str_title)
            print(hrefs[0])
            yield scrapy.Request(url= hrefs[0],meta = {"str_title":str_title,"type":2,"quote":hrefs[0]},callback=self.parse_detail,dont_filter=True)


    def parse_detail(self, response):
        content = response.xpath('(//div[@class="entry-content"]/div[@class=""])').get()
        # print (content)
        content = content.replace("href=\"https://www.coinonpro.com","href=\"https://www.metaversezhijia.com")

        contentStr = content.replace("CoinON","元宇宙之家")
        # print(content)
        # re_noscript = re.compile ('<\s*noscript[^>]*>[\s\S]*<\s*/\s*noscript\s*>', re.I) #noscript
        re_script = re.compile ('<\s*script[^>]*>[\s\S]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile ('<\s*style[^>]*>[\s\S]*<\s*/\s*style\s*>', re.I)  # style
        # re_img=  re.compile ('(?<!<noscript>)<\s*img[\s\S]*>',re.I)
        # contentStr = re_noscript.sub("",contentStr)
        contentStr = re_script.sub("",contentStr)
        contentStr = re_style.sub("",contentStr)
        # contentStr = re_img.sub("",contentStr)
        # contentStr = contentStr.replace("/wp-content/uploads/2021/09/元宇宙之家.jpg","/metaverse.jpg")
        contentStr = contentStr.replace ("<noscript>", "")
        contentStr = contentStr.replace ("</noscript>", "")
        print("-----------start------")
        print(contentStr)
        print ("-----------end------")
        # soup = BeautifulSoup(contentStr,"lxml")
        # [script.extract() for script in soup.findAll ('script')]
        # [style.extract() for style in soup.findAll ('style')]
        # [noscript.extract () for noscript in soup.findAll ('noscript')]
        # contentStr = soup.get_text()
        item = MetaverseItem()
        item["mContent"] = contentStr
        item["type"] = response.meta["type"]
        item["title"] = response.meta["str_title"]
        item["quote"] = response.meta["quote"]
        yield item





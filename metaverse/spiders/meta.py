import scrapy
import lxml.html

from metaverse.items import MetaverseItem


class MetaSpider(scrapy.Spider):
    name = 'meta'
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
        content = response.xpath ('((//div[@class="entry-content"])[1])').get()
        content = content.replace("href=\"https://www.coinonpro.com","href=\"https://www.metaversezhijia.com")
        contentStr = content.replace("CoinON","元宇宙之家")
        # print(content)
        item = MetaverseItem()
        item["mContent"] = contentStr
        item["type"] = response.meta["type"]
        item["title"] = response.meta["str_title"]
        item["quote"] = response.meta["quote"]
        yield item





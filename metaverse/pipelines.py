# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime

import pymysql
from itemadapter import ItemAdapter


class MetaversePipeline:
    def __init__(self) -> None:
        self.db = pymysql.connect(host='localhost', user='meta', passwd='LymariPCRaP5n62S', db='meta', charset='utf8', port=3306)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        sqlQuery = "SELECT quote_from from mtthreads WHERE quote_from = %s"
        self.cursor.execute(sqlQuery, item['quote'])
        result = self.cursor.fetchone()
        if result is not None:
            print("----存在----")
        else:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sqlInsertThread = "INSERT INTO mtthreads(user_id,last_posted_user_id,category_id,type,title,post_count," \
                              "posted_at,created_at,updated_at,issue_at,is_approved,quote_from,address) VALUES (1,1,%s,99,%s,1," \
                              "%s,%s,%s,%s,1,%s,%s)"
            self.cursor.execute(sqlInsertThread, (item['type'], item['title'], dt, dt,dt,dt,item['quote'],""))
            intert_id = self.cursor.lastrowid
            sqlInsertPost = "INSERT INTO mtposts(user_id,thread_id,content,ip,port,created_at,updated_at,is_first,is_approved) " \
                            "VALUES(1,%s,%s,%s,1024,%s,%s,1,1)"
            self.cursor.execute(sqlInsertPost,(str(intert_id),item["mContent"],"127.0.0.1",dt,dt))
            self.db.commit()



        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

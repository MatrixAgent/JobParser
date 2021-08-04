# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.scrapy_vacancies


    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        if spider.name=='hh_ru':
            item['salary'] = self.parse_salary1(item['salary'][0])
        else:
            item['salary'] = self.parse_salary2(item['salary'])
        collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        return item

    def parse_salary1(self, t):
        t = t.replace('\xa0', '').split()
        r1 = r2 = r3 = None
        if t[0] == 'от':
            if t[2] == 'до':
                r1 = int(t[1])
                r2 = int(t[3])
                r3 = t[4]
            else:
                r1 = int(t[1])
                r3 = t[2]
        elif t[0] == 'до':
            r2 = int(t[1])
            r3 = t[2]
        # else:
        #     r1 = int(t[0])
        #     if t[1] == '\u2013':  # символ '-' какой-то особый
        #         r2 = int(t[2])
        #         r3 = t[3]
        #     else:
        #         r3 = t[1]
        return (r1, r2, r3)

    def parse_salary2(self, t):
        r1 = r2 = r3 = None
        if len(t) == 9:
            r1 = int(t[0].replace('\xa0', ''))
            r2 = int(t[4].replace('\xa0', ''))
            r3 = t[6]
        elif len(t) == 5:
            if t[0] in ('от', 'до'):
                l = t[2].split('\xa0')
                r = int(''.join(l[:-1]))
                r3 = l[-1]
                if t[0] == 'от':
                    r1 = r
                else:
                    r2 = r
            else:
                r1 = int(t[0].replace('\xa0', ''))
                r3 = t[2]
        return (r1, r2, r3)

# coding=utf-8
import re
import json
from pymongo import MongoClient
from Kg_Android.func.Config import SOURCE_MONGODB_CLIENT, SOURCE_DATABASE, SOURCE_COLLECTION


class WriteJD(object):
    @staticmethod
    def connect_to_mongodb():
        """建立MongoDB数据库连接"""
        client = MongoClient(SOURCE_MONGODB_CLIENT)
        db = client[SOURCE_DATABASE]
        job = db[SOURCE_COLLECTION]
        print('加载完毕')
        return job

    @staticmethod
    def find_element(job):
        """查找集合中所有数据"""
        li = []
        n = 1
        # for item in job.find({'resume_from': 'qianchengwuyou', 'crawled_at': '2018-05-17', 'key_word': 'python'}):
        for item in job.find({"job_name": {'$regex': '.*ndroid.*'}}):
            # print(item)
            li.append(item)
            # print('加载了：{}条'.format(n))
            n += 1
            # if item['resume_from'] == 'liepin' or item['resume_from'] == 'qianchengwuyou':
            # if item['resume_from'] == 'liepin':
            # print(item)
            # li.append(item)
            # if len(li) == 5000:
            #     print(len(li))
            #     print('加载完成')
            #     print(li)
            # break
        print('len:', len(li))
        return li

    @staticmethod
    def remove_repeat(li):
        """去重并写入到文件"""
        print('开始写入==========================')
        # print(li)
        # s = set()
        # for i in li:
        #     s.add(i['JD_url'])
        #
        # s = list(s)
        # print(len(s), '=' * 50)
        # print('写入数据')
        # print(len(li))
        with open('./data/prepare_data/jd.json', 'a', encoding='utf-8') as f:

            lis = []
            for index, i in enumerate(li):
                i["_id"] = {"$oid": str(i["_id"])}
                jd = i.get('jd', None)
                if jd:
                    i['job_description'] = i['jd']
                if i['job_description'] not in lis:
                    lis.append(i['job_description'])
                    if '的' in str(i['job_description']):
                        # print(i['job_description'])
                        if index == 5000:
                            break
                        i = json.dumps(i)
                        # print(i)
                        i = re.sub(r'\\n|\\t|\\"', '', i)
                        i = i.encode().decode('unicode_escape')
                        i = re.sub(r'\\', '/', i)
                        i = i.lower()
                        f.write(i + '\n')
                        # lis.append(eval(i['contact']))


if __name__ == '__main__':
    wj = WriteJD()
    # 获取每个岗位需求的实际描述
    job = wj.connect_to_mongodb()
    # 将jd提取出来，并装入字典
    li = wj.find_element(job)
    # 去重并写入到文件
    # print(len(li))
    wj.remove_repeat(li)

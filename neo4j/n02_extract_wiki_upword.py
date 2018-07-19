# coding=utf-8
from pymongo import MongoClient


class WriteJD(object):
    @staticmethod
    def connect_to_mongodb():
        """建立MongoDB数据库连接"""
        client = MongoClient("mongodb://root:abc123@127.0.0.1:27017")
        db = client["skillmap"]
        job = db["wiki_android"]
        return job

    @staticmethod
    def find_element(job):
        """查找集合中所有数据"""
        n = 0
        li = list()
        for item in job.find({}):
            di = dict()
            di['search_key'] = item['search_key']
            di['title'] = item['title']
            di['category'] = item['category']
            di['introduction'] = item['introduction']
            di['infobox'] = item['infobox']

            li.append(di)
            n += 1
            # print(item)
        print('===========读取完成============')
        # print(li)
        return li
        # return list(job.find())

    @staticmethod
    def remove_repeat(li):
        """去重并写入到文件"""
        print('开始去重')
        try:
            li = set(li)
            li = list(li)
        except:
            pass
        li_str = str(li)
        print('写入数据')
        with open('./data/up_word_catg.sql', 'w', encoding='utf-8') as f:
            for i in eval(li_str):
                print(i)
                f.write(str(i).encode().decode('utf-8') + '\n')


if __name__ == '__main__':
    wj = WriteJD()
    # 获取每个岗位需求的实际描述
    job = wj.connect_to_mongodb()
    # 将jd提取出来，并装入字典
    li = wj.find_element(job)
    # 去重并写入到文件
    wj.remove_repeat(li)

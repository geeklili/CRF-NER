# coding=utf-8
import os
import jieba
import re
import jieba.posseg as pseg
from pymongo import MongoClient
from Kg_Android.func.Config import MONGODB_CLIENT, POSED_DATABASE, POSED_COLLECTION


class EntityDict(object):
    @staticmethod
    def connect_to_mongodb():
        """建立MongoDB数据库连接"""
        client = MongoClient(MONGODB_CLIENT)
        db = client[POSED_DATABASE]
        jobs = db[POSED_COLLECTION]
        return jobs

    @staticmethod
    def find_element(job):
        """查找集合中所有数据"""
        n = 0
        lis = list()
        for item in job.find({}):
            jd = item['tags']
            lis.append(jd)
            n += 1
            print(n)
        print('===========读取完成============')
        return lis

    @staticmethod
    def remove_repeat(li):
        """去重并写入到文件"""

        print('写入数据')
        with open('./data/change_data/pos_tag.data', 'w', encoding='utf-8') as f:
            for i in li:
                for j in i:
                    one = j['word']
                    two = j['tag']
                    one = re.sub('❤|️|〃|′|▽|`|\s|：|', '', one)
                    if one:
                        str_r = one + '\t' + two + '\n'

                        f.write(str_r)

    def combine(self):
        with open('./data/change_data/pos_tag.data', 'r', encoding='utf-8') as f:
            content = f.readlines()
            li = []
            for index, i in enumerate(content):
                lis = i.strip().split('\t')
                word = lis[0]
                tag = lis[1]
                li.append({word: tag})

            print(li)

            li2 = []
            for j, di in enumerate(li):
                if j >= 1:
                    w = list(di.keys())[0]
                    t = list(di.values())[0]
                    wj = list(li[j - 1].keys())[0]
                    tj = list(li[j - 1].values())[0]
                    print(wj, tj, w, t)
                    if tj == "1":
                        if tj == t:
                            w0 = wj + w
                        else:
                            w0 = wj

                        li2.append(w0)
            print(list(set(li2)))
            print(len(list(set(li2))))

            with open('./data/change_data/combine.data', 'w', encoding='utf-8') as f2:
                lis_o = list(set(li2))
                #
                # with open('./data/prepare_data/jd.json', 'r', encoding='utf-8') as f3:
                #     cont = f3.readlines()
                #     lis_t = []
                #     for i in cont:
                #         tags = eval(i)["tags"]
                #         for j in tags:
                #             lis_t.append(j)
                #             print(j)
                #     lis_t = list(set(lis_t))
                #     lis_c = list(set(lis_o).union(set(lis_t)))
                #     lis_c = list(set(lis_c))
                lis_c = list(set(lis_o))
                for c in lis_c:
                    f2.write(c + '\n')

    @staticmethod
    def create_uer_dict():
        with open('./data/change_data/combine.data', 'r', encoding='utf-8') as f:
            cont = f.readlines()
            li = []
            for i in cont:
                i.strip()
                li.append(i.strip())

            print(li)
            cont_li = ' '.join(li)
        print(cont_li)
        with open('./data/change_data/iter_user_dict.data', 'w', encoding='utf-8') as f2:
            jieba.load_userdict("./data/change_data/combine.data")
            words = pseg.cut(cont_li)
            n = 500
            for word, flag in words:
                # print(word, flag)
                if word != ' ':
                    f2.write(word + ' ' + str(n) + '\n')
                    n -= 1

    @staticmethod
    def create_entity_word():
        with open('./data/change_data/iter_user_dict.data', 'r', encoding='utf-8') as f1:
            with open('./data/change_data/iter_entity.data', 'w', encoding='utf-8') as f2:
                cont = f1.readlines()
                for i in cont:
                    word = i.strip().split(' ')[0]
                    if len(word) > 1:
                        f2.write(word + '\n')

        if os.path.exists('./data/change_data/pos_tag.data'):
            os.unlink('./data/change_data/pos_tag.data')
        if os.path.exists('./data/change_data/combine.data'):
            os.unlink('./data/change_data/combine.data')
        if os.path.exists('./data/prepare_data/jd_cut.data'):
            os.unlink('./data/prepare_data/jd_cut.data')


if __name__ == '__main__':
    # 生成 词 0/1 的标记文件
    edi = EntityDict()
    # 获取每个岗位需求的实际描述
    job = edi.connect_to_mongodb()
    # 将jd提取出来，并装入字典
    li = edi.find_element(job)
    # 去重并写入到文件
    edi.remove_repeat(li)

    # 生成 合体文件，即是将连续的两个词合成一个词
    edi.combine()

    edi.create_uer_dict()
    edi.create_entity_word()

import re
import json
import time
import jieba
import random
from pymongo import MongoClient
from Kg_Android.func.Config import MONGODB_CLIENT, WAIT_POS_DATABASE, WAIT_POS_COLLECTION


class SaveToMongodb(object):
    @staticmethod
    def extract_jd(job):
        jd_list = job['job_description']
        jd_text = []
        for jd_sentence in jd_list:
            jd_sentence = re.sub('\。|\（|\）|\(|\)|◆|\•|\！|❤|__|️|★⊙|『|③|é|＋|￣|／|☆|②||#|①|｝|８|²', '', jd_sentence)
            jd_sentence = re.sub('\+|－|^|●|｛|!|→|﹏|_|１|#|』|λ|⑨|＃|%|@|=|⺴', '', jd_sentence)
            jd_sentence = re.sub('、', '/', jd_sentence)
            jd_sentence = re.sub('，', ',', jd_sentence)
            jd_sentence = re.sub('：', '', jd_sentence)
            jd_sentence = re.sub('；', ';', jd_sentence)
            jd_sentence = re.sub('\n', '', jd_sentence)
            jd_sentence = re.sub('\d/', '', jd_sentence)
            jd_sentence = re.sub('\d\.', '', jd_sentence)
            jd_sentence = re.sub('岗位职责|岗位要求|工作内容|薪资福利|任职资格|职位描述|职位要求'
                                 '|工作职责|职责描述|任职要求|职位诱惑|职责概述|职责内容|工资待遇|职责表述'
                                 '|职位职责|招聘要求|薪酬福利', '', jd_sentence)
            jd_sentence = jd_sentence.replace(' ', '')
            jd_sentence = jd_sentence.lower()
            jd_text.append(jd_sentence)
        return jd_text

    @staticmethod
    def generate_jieba(tech_lists, jieba_file):
        for tech_list in tech_lists:
            words = list(jieba.cut(tech_list))
            jieba_file.write(' '.join(words) + '\n')

    @staticmethod
    def save_in_mongodb(db_name, collection):
        data = open('./data/prepare_data/jd_cut.data', "r", encoding="utf-8").readlines()
        client = MongoClient(MONGODB_CLIENT)
        db = client[db_name]
        col = db[collection]
        n = 1
        for d in data:
            print('存{}条了'.format(n))
            data = {
                'uid': '364-8987',
                'segs': d.strip().split(" "),
                'time': time.time()
            }
            col.insert_one(data)
            n += 1

    def cut_save(self):
        # 分词 5000 %5----> 存到，mongodb
        random.seed(10)
        with open('./data/prepare_data/jd.json', 'r', encoding='utf-8')as f0:
            cont = f0.readlines()
            jd_number = len(cont)

        db_name = WAIT_POS_DATABASE
        collection_name = WAIT_POS_COLLECTION
        # 在5000封简历里，随即挑选250封简历的下标
        random_number = random.sample(range(jd_number), int(0.045 * jd_number))
        print(random_number)
        with open('./data/prepare_data/jd.json', 'r', encoding='utf-8')as f1, \
                open('./data/prepare_data/jd_cut.data', 'w+', encoding='utf-8')as f2:
            i = 0
            for jd in f1:
                # print(jd)
                # print(i)
                i = i + 1
                if i in random_number:
                    jd_info = json.loads(jd)
                    jd_list = self.extract_jd(jd_info)
                    self.generate_jieba(jd_list, f2)

        # 存到mongodb
        self.save_in_mongodb(db_name, collection_name)
        # os.unlink('./data/prepare_data/jd_cut.data')


if __name__ == '__main__':
    sm = SaveToMongodb()
    sm.cut_save()

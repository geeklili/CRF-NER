import random
import re
import json
import os
import jieba
import jieba.posseg as psg
import jieba.posseg  # 词性标注模块


class TrainTest(object):
    @staticmethod
    def load_list(dict_name):
        tech_dict = []
        with open(dict_name, 'r', encoding='utf-8') as f:
            for line in f:
                tech_dict.append(line.strip('\n').split(' ')[0])
        return tech_dict

    @staticmethod
    def extract_jd(job):
        jd_list = job['job_description']
        jd_text = []
        for jd_sentence in jd_list:
            jd_sentence = re.sub(
                '\。|\（|\）|\(|\)|◆|\•|\！|❤|__|️|★|ｃ|_|【|■|３|’|‘|＋|·|？|１|《|ｍ|ザ|ク|ベ|サ|グ|~|ｉ|い|ニ|チ|ィ|'
                'ま|ｒ|ズ|イ|ア|ネ|%|シ|リ|め|ラ|る|⑥|フ|ｓ|り|タ|＃|け|ダ|す|ム|際|キ|デ|ト|に|ー|ル|ビ|き|ｐ|ジ|ソ|づ|マ|①|'
                'ン|プ|て|な|が|ュ|ス|ｅ|ｔ|し|お|ケ|テ|—|ｎ|レ|ッ|と|ロ|ミ|ェ|オ|ホ|ブ|／|ョ|の|コ|を',
                '', jd_sentence)
            jd_sentence = re.sub('、', '/', jd_sentence)
            jd_sentence = re.sub('，', ',', jd_sentence)
            jd_sentence = re.sub('：', '', jd_sentence)
            jd_sentence = re.sub('；', ';', jd_sentence)
            jd_sentence = re.sub('\n', '', jd_sentence)
            jd_sentence = re.sub('\d/', '', jd_sentence)
            jd_sentence = re.sub('\d\.', '', jd_sentence)
            jd_sentence = re.sub('\xa0', '', jd_sentence)
            jd_sentence = re.sub('岗位职责|岗位要求|工作内容|薪资福利|任职资格|职位描述|职位要求'
                                 '|工作职责|职责描述|任职要求|职位诱惑|职责概述|职责内容|工资待遇|职责表述'
                                 '|职位职责|招聘要求|薪酬福利', '', jd_sentence)
            jd_sentence = jd_sentence.replace(' ', '')
            jd_sentence = jd_sentence.lower()
            jd_text.append(jd_sentence)
        # print(jd_text)
        return jd_text

    def cut_save(self):
        with open('./data/prepare_data/jd.json', 'r', encoding='utf-8')as f1, \
                open('./data/prepare_data/p_two.data', 'w+', encoding='utf-8')as f2, \
                open('./data/prepare_data/p_eight.data', 'w+', encoding='utf-8')as f3:
            lis = []
            for jd in f1:
                # jd_info = json.loads(jd)
                jd_info = eval(jd)

                jd_list = self.extract_jd(jd_info)
                # print(jd_list)
                lis.append(jd_list)
            n = len(lis)
            two = int(n / 4)
            t_li = random.sample(lis, two)
            e_li = [i for i in lis if i not in t_li]
            print(len(t_li))
            print(len(e_li))

            for i in t_li:
                for j in i:
                    f2.write(j)

            for a in e_li:
                for b in a:
                    f3.write(b)

    @staticmethod
    def write_pos_data(jd_list, tech_words, stop_words, crf_file, pos=None):
        for jd in jd_list:
            jieba.load_userdict('./data/change_data/iter_user_dict.data')
            words = list(psg.cut(jd))
            for word, flag in words:
                if word not in stop_words:
                    if all(65 < ord(c) < 122 for c in word):
                        flag = 'eng'
                    if word in tech_words:
                        if flag != 'eng':
                            flag = 'nz'
                        if pos:
                            crf_file.write('{} {} {}'.format(word, flag, '1') + '\n')
                        else:
                            crf_file.write('{} {}'.format(word, flag) + '\n')
                    else:
                        if pos:
                            crf_file.write('{} {} {}'.format(word, flag, '0') + '\n')
                        else:
                            crf_file.write('{} {}'.format(word, flag) + '\n')

    def create_test_data(self):
        """"""
        """
        全文词性标注
        :return: None
        """
        with open('./data/prepare_data/p_eight.data', 'r', encoding='utf-8') as f5:
            with open('./data/crf_data/test.data', 'w+', encoding='utf-8')as f6:
                for i in f5:

                    tech_li = self.load_list('./data/change_data/iter_user_dict.data')
                    stop_li = self.load_list('../Zdata/stopwords.data')
                    self.write_pos_data([i], tech_li, stop_li, f6)

        print('全文分词成功！标注词性成功！保存的测试集文件名为：test.data')

    def create_train_data(self):
        """
        根据已有的标好目标值的数据，将其应用到全部训练集，从而标注好训练集数据
        :return: None
        """
        with open('./data/prepare_data/p_two.data', 'r', encoding='utf-8') as f7:
            with open('./data/crf_data/train.data', 'w+', encoding='utf-8')as f8:
                for i in f7:

                    tech_li = self.load_list('./data/change_data/iter_user_dict.data')
                    stop_li = self.load_list('../Zdata/stopwords.data')
                    self.write_pos_data([i], tech_li, stop_li, f8, pos=True)

        print('成功生成训练集文件：train.data')
        os.unlink('./data/prepare_data/p_eight.data')
        os.unlink('./data/prepare_data/p_two.data')


if __name__ == '__main__':
    tt = TrainTest()
    tt.cut_save()
    tt.create_test_data()
    tt.create_train_data()

import os
import time
import shutil


class TrainPredict(object):
    @staticmethod
    def remove_and_copy():
        if os.path.exists('./test.data'):
            os.unlink('./test.data')

        if os.path.exists('./train.data'):
            os.unlink('./train.data')

        if os.path.exists('./output.txt'):
            os.unlink('./output.txt')

        if os.path.exists('./model'):
            os.unlink('./model')

        print('文件移除成功，移除的文件有：test.data, train.data, output.txt, model')

        shutil.copy("../data/crf_data/test.data", "./")
        shutil.copy("../data/crf_data/train.data", "./")

        print('文件copy成功！其中包括：test.data, train.data')

    @staticmethod
    def fit():
        os.system('crf_learn -a CRF-L2 -f 5 -c 18.0 template train.data model')

        # for i in range(0, 100):
        #     time.sleep(0.005)
        #     print('\r正在准备文件，请稍后：%.2f%%' % (i + 1), end='')

        os.system('crf_test -m model test.data >> output.txt')
        # os.system('pause')

    def show_find_word(self):
        """
        读取预测的数据，挑选出目标值为1的特征值，并添加到列表里
        :return:
        """
        with open('output.txt', 'r', encoding='utf-8') as f:
            word_list = []
            li = f.readlines()
            for i in li:
                i = i[:-1]
                i = i.split('	')
                # print(i)
                if i[-1] == '1':
                    word_list.append(i[0])
            word_set = set(word_list)
            word_list = list(word_set)
            print('发现：', len(word_list), '个词')
            print('新发现的词为', word_list, '\n')

            di = self.show_add_word()
            raw_li = di
            print('原有：', len(raw_li), '个词')
            print('原先的词为：', raw_li, '\n')

            new_li = list()
            for i in word_list:
                if i not in raw_li:
                    new_li.append(i)
            print('增加：', len(new_li), '个词')
            print('新增加的词为：', new_li)
            with open('new.txt', 'w', encoding='utf-8')as f2:
                for j in new_li:

                    f2.write(j + '\n')

    @staticmethod
    def show_add_word():
        lis = list()
        # 将手动标注好的数据，读取到字典里
        with open('../data/change_data/iter_entity.data', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # print(lines)
            for i in lines:
                li = i.strip('\n')
                lis.append(li)
            return lis


if __name__ == '__main__':
    tp = TrainPredict()
    tp.remove_and_copy()
    tp.fit()
    tp.show_find_word()


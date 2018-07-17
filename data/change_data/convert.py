import collections
import re
import os


def convert():
    with open('iter_entity.data', 'r', encoding='utf-8') as f:
        cont = f.readlines()
        li = []
        for i in cont:
            li.append(i.strip().split('\t')[0].lower())
        li = list(set(li))
        print(li)
        print(len(li))

        with open('entity.data', 'w', encoding='utf-8') as f2:
            for j in li:
                f2.write(j + '\n')

        with open('entity.data', 'r', encoding='utf-8') as f4:
            cont2 = f4.readlines()

        with open('iter_user_dict.data', 'w', encoding='utf-8') as f3:
            n = 1800
            for d in cont2:
                w = d.strip().split('\t')[0]
                if 96 < ord(w[0]) < 123:
                    f3.write(w + "\t" + str(n) + '\t' + 'eng' + '\n')
                else:
                    f3.write(w + "\t" + str(n) + '\t' + 'nz' + '\n')

                n -= 1


def origin_entity_appear_times():
    with open('../prepare_data/jd.json', 'rt', encoding='utf-8') as f4:
        content = list()
        for i in f4:
            i = eval(i)
            jd = i['job_description']
            content.append(jd)
        content = str(content)

    with open('./iter_user_dict.data', 'r', encoding='utf-8') as f5:
        with open('./iter_user_dict.txt', 'w', encoding='utf-8') as f6:
            di = dict()
            for i in f5.readlines():
                li = i.strip().split('\t')
                patt = re.compile(li[0] if li[0] != 'c++' else 'c\+\+')
                counter = collections.Counter(patt.findall(str(content)))
                counter_dict = dict(counter.most_common(100000))
                di[li[0]] = counter_dict.get(li[0], 0)
            di = sorted(di.items(), key=lambda x: x[1], reverse=True)
            for j in di:
                word = j[0]
                times = j[1]
                first_word = j[0][0]
                if 96 < ord(first_word) < 123:
                    line = word + '\t' + str(times) + '\t' + 'eng' + '\n'
                else:
                    line = word + '\t' + str(times) + '\t' + 'nz' + '\n'
                f6.write(line)


def user_dict_rename():
    os.unlink('./iter_user_dict.data')
    os.rename('./iter_user_dict.txt', 'iter_user_dict.data')



if __name__ == '__main__':
    convert()
    origin_entity_appear_times()
    user_dict_rename()

import yaml


def convert():
    with open('../data/change_data/iter_user_dict.data', 'r', encoding='utf-8') as f1:
        with open('../../Zdata/word_map.yml', 'r', encoding='utf-8') as f2:
            cont1 = f1.readlines()
            cont2 = f2.read()

            yml_dict = yaml.load(cont2)
            cont3 = dict()
            for i in cont1:
                i = i.strip().split('\t')
                word = yml_dict.get(i[0], i[0])
                if word == i[0]:
                    cont3[i[0]] = int(i[1]) + int(cont3.get(word, 0))
                else:
                    cont3[word] = int(cont3.get(word, 0))
                    cont3[word] += int(i[1])
    return cont3


def write_entity(entity_li):
    with open('./data/pure_entity.data', 'w', encoding='utf-8') as f4:
        di = sorted(entity_li.items(), key=lambda x: x[1], reverse=True)
        for j in di:
            word = j[0]
            times = j[1]
            first_word = j[0][0]
            if 96 < ord(first_word) < 123:
                line = word + '\t' + str(times) + '\t' + 'eng' + '\n'
            else:
                line = word + '\t' + str(times) + '\t' + 'nz' + '\n'
            f4.write(line)


if __name__ == '__main__':
    entity_lis = convert()
    write_entity(entity_lis)

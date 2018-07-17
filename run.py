from Kg_Android.func.entity_userdict import EntityDict
from Kg_Android.func.extract_jd import WriteJD
from Kg_Android.func.save_to_mongodb import SaveToMongodb
from Kg_Android.func.train_test import TrainTest


def create_jd_data():
    """生成初始的jd数据，储存到文件jd.json"""
    wj = WriteJD()
    # 获取每个岗位需求的实际描述
    job = wj.connect_to_mongodb()
    # 将jd提取出来，并装入字典
    li = wj.find_element(job)
    # 去重并写入到文件
    # print(len(li))
    wj.remove_repeat(li)


def create_tag_data_to_mongodb():
    """生成 %5 的标记数据(先分词)，并存入mongodb的test2"""
    sm = SaveToMongodb()
    sm.cut_save()


def run_flask():
    """运行flask,开始标注数据"""
    pass


def create_entity_user_dict():
    """生成技术实体，以及用户词典"""
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


def create_train_test_data():
    """将原始数据生成训练所用的数据 2/8, 并分词标记
        生成训练集数据, 生成测试数据
    """
    tt = TrainTest()
    tt.cut_save()
    tt.create_test_data()
    # tt.pos_train_data()
    tt.create_train_data()


if __name__ == '__main__':
    # 1. 生成初始的jd数据，储存到文件jd.json
    # create_jd_data()

    # 2. 生成 %5 的标记数据(先分词)，并存入mongodb
    # create_tag_data_to_mongodb()

    # 3. run_flask
    # run_flask()

    # 4. 生成技术实体，以及用户词典-------第一次执行这个函数，如果手动抽取的新词，则自己添加到文件中，不用执行这个函数
    # create_entity_user_dict()

    # 迭代：添加新词（手动）---->执行下面5这个函数---->去crf里执行预测---->添加新词（手动）
    # 5. 将原始数据生成训练所用的数据 2/8, 并分词标记,生成训练集数据, 生成测试数据
    create_train_test_data()
    pass













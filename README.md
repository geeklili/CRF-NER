# CRF-NER
使用crf++实现了命名实体识别

## 构建训练集数据

## 构建预测集数据

## 筛选结果


配置文件config：可以配置数据的存取位置
run.py：主控文件

## 运行步骤如下：
    #### 1. 生成初始的jd数据，储存到文件jd.json
    ```create_jd_data()```

    #### 2. 生成 %5 的标记数据(先分词)，并存入mongodb
    ```create_tag_data_to_mongodb()```

    #### 3. run_flask
    ```run_flask()```

    #### 4. 生成技术实体，以及用户词典-------第一次执行这个函数，如果手动抽取的新词，则自己添加到文件中，不用执行这个函数
    ```create_entity_user_dict()```

    #### 迭代：添加新词（手动）---->执行下面5这个函数---->去crf里执行预测---->添加新词（手动）

    #### 5. 将原始数据生成训练所用的数据 2/8, 并分词标记,生成训练集数据, 生成测试数据
    ```create_train_test_data()```


### 预测：
```运行crf.train_model_predict.py即可```

### 迭代：
* 新增加的词位于：new.txt
* 挑选好后，放入data.change_data下的两个文件里
* 执行上面的步骤5------>预测------>添加新词（手动）

### 存入数据库
##### n00_create_pure_entity.py
* 根据yaml文件将错误的技术实体全部替换成正确的技术实体

##### n02_extract_wiki_upword.py
* 爬取技术实体的wiki数据
* 将数据从数据库里取出来
* 消除歧义

##### n03_save_to_neo4j.py
* 保存到图数据库
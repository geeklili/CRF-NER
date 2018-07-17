# coding: utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeSelector

# 链接图数据库
graph = Graph("http://localhost:7474", username="open", password="open")
# 清理数据库里所有的数据
# print('------清空数据库------')
# graph.delete_all()
# print('-------清空完毕-------')
selector = NodeSelector(graph)

# # 创建python实体
# node_python = Node('python', name='Python')
# graph.create(node_python)


with open('./data/up_word_catg.sql', 'r', encoding='utf-8') as f2:
    n = 0
    content = f2.readlines()
    for i in content:
        di = eval(i)
        key = di['search_key']
        li = di['category']

        # 创建技术实体2，并创建其与python实体的关系
        node_2 = selector.select('tech', name=key)
        if list(node_2):
            node_2 = list(node_2)[0]
        else:
            node_2 = Node('tech', name=key)
        graph.create(node_2)
        # nodep2 = Relationship(node_python, 'tec', node_2)
        # graph.create(nodep2)

        print('创建了{}个php实体'.format(n))
        n += 1

        for ct in li:
            # 创建技术实体3，并创建其与实体2的关系
            node_3 = selector.select('category', name=ct)

            # node_3 = graph.find_one(ct)

            if list(node_3):
                node_3 = list(node_3)[0]
            else:
                node_3 = Node('category', name=ct)
            graph.create(node_3)

            node23 = Relationship(node_2, 'is', node_3)
            graph.create(node23)

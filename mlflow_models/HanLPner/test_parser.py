import unittest

from mlflow_models.HanLPner.parser import convert_to_knowledge_graph_spec


class TestParser(unittest.TestCase):

    def test_parser(self):
        model_results: list = [[[['米哈游', 'ARG1', 0, 1], ['成立', 'PRED', 1, 2], ['于2011年', 'ARGM-TMP', 2, 4]],
                                [['米哈游', 'ARG0', 0, 1], ['致力', 'PRED', 5, 6],
                                 ['于为用户提供美好的、超出预期的产品与内容', 'ARG1', 6, 19]],
                                [['为用户', 'ARG2', 7, 9], ['提供', 'PRED', 9, 10],
                                 ['美好的、超出预期的产品与内容', 'ARG1', 10, 19]],
                                [['美好', 'PRED', 10, 11], ['产品与内容', 'ARG0', 16, 19]],
                                [['超出', 'PRED', 13, 14], ['预期', 'ARG1', 14, 15], ['产品与内容', 'ARG0', 16, 19]],
                                [['预期', 'PRED', 14, 15], ['产品与内容', 'ARG1', 16, 19]],
                                [['米哈游', 'ARG0', 20, 21], ['多年来', 'ARGM-TMP', 21, 24], ['秉持', 'PRED', 24, 25],
                                 ['技术自主创新', 'ARG1', 25, 28]],
                                [['技术', 'ARG1', 25, 26], ['自主', 'ARGM-MNR', 26, 27], ['创新', 'PRED', 27, 28]],
                                [['米哈游', 'ARG0', 20, 21], ['多年来', 'ARGM-TMP', 21, 24], ['坚持', 'PRED', 29, 30],
                                 ['走原创精品之路', 'ARG1', 30, 35]],
                                [['走', 'PRED', 30, 31], ['原创精品之路', 'ARG1', 31, 35]],
                                [['米哈游', 'ARG0', 20, 21], ['围绕', 'PRED', 36, 37]],
                                [['米哈游', 'ARG0', 20, 21], ['多年来', 'ARGM-TMP', 21, 24], ['打造', 'PRED', 39, 40],
                                 ['涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链', 'ARG1', 41, 57]],
                                [['涵盖', 'PRED', 41, 42], ['漫画、动画、游戏、音乐、小说及动漫周边', 'ARG1', 42, 54],
                                 ['产业链', 'ARG0', 56, 57]]],
                               [[['我', 'ARG0', 0, 1], ['爱', 'PRED', 1, 2], ['中国', 'ARG1', 2, 3]]]]

        expected_nodes = [
            '米哈游',
            '于为用户提供美好的、超出预期的产品与内容',
            '产品与内容',
            '预期',
            '技术自主创新',
            '走原创精品之路',
            '涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链',
            '产业链',
            '漫画、动画、游戏、音乐、小说及动漫周边',
            '我',
            '中国'
        ]

        expected_links = ['致力', '超出', '秉持', '坚持', '打造', '涵盖', '爱']

        assert [node["fields"]["name"] for node in
                convert_to_knowledge_graph_spec(model_results)["nodes"]] == expected_nodes
        assert [node["fields"]["type"] for node in
                convert_to_knowledge_graph_spec(model_results)["links"]] == expected_links

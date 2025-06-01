import pytest
from src.graph import TextGraph
from src.processor import TextProcessor


def test_white1():
    """测试空图处理: 路径1 (141 → 142 → 143)"""
    # 1. 创建空图
    graph = TextGraph()

    # 2. 计算PageRank
    ranks = TextProcessor.calc_pagerank(graph)

    # 3. 验证结果
    assert ranks == {}

    # 4. 验证节点集合为空
    assert len(graph.nodes) == 0
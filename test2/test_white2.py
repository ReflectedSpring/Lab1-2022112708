import pytest
from src.graph import TextGraph
from src.processor import TextProcessor


def test_white2():
    """测试零迭代: 路径2 (141-142, 145-146, 148, 172-173)"""
    # 1. 创建图: 环状图(A→B, B→C, C→A)
    graph = TextGraph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")

    # 2. 计算PageRank (0次迭代)
    ranks = TextProcessor.calc_pagerank(graph, iterations=0)

    # 3. 验证结果
    assert len(ranks) == 3
    for node, pr_value in ranks.items():
        # 初始PR值应为1/3≈0.3333
        assert pr_value == pytest.approx(0.3333, abs=0.0001)

    # 4. 验证节点集合
    assert set(ranks.keys()) == {"a", "b", "c"}
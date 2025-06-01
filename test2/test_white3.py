import pytest
from src.graph import TextGraph
from src.processor import TextProcessor



def test_white3():
    """测试正常入边贡献: 路径4 (141-142,145-146,148,149-151,154,156,159,160,161,159,164,167,169,172-173)"""
    # 1. 创建图: 环状图(A→B, B→C, C→A)
    graph = TextGraph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")

    # 2. 计算PageRank (1次迭代)
    ranks = TextProcessor.calc_pagerank(graph, iterations=1)

    # 3. 验证结果
    # 所有节点PR值应该大约相等
    assert len(ranks) == 3
    assert ranks["a"] == pytest.approx(0.3333, abs=0.0001)
    assert ranks["b"] == pytest.approx(0.3333, abs=0.0001)
    assert ranks["c"] == pytest.approx(0.3333, abs=0.0001)

    # 4. 验证边权重
    assert graph.get_edges("a")["b"] == 1
    assert graph.get_edges("b")["c"] == 1
    assert graph.get_edges("c")["a"] == 1
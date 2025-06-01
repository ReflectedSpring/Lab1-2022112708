import pytest
from src.graph import TextGraph
from src.processor import TextProcessor



def test_white6():
    """测试多节点迭代: 路径7 (完整的多节点多迭代路径)"""
    # 1. 创建图: 线性图(A→B, B→C, C→D)
    graph = TextGraph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "D")

    # 2. 计算PageRank (不同迭代次数)
    ranks1 = TextProcessor.calc_pagerank(graph, iterations=1)
    ranks2 = TextProcessor.calc_pagerank(graph, iterations=2)
    ranks10 = TextProcessor.calc_pagerank(graph, iterations=10)

    # 3. 验证基本属性
    assert len(ranks1) == 4
    assert len(ranks2) == 4
    assert len(ranks10) == 4

    # 4. 验证结果总和为1 (归一化)
    assert sum(ranks1.values()) == pytest.approx(1.0)
    assert sum(ranks2.values()) == pytest.approx(1.0)
    assert sum(ranks10.values()) == pytest.approx(1.0)

    # 5. 验证迭代次数的影响
    # 终端节点D的PR值应该随着迭代次数增加而增加
    assert ranks10["d"] > ranks2["d"] > ranks1["d"]

    # 6. 验证图结构
    assert graph.out_degree("a") == 1
    assert graph.out_degree("d") == 0  # D是终端节点
import pytest
from src.graph import TextGraph
from src.processor import TextProcessor



def test_white5():
    """测试添加悬挂贡献: 路径6 (141-142,145-146,148,149-151,154,156,159,160,161,159,164,165,167,169,172-173)"""
    # 1. 创建图: (A→B, C) 其中C是悬挂节点
    graph = TextGraph()
    graph.add_edge("A", "B")
    graph.add_edge("C", "C")  # 悬挂节点

    # 2. 计算PageRank
    ranks = TextProcessor.calc_pagerank(graph, iterations=1)

    # 3. 验证结果
    # PR(A) = (1-0.85)/3 + 0.85 * dangling_sum/(3-1)
    # dangling_sum = PR(C) = 1/3 ≈ 0.333
    # PR(A) ≈ 0.05 + 0.85 * (0.333)/2 ≈ 0.05 + 0.14 ≈ 0.19
    assert ranks["a"] > (1 - 0.85) / 3  # 0.05

    # 4. 验证悬挂节点状态
    assert graph.out_degree("c") == 0  # C是悬挂节点
    dangling_sum = sum(ranks[node] for node in graph.nodes if graph.out_degree(node) == 0)
    assert dangling_sum > 0
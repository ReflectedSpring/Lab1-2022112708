import pytest
from src.graph import TextGraph
from src.processor import TextProcessor



def test_white4():
    """测试出度为0的入边: 路径5 (141-142,145-146,148,149-151,154,156,159,160,159,164,167,169,172-173)"""
    # 1. 创建图: (A→B) 其中B是终端节点
    graph = TextGraph()
    graph.add_edge("A", "B")

    # 2. 计算PageRank
    ranks = TextProcessor.calc_pagerank(graph, iterations=1)

    # 3. 验证结果
    # PR(B) = (1-0.85)/2 + 0.85 * PR(A) * 1/1
    # PR(A) ≈ (1-0.85)/2 = 0.075 (因为PR(B)初始=0.5，不贡献给A)
    # PR(B) ≈ 0.075 + 0.85 * 0.5 ≈ 0.5
    assert ranks["b"] == pytest.approx(0.5, abs=0.1)

    # 4. 验证节点出度
    assert graph.out_degree("a") == 1  # A有出边
    assert graph.out_degree("b") == 0  # B无出边
import pytest
from src.graph import TextGraph
from src.processor import TextProcessor

@pytest.fixture
def test_graph():
    graph = TextGraph()
    edges = [
        ("A", "B"), ("A", "B"),
        ("B", "C"), ("B", "C"), ("B", "C"),
        ("A", "D"),
        ("X", "X"),  # 确保X存在
        ("Y", "Y"),  # 添加Y节点 ✅
    ]
    for src, dst in edges:
        graph.add_edge(src, dst)
    return graph


def test_case3_isolated_nodes(test_graph):
    """测试用例3: 孤立节点 X→Y (无路径)"""
    distance, path = TextProcessor.calc_shortest_path(test_graph, "X", "Y")
    assert distance is None
    assert path == []

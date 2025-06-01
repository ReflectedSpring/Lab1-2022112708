import pytest
from src.graph import TextGraph
from src.processor import TextProcessor

@pytest.fixture
def test_graph():
    graph = TextGraph()
    edges = [
        ("A", "B"), ("A", "B"),  # A→B 权重2
        ("B", "C"), ("B", "C"), ("B", "C"),  # B→C 权重3
        ("A", "D"),  # A→D 权重1
       # ("D", "C"),  # D→C 权重1（原为4，改为1使总权重2）
        # 添加孤立节点X和Y
        ("X", "X"),  # 自环边，确保X被加入节点，但无出边
    ]
    for src, dst in edges:
        graph.add_edge(src, dst)
    return graph

def test_case2_same_node(test_graph):
    """测试用例2: 相同节点 A→A"""
    distance, path = TextProcessor.calc_shortest_path(test_graph, "A", "A")
    assert distance == 0
    assert path == ["a"]


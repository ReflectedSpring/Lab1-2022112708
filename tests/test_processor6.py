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


def test_case6_empty_input(test_graph):
    """测试用例6: 输入为空字符串"""
    with pytest.raises(ValueError) as e:
        TextProcessor.calc_shortest_path(test_graph, "", "B")
    assert "输入单词不能为空" in str(e.value)


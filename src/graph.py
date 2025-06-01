# src/graph.py
from collections import defaultdict
from typing import Dict, Set, List, DefaultDict, Tuple

class TextGraph:
    def __init__(self):
        self._out_edges: DefaultDict[str, Dict[str, int]] = defaultdict(dict)
        self._in_edges: DefaultDict[str, Dict[str, int]] = defaultdict(dict)
        self._all_nodes: Set[str] = set()

    def add_edge(self, source: str, target: str) -> None:
        """添加带权边并维护节点集合"""
        source = source.strip().lower()  # 修正原始代码中的拼写错误
        target = target.strip().lower()

        if not source or not target or source == target:
            return

        self._out_edges[source][target] = self._out_edges[source].get(target, 0) + 1
        self._in_edges[target][source] = self._in_edges[target].get(source, 0) + 1
        self._all_nodes.update([source, target])

    @property
    def nodes(self) -> Set[str]:
        """获取所有节点（O(1)时间复杂度）"""
        return self._all_nodes.copy()

    def get_edges(self, node: str) -> Dict[str, int]:
        """获取节点的所有出边（返回防御性拷贝）"""
        return dict(self._out_edges.get(node.lower(), {}))

    def get_in_edges(self, node: str) -> Dict[str, int]:
        """获取节点的所有入边（返回防御性拷贝）"""
        return dict(self._in_edges.get(node.lower(), {}))

    def out_degree(self, node: str) -> int:
        """计算加权出度"""
        return sum(self.get_edges(node).values())

    def contains_word(self, word: str) -> bool:
        """检查单词是否存在于图中"""
        return word.lower() in self._all_nodes

    @property
    def edges(self) -> List[Tuple[str, str, int]]:  # 新增属性
        """获取所有边（来源，目标，权重）"""
        return [
            (src, dst, weight)
            for src, targets in self._out_edges.items()
            for dst, weight in targets.items()
        ]
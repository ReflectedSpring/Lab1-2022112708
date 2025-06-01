# processor.py
import re
import random
import heapq
from typing import List, Optional, Tuple, Dict
import matplotlib.pyplot as plt
import networkx as nx
from src.graph import TextGraph


class TextProcessor:
    # -------------------- 核心处理方法 --------------------

    @staticmethod
    def parse_text(file_path: str) -> List[str]:
        """文本预处理流水线"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 替换所有非字母字符为空格并转为小写
        cleaned = re.sub(r'[^a-zA-Z]', ' ', content).lower()
        return [word for word in cleaned.split() if word]

    @staticmethod
    def build_graph(words: List[str]) -> TextGraph:
        """构建图结构（带输入验证）"""
        if not words or len(words) < 2:
            raise ValueError("输入文本至少需要包含两个有效单词")

        graph = TextGraph()
        for i in range(len(words) - 1):
            graph.add_edge(words[i], words[i + 1])
        return graph

    # -------------------- 桥接词功能 --------------------

    @staticmethod
    def query_bridge_words(graph: TextGraph, word1: str, word2: str) -> Optional[List[str]]:
        """带输入验证的桥接词查询"""
        word1 = word1.strip().lower()
        word2 = word2.strip().lower()

        if not word1 or not word2:
            raise ValueError("输入单词不能为空")

        if not graph.contains_word(word1):
            raise ValueError(f"单词 '{word1}' 不存在于图中")
        if not graph.contains_word(word2):
            raise ValueError(f"单词 '{word2}' 不存在于图中")

        bridges = []
        for candidate in graph.get_edges(word1):
            if word2 in graph.get_edges(candidate):
                bridges.append(candidate)
        return bridges

    # -------------------- 新文本生成 --------------------

    @staticmethod
    def generate_new_text(graph: TextGraph, input_text: str) -> str:
        """带概率选择的文本生成"""
        words = TextProcessor._preprocess_input(input_text)
        if len(words) < 1:
            return ""

        new_words = []
        rand = random.Random()

        for i in range(len(words) - 1):
            current, next_word = words[i], words[i + 1]
            new_words.append(current)

            if not (graph.contains_word(current) and graph.contains_word(next_word)):
                continue

            bridges = TextProcessor.query_bridge_words(graph, current, next_word)
            if bridges:
                new_words.append(rand.choice(bridges))

        new_words.append(words[-1])
        return ' '.join(new_words)

    @staticmethod
    def _preprocess_input(text: str) -> List[str]:
        """统一的输入预处理"""
        text = re.sub(r'[^a-zA-Z]', ' ', text).lower()
        return [w for w in text.split() if w]

    # -------------------- 最短路径算法 --------------------

    @staticmethod
    def calc_shortest_path(graph: TextGraph, src: str, dest: str) -> Tuple[Optional[int], List[str]]:
        """带路径重构的Dijkstra算法"""
        src = src.lower()
        dest = dest.lower()

        if src not in graph.nodes:
            raise ValueError(f"起始节点 '{src}' 不存在")
        if dest not in graph.nodes:
            raise ValueError(f"目标节点 '{dest}' 不存在")
        if src == dest:
            return (0, [src])

        # 初始化数据结构
        dist = {node: float('inf') for node in graph.nodes}
        prev = {node: None for node in graph.nodes}
        dist[src] = 0
        heap = [(0, src)]

        while heap:
            current_dist, u = heapq.heappop(heap)
            if u == dest:
                break
            if current_dist > dist[u]:
                continue

            for v, weight in graph.get_edges(u).items():
                if (new_dist := current_dist + weight) < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(heap, (new_dist, v))

        if dist[dest] == float('inf'):
            return (None, [])

        # 重构路径
        path = []
        current = dest
        while current is not None:
            path.append(current)
            current = prev.get(current)
        path.reverse()

        return (dist[dest], path)

    # -------------------- PageRank算法 --------------------

    def calc_pagerank(graph: TextGraph, damping: float = 0.85, iterations: int = 100) -> Dict[str, float]:
        nodes = list(graph.nodes)
        if not nodes:
            return {}

        n = len(nodes)
        pr = {node: 1.0 / n for node in nodes}

        for _ in range(iterations):
            new_pr = {}
            dangling_nodes = [node for node in nodes if graph.out_degree(node) == 0]
            dangling_sum = sum(pr[node] for node in dangling_nodes)

            # 计算所有节点PR值但不加悬挂贡献
            for node in nodes:
                rank = (1 - damping) / n

                for in_node, weight in graph.get_in_edges(node).items():
                    if (total := graph.out_degree(in_node)) > 0:
                        rank += damping * pr[in_node] * (weight / total)

                new_pr[node] = rank

            # 单独添加悬挂节点贡献（只添加给非悬挂节点）
            for node in nodes:
                if n > 1 and dangling_sum > 0 and node not in dangling_nodes:
                    new_pr[node] += damping * dangling_sum / (n - 1)

            pr = new_pr

        # 归一化处理
        total = sum(pr.values())
        return {k: v / total for k, v in pr.items()}

    # -------------------- 随机游走 --------------------

    # processor.py
    @staticmethod
    def random_walk(graph: TextGraph) -> List[str]:
        """带终止条件的随机游走"""
        path = []  # 确保始终初始化列表
        if not graph.nodes:
            return path  # 返回空列表而非None

        try:
            current = random.choice(list(graph.nodes))
            path = [current]
            visited_edges = set()

            while True:
                edges = graph.get_edges(current)
                if not edges:
                    break

                total = sum(edges.values())
                if total <= 0:  # 处理权重和为零的情况
                    break

                rand_val = random.uniform(0, total)
                cumulative = 0
                next_node = None

                for node, weight in edges.items():
                    cumulative += weight
                    if rand_val <= cumulative:
                        next_node = node
                        break

                if not next_node:
                    break

                edge = (current, next_node)
                if edge in visited_edges:
                    break

                visited_edges.add(edge)
                path.append(next_node)
                current = next_node

        except Exception as e:
            print(f"随机游走异常: {str(e)}")  # 调试日志
            return path  # 返回当前路径

        return path
    # -------------------- 新增绘图方法 --------------------
    @staticmethod
    def draw_graph(
            graph: TextGraph,
            output_path: str = 'src.png',
            layout: str = 'spring',
            node_size: int = 800,
            edge_width: float = 1.2
    ) -> None:
        """生成专业级图可视化

        参数：
            graph: 文本图对象
            output_path: 输出路径（支持.png/.jpg/.pdf等格式）
            layout: 布局算法（spring/circular/random）
            node_size: 节点直径
            edge_width: 基础边宽
        """
        try:
            G = nx.DiGraph()
            G.add_weighted_edges_from(graph.get_all_edges())

            # 布局算法选择
            layout_functions = {
                'spring': nx.spring_layout,
                'circular': nx.circular_layout,
                'random': nx.random_layout
            }
            pos = layout_functions[layout](G, seed=42)

            plt.figure(figsize=(15, 15))

            # 绘制节点
            nx.draw_networkx_nodes(
                G, pos,
                node_size=node_size,
                node_color='#FFD700',
                alpha=0.9,
                linewidths=0.5,
                edgecolors='black'
            )

            # 绘制边（动态调整宽度）
            edge_weights = [d['weight'] * 0.3 for (u, v, d) in G.edges(data=True)]
            nx.draw_networkx_edges(
                G, pos,
                arrows=True,
                arrowstyle='-|>',
                arrowsize=20,
                edge_color='#404040',
                width=[edge_width + w for w in edge_weights]
            )

            # 绘制标签
            nx.draw_networkx_labels(
                G, pos,
                font_size=10,
                font_family='sans-serif',
                font_weight='bold',
                verticalalignment='bottom'
            )

            # 保存输出
            plt.axis('off')
            plt.savefig(
                output_path,
                dpi=300,
                bbox_inches='tight',
                pad_inches=0.1,
                transparent=True
            )
            plt.close()

        except ImportError as e:
            raise RuntimeError("需要安装networkx和matplotlib: pip install networkx matplotlib") from e
        except KeyError as e:
            raise ValueError(f"不支持的布局算法: {layout}") from e
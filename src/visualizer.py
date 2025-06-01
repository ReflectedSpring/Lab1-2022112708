# src/visualizer.py （新建文件）
import os
import matplotlib.pyplot as plt
import networkx as nx
from typing import Optional
from src.graph import TextGraph


class GraphVisualizer:
    @staticmethod
    def save_vector(  # 修正方法名称
        graph: TextGraph,
        origin_file: str,
        format: str = "pdf",
        dpi: int = 300,
        scale: float = 1.0
    ) -> str:
        """
        生成矢量图到源文件同级目录
        参数：
            origin_file: 原始文本文件路径（用于确定输出路径）
            format: 支持pdf/svg/eps
            dpi: 分辨率（默认300）
            scale: 布局缩放因子（0.5-2.0）
        """
        # 生成输出路径
        base_name = os.path.basename(origin_file)
        output_name = f"{os.path.splitext(base_name)[0]}_digraph.{format}"
        output_path = os.path.join(os.path.dirname(origin_file), output_name)

        # 创建有向图
        G = nx.DiGraph()
        G.add_weighted_edges_from(graph.edges)

        # 设置绘图参数
        plt.figure(figsize=(10 * scale, 7 * scale), dpi=dpi)
        pos = nx.spring_layout(G, seed=42, k=0.8 * scale)

        # 绘制节点
        nx.draw_networkx_nodes(
            G, pos,
            node_size=1200,
            node_color="none",
            edgecolors="#666666",
            linewidths=0.8,
            alpha=0.9
        )

        # 绘制标签
        nx.draw_networkx_labels(
            G, pos,
            font_size=10,
            font_family="DejaVu Sans",  # 跨平台兼容字体
            font_weight="bold"
        )

        # 绘制边
        nx.draw_networkx_edges(
            G, pos,
            arrows=True,
            arrowsize=20,
            edge_color="#666666",
            width=[w['weight'] * 0.5 for (u, v, w) in G.edges(data=True)]  # 权重越大线越粗
        )

        # 添加权重标签
        edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_size=8,
            label_pos=0.35
        )

        plt.axis("off")
        plt.savefig(output_path, bbox_inches="tight", dpi=dpi)
        plt.close()

        return output_path
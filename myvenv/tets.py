import networkx as nx
import matplotlib.pyplot as plt

# 测试绘图功能
G = nx.DiGraph()
G.add_edge("A", "B")
nx.draw(G, with_labels=True)
plt.show()
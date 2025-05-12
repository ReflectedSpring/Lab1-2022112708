# text_graph/cli.py
import click
import os
import sys
from typing import Optional
from text_graph.graph import TextGraph
from text_graph.processor import TextProcessor
from text_graph.visualizer import GraphVisualizer

class CLIManager:
    def __init__(self):
        self.graph: Optional[TextGraph] = None
        self.current_file: Optional[str] = None

    def load_graph(self, file_path: str) -> None:
        """加载并缓存图结构"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()  # 验证文件可读性

            words = TextProcessor.parse_text(file_path)
            if len(words) < 2:
                raise ValueError("输入文本至少需要包含两个有效单词")

            self.graph = TextProcessor.build_graph(words)
            self.current_file = os.path.abspath(file_path)
            click.secho(f"✓ 成功加载文件: {self.current_file}", fg='green', bold=True)
            click.echo(f"• 节点数: {len(self.graph.nodes)}")
            click.echo(f"• 边数量: {len(self.graph.edges)}")
        except Exception as e:
            click.secho(f"× 加载失败: {str(e)}", fg='red')
            sys.exit(1)

    def ensure_loaded(self) -> TextGraph:
        """确保图已加载"""
        if not self.graph or not self.current_file:
            click.secho("请先使用 -f 参数加载文件", fg='yellow')
            sys.exit(1)
        return self.graph

cli_manager = CLIManager()

@click.group()
@click.option('-f', '--file', help="输入文本文件路径", required=True)
def cli(file):
    """文本图分析命令行工具"""
    cli_manager.load_graph(file)

@cli.command()
@click.argument('word1')
@click.argument('word2')
def bridge(word1, word2):
    """查询桥接词"""
    graph = cli_manager.ensure_loaded()
    try:
        bridges = TextProcessor.query_bridge_words(graph, word1, word2)
        if bridges:
            click.echo(f"桥接词: {', '.join(bridges)}")
        else:
            click.secho("无桥接词存在", fg='yellow')
    except ValueError as e:
        click.secho(str(e), fg='red')

@cli.command()
@click.argument('text')
def generate(text):
    """生成新文本"""
    graph = cli_manager.ensure_loaded()
    try:
        result = TextProcessor.generate_new_text(graph, text)
        click.echo(f"生成结果: {result}")
    except Exception as e:
        click.secho(f"生成失败: {str(e)}", fg='red')

@cli.command()
@click.argument('start')
@click.argument('end')
def shortest(start, end):
    """计算最短路径"""
    graph = cli_manager.ensure_loaded()
    try:
        distance, path = TextProcessor.calc_shortest_path(graph, start, end)
        if not path:
            click.secho("路径不存在", fg='yellow')
        else:
            click.echo(f"路径: {' → '.join(path)}")
            click.echo(f"总权重: {distance}")
    except ValueError as e:
        click.secho(str(e), fg='red')

@cli.command()
@click.option('--node', help="查询指定节点的PageRank")
def pagerank(node):
    """计算PageRank"""
    graph = cli_manager.ensure_loaded()
    try:
        ranks = TextProcessor.calc_pagerank(graph)
        if node:
            click.echo(f"{node}: {ranks.get(node.lower(), 0):.4f}")
        else:
            for word, rank in sorted(ranks.items(), key=lambda x: -x[1])[:10]:
                click.echo(f"{word}: {rank:.4f}")
    except Exception as e:
        click.secho(f"计算失败: {str(e)}", fg='red')


@cli.command()
@click.option('-o', '--output', help="保存结果到文件")
def walk(output):
    """执行随机游走"""
    graph = cli_manager.ensure_loaded()
    try:
        path = TextProcessor.random_walk(graph)
        if not isinstance(path, list):
            raise ValueError("游走路径返回了无效类型")

        result = ' '.join(path) if path else "空路径"
        if output:
            with open(output, 'w') as f:
                f.write(result)
            click.echo(f"结果已保存至: {output}")
        else:
            click.echo(f"游走路径: {result}")
    except Exception as e:
        click.secho(f"游走失败: {str(e)}", fg='red')
        import traceback
        traceback.print_exc()  # 打印完整堆栈

@cli.command()
@click.option('--format', type=click.Choice(['pdf', 'svg', 'eps']), default='pdf',
             help="输出格式（默认：PDF）")
@click.option('--dpi', default=300, help="分辨率（默认：300）")
@click.option('--scale', default=1.0, type=float,
             help="布局缩放比例（0.5-2.0，默认1.0）")
def draw(format, dpi, scale):
    """生成并保存矢量图"""
    graph = cli_manager.ensure_loaded()
    try:
        output_path = GraphVisualizer.save_vector(
            graph,
            cli_manager.current_file,
            format=format,
            dpi=dpi,
            scale=scale
        )
        click.secho(f"✓ 矢量图已保存到：{output_path}", fg='green')
        click.echo(f"• 格式：{format.upper()}")
        click.echo(f"• 分辨率：{dpi}dpi")
        click.echo(f"• 文件大小：{os.path.getsize(output_path)/1024:.1f}KB")
    except Exception as e:
        click.secho(f"× 生成失败：{str(e)}", fg='red')
        if "findfont" in str(e):
            click.echo("提示：可能需要安装中文字体（如Windows安装SimHei字体）")

if __name__ == '__main__':
    cli()
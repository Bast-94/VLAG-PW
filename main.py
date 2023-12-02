import argparse
import os
import random

import matplotlib.pyplot as plt
import networkx as nx

from src.bron_kerbosch import bron_kerbosch
from src.bron_kerbosch_degeneracy import bron_kerbosch_degeneracy
from src.bron_kerbosch_pivot import bron_kerbosch_pivot

IMG_DIR = "img"


def clique(n_clique):
    for i in range(1, n_clique + 1):
        for j in range(i + 1, n_clique + 1):
            yield (i, j)


def edges_list(n_clique, additional_nodes):
    for i in range(n_clique + 1, n_clique + 1 + additional_nodes):
        yield (
            random.randint(0, n_clique + additional_nodes),
            random.randint(0, n_clique + additional_nodes),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--n-clique", type=int, default=5)
    parser.add_argument("-a", "--additional-nodes", type=int, default=54)
    G = nx.Graph()
    n_clique = parser.parse_args().n_clique
    additional_nodes = parser.parse_args().additional_nodes
    clique_edges = list(clique(n_clique))

    edges = list(edges_list(n_clique, additional_nodes))

    G.add_edges_from(edges + clique_edges)
    bron_kerbosch_funcs = [bron_kerbosch, bron_kerbosch_pivot, bron_kerbosch_degeneracy]
    fig = plt.figure()
    for func in bron_kerbosch_funcs:
        max_clique = func(G)

        cmap = lambda node: "red" if node in max_clique else "blue"
        node_color = list(map(cmap, G.nodes))
        pos = nx.spring_layout(G)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        nx.draw(
            G,
            pos=nx.kamada_kawai_layout(G),
            node_color=node_color,
            with_labels=True,
            node_size=100,
            font_size=10,
            ax=ax,
        )
        ax.set_title(f"Graph with a {len(max_clique)} clique using {func.__name__}")
        fig.savefig(os.path.join(IMG_DIR, f"{func.__name__}.png"))

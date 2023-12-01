import networkx as nx
import random
from src.bron_kerbosch import bron_kerbosch
import matplotlib.pyplot as plt
import os
IMG_DIR = 'img'
def clique(n_clique):
  for i in range(1,n_clique+1):
      for j in range(i+1,n_clique+1):
        yield (i,j)

def edges_list(n_clique, additional_nodes):
  for i in range(n_clique+1, n_clique+1+additional_nodes):

    yield (random.randint(0,n_clique+additional_nodes), random.randint(0,n_clique+additional_nodes))

if __name__ == '__main__':
  G = nx.Graph()
  n_clique= 5
  additional_nodes = 20
  clique_edges = list(clique(n_clique))

  edges = list(edges_list(n_clique, additional_nodes))

  G.add_edges_from(edges+clique_edges)

  max_clique = bron_kerbosch(G)
  cmap = lambda node : 'red' if node in max_clique else 'blue'
  node_color = list(map(cmap,G.nodes))
  pos = nx.spring_layout(G)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  nx.draw(G,pos=pos,node_color=node_color,with_labels=True, node_size=100, font_size=10,ax=ax)
  ax.set_title(f'Graph with a {len(max_clique)} clique')
  fig.savefig(os.path.join(IMG_DIR,'clique.png'))
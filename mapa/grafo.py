import math
from mapa.no import No  
import networkx as nx  
import matplotlib.pyplot as plt  

# EM FALTA: aresta deve ser as seguintes variáveis
# veículos que podem lá passar (se for inacessível, a lista está vazia)
# objeto metereologia (que deve ter int para vento, chuva, inundação)

class Grafo:
    def __init__(self, directed=False):
        self.m_nodes = []  
        self.m_directed = directed
        self.m_graph = {}
        self.m_h = {}  # Dicionário para armazenar as heurísticas de cada nó

    # Método para adicionar uma aresta entre dois nós
    def add_edge(self, node1, node2, weight):
        n1 = No(node1)
        n2 = No(node2)
        
        # Adiciona o nó n1 se não estiver na lista de nós
        if n1 not in self.m_nodes:
            n1.setId(len(self.m_nodes))
            self.m_nodes.append(n1)
            self.m_graph[node1] = []
        
        # Adiciona o nó n2 se não estiver na lista de nós
        if n2 not in self.m_nodes:
            n2.setId(len(self.m_nodes))
            self.m_nodes.append(n2)
            self.m_graph[node2] = []

        # Adiciona a aresta de n1 para n2 com o peso especificado
        self.m_graph[node1].append((node2, weight))
        
        # Se o grafo não for direcionado, adiciona também a aresta de n2 para n1
        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))

    # Adiciona uma heurística para um nó específico
    def add_heuristica(self, n, estima):
        n1 = No(n)
        if n1 in self.m_nodes:
            self.m_h[n] = estima

    # Devolve a heurística do nó, ou um valor alto se não estiver definida
    def getH(self, nodo):
        if nodo not in self.m_h.keys():
            return 1000
        else:
            return self.m_h[nodo]

    # Função para calcular o custo total de um caminho
    def calcula_custo(self, caminho):
        custo = 0
        for i in range(len(caminho) - 1):
            custo += self.get_arc_cost(caminho[i], caminho[i + 1])
        return custo

    # Devolve o custo de uma aresta entre dois nós, se existir
    def get_arc_cost(self, node1, node2):
        for nodo, custo in self.m_graph[node1]:
            if nodo == node2:
                return custo
        return math.inf

    # Devolve os vizinhos de um nó específico no grafo
    def getNeighbours(self, nodo):
        return self.m_graph.get(nodo, [])

    def desenha(self):  # Certifique-se de que está corretamente indentado
            g = nx.Graph()
            for node in self.m_nodes:
                n = node.getName()
                g.add_node(n)
                for (adjacente, peso) in self.m_graph[n]:
                    g.add_edge(n, adjacente, weight=peso)

            pos = nx.spring_layout(g, seed=9, k=0.8)

            # Ajustar manualmente a posição de "Caramoan"
            if "Caramoan" in pos:
                pos["Caramoan"][0] -= 0.2  # Move para a esquerda no eixo X
                pos["Caramoan"][1] += 0.1  # Ajuste no eixo Y

            plt.figure(figsize=(20, 16))
            nx.draw_networkx_nodes(g, pos, node_size=6000, node_color='skyblue', edgecolors='black')
            nx.draw_networkx_labels(g, pos, font_size=10, font_weight='bold', verticalalignment='center')
            nx.draw_networkx_edges(g, pos, width=2, edge_color='gray')
            labels = nx.get_edge_attributes(g, 'weight')
            nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_size=8)
            plt.title("<3 Filipinas <3", fontsize=16)
            plt.axis('off')
            plt.show()
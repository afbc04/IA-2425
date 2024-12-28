import math
from mapa.no import No  
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, directed=False):
        self.m_nodes = []  # Lista de nós
        self.m_directed = directed  # Se o grafo é direcionado
        self.m_graph = {}  # Representação do grafo: {nó: [(adjacente, peso)]}
        self.m_h = {}  # Heurísticas: {nó: valor}

    def _get_or_create_node(self, node_name):
        """
        Obtém um nó existente ou cria um novo nó se ele não existir.
        :param node_name: Nome do nó.
        :return: Objeto No correspondente.
        """
        for node in self.m_nodes:
            if node.getName() == node_name:
                return node

        # Cria um novo nó se não existir
        new_node = No(node_name)
        new_node.setId(len(self.m_nodes))
        self.m_nodes.append(new_node)
        self.m_graph[node_name] = []
        return new_node

    # Calcula a heurística de prioridade
    @staticmethod
    def calcula_heuristica_prioridade(no):
        """
        Calcula a prioridade heurística de um nó com base na população e tempo.
        :param no: Objeto do tipo No.
        :return: Heurística de prioridade.
        """
        if no.janela_tempo <= 0:
            return 0
        return no.populacao / no.janela_tempo

    # Devolve a heurística do nó, ou um valor alto se não estiver definida
    def getH(self, nodo):
        """
        Retorna o valor da heurística associada a um nó.
        :param nodo: Nome do nó.
        :return: Valor da heurística.
        """
        return self.m_h.get(nodo, float('inf'))

    # Função para calcular o custo total de um caminho
    def calcula_custo(self, caminho):
        """
        Calcula o custo total de um caminho no grafo.
        :param caminho: Lista de nós representando o caminho.
        :return: Custo total do caminho.
        """
        custo = 0
        for i in range(len(caminho) - 1):
            custo += self.get_arc_cost(caminho[i], caminho[i + 1])
        return custo

    # Devolve o custo de uma aresta entre dois nós, se existir
    def get_arc_cost(self, node1, node2):
        """
        Retorna o custo de uma aresta entre dois nós.
        :param node1: Nó de origem.
        :param node2: Nó de destino.
        :return: Peso da aresta ou infinito se não existir.
        """
        for adjacente, custo in self.m_graph.get(node1, []):
            if adjacente == node2:
                return custo
        return float('inf')

    # Devolve os vizinhos de um nó específico no grafo
    def getNeighbours(self, nodo):
        """
        Retorna os vizinhos de um nó no grafo.
        :param nodo: Nome do nó.
        :return: Lista de tuplos (vizinho, peso).
        """
        return self.m_graph.get(nodo, [])

    # Retorna o nó com a maior prioridade no grafo
    def get_no_maior_prioridade(self):
        """
        Retorna o nó com a maior prioridade (menor valor da função calcula_prioridade).
        """
        menor_prioridade = float('inf')  # Prioridade menor significa maior urgência
        no_maior_prioridade = None

        for no in self.m_nodes:
            prioridade = no.calcula_prioridade()
            if prioridade < menor_prioridade:
                menor_prioridade = prioridade
                no_maior_prioridade = no

        return no_maior_prioridade

    def desenha(self):
        """
        Gera uma visualização do grafo usando NetworkX e Matplotlib.
        """
        g = nx.Graph()
        for node in self.m_nodes:
            n = node.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g, seed=42, k=0.8)
        plt.figure(figsize=(15, 10))
        nx.draw_networkx_nodes(g, pos, node_size=6000, node_color="skyblue", edgecolors="black")
        nx.draw_networkx_labels(g, pos, font_size=10, font_weight="bold")
        nx.draw_networkx_edges(g, pos, width=2, edge_color="gray")
        labels = nx.get_edge_attributes(g, "weight")
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels, font_size=8)
        plt.title("Mapa de Zonas e Conexões", fontsize=16)
        plt.axis("off")
        plt.show()
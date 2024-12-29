import math
import networkx as nx
import matplotlib.pyplot as plt
from no import No

class Grafo:
    def __init__(self, directed=False):
        self.m_nodes = []  # Lista de nós
        self.m_directed = directed  # Indica se o grafo é direcionado
        self.m_graph = {}  # Representação do grafo: {nó: [(vizinho, peso, bloqueada)]}
        self.m_h = {}  # Heurísticas: {nó: valor}

    def _get_or_create_node(self, node_name):
        """
        Obtém um nó existente ou cria um novo nó se ele não existir.
        """
        for node in self.m_nodes:
            if node.getName() == node_name:
                return node

        new_node = No(node_name)
        new_node.setId(len(self.m_nodes))
        self.m_nodes.append(new_node)
        self.m_graph[node_name] = []
        return new_node

    def add_edge(self, node1, node2, weight, blocked=False):
        """
        Adiciona uma aresta entre dois nós com um peso e estado (bloqueada ou livre).
        """
        print(f"Adicionar aresta: {node1} -> {node2}, Peso: {weight}, Bloqueada: {blocked}")
        n1 = self._get_or_create_node(node1)
        n2 = self._get_or_create_node(node2)

        self.m_graph[node1].append((node2, weight, blocked))
        if not self.m_directed:
            self.m_graph[node2].append((node1, weight, blocked))

    def getNeighbours(self, nodo):
        return [(adjacente, peso) for adjacente, peso, bloqueada in self.m_graph.get(nodo, []) if not bloqueada]

    def get_arc_cost(self, node1, node2):
        for adjacente, custo, bloqueada in self.m_graph.get(node1, []):
            if adjacente == node2:
                return custo if not bloqueada else float('inf')
        return float('inf')

    def calculaDist(self, node1_name, node2_name):
        node1 = next((node for node in self.m_nodes if node.getName() == node1_name), None)
        node2 = next((node for node in self.m_nodes if node.getName() == node2_name), None)

        if node1 and node2:
            coord1 = node1.get_coordenadas()
            coord2 = node2.get_coordenadas()
            return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
        return float('inf')
    
    def calcula_custo(self, caminho):
        custo = 0
        for i in range(len(caminho) - 1):
            custo += self.get_arc_cost(caminho[i], caminho[i + 1])
        return custo

    def calcula_heuristica(self, no):
        destino = self.get_no_maior_prioridade()
        if destino is None:
            return float('inf')

        return self.calculaDist(no.getName(), destino.getName())

    def get_no_maior_prioridade(self):
        menor_prioridade = float('inf')
        no_maior_prioridade = None

        for no in self.m_nodes:
            prioridade = no.calcula_prioridade()
            if prioridade < menor_prioridade:
                menor_prioridade = prioridade
                no_maior_prioridade = no

        return no_maior_prioridade

    def desenha(self):
        """
        Gera uma visualização do grafo usando as coordenadas definidas nos nós.
        """
        g = nx.Graph()

        # Adicionar nós ao grafo NetworkX com coordenadas
        pos = {}
        for node in self.m_nodes:
            g.add_node(node.getName())
            pos[node.getName()] = node.get_coordenadas()  # Usa as coordenadas do JSON

        # Adicionar arestas ao grafo NetworkX
        edge_colors = []
        edge_labels = {}
        for node in self.m_nodes:
            for adjacente, peso, bloqueada in self.m_graph[node.getName()]:
                if not g.has_edge(node.getName(), adjacente):
                    g.add_edge(node.getName(), adjacente, weight=peso)
                    edge_colors.append("red" if bloqueada else "black")
                    edge_labels[(node.getName(), adjacente)] = peso

        # Desenhar o grafo com as coordenadas fornecidas
        plt.figure(figsize=(12, 8))
        nx.draw(
            g,
            pos,
            with_labels=True,
            node_size=3000,
            node_color="skyblue",
            edge_color=edge_colors,
            font_size=10,
            font_weight="bold",
            edgecolors="black",
        )
        nx.draw_networkx_edge_labels(
            g,
            pos,
            edge_labels=edge_labels,
            font_size=8,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"),
        )

        plt.title("Mapa de Zonas e Conexões", fontsize=16)
        plt.axis("off")
        plt.show()

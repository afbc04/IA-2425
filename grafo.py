import math
from no import No  
import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, directed=False):
        self.m_nodes = []  # Lista de nós
        self.m_directed = directed  # Se o grafo é direcionado
        self.m_graph = {}  # Representação do grafo: {nó: [(adjacente, peso)]}
        self.m_h = {}  # Heurísticas: {nó: valor}
        self.m_positions = {} # Coordenadas x e y para cada nó

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

    def add_edge(self, node1, node2, weight, blocked=False):
        """
        Adiciona uma aresta entre dois nós com um peso e estado (bloqueada ou livre).
        """
        print(f"Adicionar aresta: {node1} -> {node2}, Peso: {weight}, Bloqueada: {blocked}")  # Depuração
        n1 = self._get_or_create_node(node1)
        n2 = self._get_or_create_node(node2)

        # Adiciona a aresta com peso e estado
        self.m_graph[node1].append((node2, weight, blocked))
        if not self.m_directed:
            self.m_graph[node2].append((node1, weight, blocked))

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
        Considera o estado da aresta (bloqueada ou livre).
        :param node1: Nó de origem.
        :param node2: Nó de destino.
        :return: Peso da aresta ou infinito se não existir ou estiver bloqueada.
        """
        for adjacente, custo, bloqueada in self.m_graph.get(node1, []):
            if adjacente == node2:
                return custo if not bloqueada else float('inf')  # Retorna custo infinito se a aresta estiver bloqueada
        return float('inf')


    # Devolve os vizinhos de um nó específico no grafo
    def getNeighbours(self, nodo):
        """
        Retorna os vizinhos de um nó no grafo, ignorando arestas bloqueadas.
        """
        return [(adjacente, peso) for adjacente, peso, bloqueada in self.m_graph.get(nodo, []) if not bloqueada]

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
    
    def calculaDist(self, CoordNode1, CoordNode2):
        """
        Retorna a distância em linha reta entre dois nós
        """
        return math.sqrt((CoordNode1[0] - CoordNode2[0])**2 + (CoordNode1[1] - CoordNode2[1])**2)

        # Calcula a heurística de prioridade
    def calcula_heuristica(self, no):
        """
        Calcula a prioridade heurística de um nó com base na população, tempo e coordenadas.
        :param no: Objeto do tipo No.
        :return: Heurística de prioridade.
        """
        # Obtém o nó com a maior prioridade (destino)
        destino = self.get_no_maior_prioridade()

        # Calcular a distancia em linha reta entre dois nós
        coord_no = no.get_coordenadas()
        coord_destino = destino.get_coordenadas()

        dist = self.calculaDist(coord_no, coord_destino)


    def desenha(self):
        """
        Gera uma visualização do grafo usando NetworkX e Matplotlib.
        As arestas livres são desenhadas a preto e as bloqueadas a vermelho.
        """
        g = nx.Graph()
        edge_list = []  # Lista para armazenar as arestas (origem, destino)
        edge_colors = []  # Lista para armazenar as cores das arestas
        edge_labels = {}  # Dicionário para armazenar os pesos das arestas

        # Adicionar nós e arestas ao grafo
        for node in self.m_nodes:
            n = node.getName()
            g.add_node(n)
            for (adjacente, peso, bloqueada) in self.m_graph[n]:
                # Evitar duplicar arestas em grafos não direcionados
                if not g.has_edge(n, adjacente):
                    g.add_edge(n, adjacente)
                    edge_list.append((n, adjacente))  # Adiciona a aresta à lista
                    edge_colors.append("red" if bloqueada else "black")  # Adiciona a cor correspondente
                    edge_labels[(n, adjacente)] = peso  # Associa o peso da aresta

        # Gera a disposição dos nós
        pos = nx.spring_layout(g, seed=42, k=0.8)

        # Desenhar o grafo
        plt.figure(figsize=(15, 10))
        nx.draw_networkx_nodes(g, pos, node_size=6000, node_color="skyblue", edgecolors="black")
        nx.draw_networkx_labels(g, pos, font_size=10, font_weight="bold")
        nx.draw_networkx_edges(g, pos, edgelist=edge_list, edge_color=edge_colors, width=2)
        nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, font_size=8)
        plt.title("Mapa de Zonas e Conexões", fontsize=16)
        plt.axis("off")
        plt.show()

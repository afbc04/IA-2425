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
        self.custos_veiculos = {}  # Dicionário global para custos de veículos

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

    def add_edge(self, node1, node2, weight, blocked=False, permitidos=None):
        """
        Adiciona uma aresta entre dois nós com um peso, estado (bloqueada ou livre) e veículos permitidos.
        """
        permitidos = permitidos or []  # Se não for especificado, assume vazio
        print(f"Adicionar aresta: {node1} -> {node2}, Peso: {weight}, Bloqueada: {blocked}, Veículos Permitidos: {permitidos}")
        n1 = self._get_or_create_node(node1)
        n2 = self._get_or_create_node(node2)

        # Adiciona a aresta com peso, estado e veículos permitidos
        self.m_graph[node1].append((node2, weight, blocked, permitidos))
        if not self.m_directed:
            self.m_graph[node2].append((node1, weight, blocked, permitidos))

    def getNeighbours(self, nodo, veiculo):
        """
        Retorna os vizinhos de um nó no grafo acessíveis com o veículo especificado.
        """
        return [
            (adjacente, peso)
            for adjacente, peso, bloqueada, permitidos in self.m_graph.get(nodo, [])
            if not bloqueada and veiculo in permitidos
        ]

    def get_arc_cost(self, node1, node2, veiculo_tipo):
        """
        Retorna o peso da aresta entre dois nós se o veículo for permitido e a aresta não estiver bloqueada.
        """
        for adjacente, peso, bloqueada, permitidos in self.m_graph.get(node1, []):
            if adjacente == node2:
                if not bloqueada and veiculo_tipo in permitidos:
                    return peso
                else:
                    print(f"Aresta bloqueada ou veículo {veiculo_tipo} não permitido entre {node1} e {node2}")
                    return float('inf')  # Caminho inválido para este veículo
        return float('inf')  # Não existe conexão entre os nós

    def calculaDist(self, node1_name, node2_name):
        node1 = next((node for node in self.m_nodes if node.getName() == node1_name), None)
        node2 = next((node for node in self.m_nodes if node.getName() == node2_name), None)

        if node1 and node2:
            coord1 = node1.get_coordenadas()
            coord2 = node2.get_coordenadas()
            return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
        return float('inf')

    def calcula_custo(self, caminho, veiculo):
        """
        Calcula o custo total de um caminho no grafo para um veículo específico.
        """
        custo_total_arestas = 0

        for i in range(len(caminho) - 1):
            node1 = caminho[i]
            node2 = caminho[i + 1]

            # Obter o custo da aresta entre node1 e node2
            peso = self.get_arc_cost(node1, node2, veiculo.get_tipo())
            if peso == float('inf'):
                print(f"Aresta inválida entre {node1} e {node2} para o veículo {veiculo.get_tipo()}")
                return float('inf')  # Caminho inválido para este veículo

            custo_total_arestas += peso

        # Multiplicar pelo custo do veículo
        custo_veiculo = self.custos_veiculos.get(veiculo.get_tipo(), float('inf'))
        if custo_veiculo == float('inf'):
            print(f"Custo não definido para o veículo {veiculo.get_tipo()}")
            return float('inf')  # Veículo inválido ou custo não definido

        return custo_total_arestas * custo_veiculo

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

    def get_veiculos_no(self, no_name):
        """
        Retorna os veículos associados a um nó específico no grafo, ordenados por custo.
        """
        for node in self.m_nodes:
            if node.getName() == no_name:
                veiculos = node.get_veiculos()
                veiculos.sort(key=lambda v: v.get_custo())  # Ordenar por custo
                return veiculos
        return []

    def calcula_custo(self, caminho, veiculo_tipo):
        """
        Calcula o custo total de um caminho no grafo com base nas arestas.
        """
        custo_total_arestas = 0

        for i in range(len(caminho) - 1):
            node1 = caminho[i]
            node2 = caminho[i + 1]

            # Obter o custo da aresta entre node1 e node2
            peso = self.get_arc_cost(node1, node2, veiculo_tipo)
            if peso == float('inf'):
                print(f"Aresta inválida entre {node1} e {node2} para o veículo {veiculo_tipo}")
                return float('inf')  # Caminho inválido para este veículo

            custo_total_arestas += peso
            print(f"Aresta {node1} -> {node2}, Peso: {peso}, Custo acumulado: {custo_total_arestas}")

        return custo_total_arestas

        # Multiplicar pelo custo do veículo
        custo_veiculo = self.custos_veiculos.get(veiculo.get_tipo(), float('inf'))
        if custo_veiculo == float('inf'):
            return float('inf')  # Veículo inválido ou custo não definido

        return custo_total * custo_veiculo

    def set_custos_veiculos(self, custos):
        """
        Define os custos globais dos veículos.
        """
        self.custos_veiculos = custos

    def desenha(self):
        """
        Gera uma visualização do grafo com informações adicionais.
        """
        plt.ion()  # Ativa o modo interativo

        g = nx.Graph()

        # Adicionar nós ao grafo NetworkX com coordenadas e informações adicionais
        pos = {}
        node_labels = {}
        for node in self.m_nodes:
            g.add_node(node.getName())
            pos[node.getName()] = node.get_coordenadas()  # Usa as coordenadas do JSON
            vehicles = ', '.join([veiculo.get_tipo() for veiculo in node.get_veiculos()])
            node_labels[node.getName()] = f"{node.getName()} ({vehicles})"

        # Identificar o nó de maior prioridade
        no_maior_prioridade = self.get_no_maior_prioridade()
        no_destacado = no_maior_prioridade.getName() if no_maior_prioridade else None

        # Adicionar arestas ao grafo NetworkX
        edge_colors = []
        edge_labels = {}
        for node in self.m_nodes:
            for adjacente, peso, bloqueada, permitidos in self.m_graph[node.getName()]:
                if not g.has_edge(node.getName(), adjacente):
                    g.add_edge(node.getName(), adjacente)
                    edge_colors.append("red" if bloqueada else "black")
                    # Adiciona rótulo com o custo e veículos permitidos
                    edge_labels[(node.getName(), adjacente)] = f"{peso} ({', '.join(permitidos)})"

        # Determinar cores dos nós (vermelho para maior prioridade, azul claro para os demais)
        node_colors = [
            "red" if node.getName() == no_destacado else "skyblue"
            for node in self.m_nodes
        ]

        # Desenhar o grafo com as coordenadas fornecidas
        plt.figure(figsize=(12, 8))
        nx.draw(
            g,
            pos,
            with_labels=True,
            labels=node_labels,
            node_size=7000,
            node_color=node_colors,
            edge_color=edge_colors,
            font_size=9,
            font_weight="bold",
            edgecolors="black",
        )

        # Adicionar rótulos às arestas (custo e veículos permitidos)
        nx.draw_networkx_edge_labels(
            g,
            pos,
            edge_labels=edge_labels,
            font_size=8,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"),
        )

        plt.title("Mapa de Zonas e Conexões", fontsize=16)
        plt.axis("off")
        plt.show(block=False)  # Exibe o grafo sem bloquear o programa

        # Atualiza a janela para refletir mudanças no grafo
        plt.pause(0.1)

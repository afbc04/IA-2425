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

    def get_node_by_name(self, node_name):
        """
        Retorna o nó pelo nome, ou None se o nó não existir.
        """
        for node in self.m_nodes:
            if node.getName() == node_name:
                return node
        return None

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

    def add_edge(self, node1, node2, peso, blocked=False, permitidos=None):
        """
        Adiciona uma aresta entre dois nós com peso, estado (bloqueada ou não) e veículos permitidos.
        """
        permitidos = permitidos or []  # Define uma lista vazia como padrão
        print(f"Adicionar aresta: {node1} -> {node2}, Peso: {peso}, Bloqueada: {blocked}, Permitidos: {permitidos}")

        n1 = self._get_or_create_node(node1)
        n2 = self._get_or_create_node(node2)

        # Adicionar a aresta à estrutura do grafo
        self.m_graph[node1].append((node2, peso, blocked, permitidos))
        if not self.m_directed:
            self.m_graph[node2].append((node1, peso, blocked, permitidos))

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
                    print(f"[DEBUG] Aresta bloqueada ou veículo '{veiculo_tipo}' não permitido entre {node1} e {node2}")
                    return float('inf')  # Caminho inválido para este veículo
        print(f"[DEBUG] Aresta não encontrada entre {node1} e {node2}")
        return float('inf')  # Não existe conexão entre os nós



    def calculaDist(self, node1_name, node2_name):
        node1 = next((node for node in self.m_nodes if node.getName() == node1_name), None)
        node2 = next((node for node in self.m_nodes if node.getName() == node2_name), None)

        if node1 and node2:
            coord1 = node1.get_coordenadas()
            coord2 = node2.get_coordenadas()
            return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)
        return float('inf')

    def calcula_acumulado_arestas(self, caminho, veiculo):
        """
        Calcula a soma total das arestas ao longo do caminho e retorna o valor acumulado.
        Considera apenas arestas válidas para o veículo especificado.
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
            print(f"Aresta {node1} -> {node2}, Peso: {peso}, Custo acumulado: {custo_total_arestas}")

        return custo_total_arestas


    def calcula_custo(self, caminho, veiculo):
        """
        Calcula o custo total de um caminho no grafo considerando:
        - Soma dos pesos das arestas (calculada por calcula_acumulado_arestas).
        - Custo do veículo.
        - Número de pessoas socorridas (respeitando o limite de carga do veículo).
        """
        # Calcular o acumulado das arestas
        custo_total_arestas = self.calcula_acumulado_arestas(caminho, veiculo)
        if custo_total_arestas == float('inf'):
            return float('inf')  # Caminho inválido para este veículo

        origem = self.get_node_by_name(caminho[0])
        destino = self.get_node_by_name(caminho[-1])

        if origem and destino:
            medicamentos_disponiveis = origem.get_medicamento()
            populacao_por_assistir = destino.populacao
            limite_carga = veiculo.get_limite_carga()

            # Debug adicional para validar os valores antes do cálculo
            print(f"[DEBUG] Medicamentos em {caminho[0]}: {medicamentos_disponiveis}, "
                f"População em {caminho[-1]}: {populacao_por_assistir}, Limite do veículo: {limite_carga}")

            # Número de pessoas socorridas
            pessoas_socorridas = min(medicamentos_disponiveis, populacao_por_assistir, limite_carga)

        # Calcular o custo final ajustado
        custo_veiculo = veiculo.get_custo()
        custo_final = custo_total_arestas * (custo_veiculo / pessoas_socorridas)
        print(f"[DEBUG] Veículo: {veiculo.get_tipo()}, Soma das arestas: {custo_total_arestas}, "
            f"Custo do veículo: {custo_veiculo}, Pessoas socorridas: {pessoas_socorridas}, "
            f"Custo final ajustado: {custo_final}")

        return custo_final


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

    def set_custos_veiculos(self, custos):
        """
        Define os custos globais dos veículos.
        """
        self.custos_veiculos = custos

    def atualizar_medicamentos_e_populacao(grafo):
        """
        Ajusta os valores de medicamentos e população para cada nó.
        Se o número de medicamentos é suficiente para atender parte da população,
        os medicamentos são subtraídos e a população restante é ajustada.
        """
        for no in grafo.m_nodes:
            populacao = no.populacao
            medicamentos = no.get_medicamento()

            if medicamentos >= populacao:
                # Todos os medicamentos necessários estão disponíveis
                no.populacao = 0
                no.set_medicamento(medicamentos - populacao)
            else:
                # Medicamentos insuficientes para a população
                no.populacao = populacao - medicamentos
                no.set_medicamento(0)

            print(
                f"Nó {no.getName()}: População atualizada = {no.populacao}, Medicamentos restantes = {no.get_medicamento()}"
            )

    def transferir_medicamentos(self, caminho, veiculo):
        """
        Transfere medicamentos ao longo do caminho especificado.
        Cada transferência considera a capacidade do veículo, a disponibilidade do nó de origem
        e a necessidade do nó de destino.
        """
        for i in range(len(caminho) - 1):
            origem = self.get_node_by_name(caminho[i])
            destino = self.get_node_by_name(caminho[i + 1])

            if not origem or not destino:
                print(f"Erro: Não foi possível encontrar os nós {caminho[i]} ou {caminho[i+1]}")
                continue

            # Determinar a quantidade a transferir
            medicamentos_disponiveis = origem.get_medicamento()
            populacao_por_assistir = destino.populacao
            limite_carga = veiculo.get_limite_carga()

            # A quantidade máxima que pode ser transferida
            quantidade_a_transferir = min(medicamentos_disponiveis, populacao_por_assistir, limite_carga)

            if quantidade_a_transferir > 0:
                # Atualizar os medicamentos do nó de origem
                origem.set_medicamento(medicamentos_disponiveis - quantidade_a_transferir)

                # Atualizar a população e os medicamentos do nó de destino
                destino.set_medicamento(destino.get_medicamento() + quantidade_a_transferir)
                destino.populacao -= quantidade_a_transferir

                print(f"Transferidos {quantidade_a_transferir} medicamentos de {origem.getName()} para {destino.getName()}.")
                print(f"Nó {origem.getName()}: Medicamentos restantes = {origem.get_medicamento()}")
                print(f"Nó {destino.getName()}: População por assistir = {destino.populacao}, Medicamentos = {destino.get_medicamento()}")
            else:
                print(f"Sem transferência possível de {origem.getName()} para {destino.getName()}.")


    def desenha(self):
        """
        Gera uma visualização do grafo.
        """
        plt.ion()  # Ativa o modo interativo

        g = nx.Graph()

        # Adicionar nós ao grafo NetworkX com coordenadas, entre outros
        pos = {}
        node_labels = {}
        for node in self.m_nodes:
            g.add_node(node.getName())
            pos[node.getName()] = node.get_coordenadas()  # Usa as coordenadas do JSON
            vehicles = ', '.join([veiculo.get_tipo() for veiculo in node.get_veiculos()])
            medicamentos = node.get_medicamento()  # Obtém o número de medicamentos corretamente
            populacao = node.populacao  # Obtém a população do nó
            node_labels[node.getName()] = (
                f"{node.getName()}\n"
                f"População: {populacao}\n"
                f"Medicamentos: {medicamentos}\n"
                f"Veículos: {vehicles}"
            )

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
                    edge_labels[(node.getName(), adjacente)] = f"{peso} ({', '.join(permitidos)})"

        # Criar a figura do grafo
        plt.figure(figsize=(12, 8))

        # Desenhar as arestas
        nx.draw_networkx_edges(
            g,
            pos,
            edge_color=edge_colors,
        )

        # Adicionar rótulos às arestas
        nx.draw_networkx_edge_labels(
            g,
            pos,
            edge_labels=edge_labels,
            font_size=8,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"),
        )

        # Adicionar retângulos como nós
        ax = plt.gca()
        rect_width = 0.8  # Largura do retângulo
        rect_height = 0.6  # Altura do retângulo
        for node, (x, y) in pos.items():
            rect = plt.Rectangle(
                (x - rect_width / 2, y - rect_height / 2),  # Posição inicial (centro menos metade da largura/altura)
                rect_width,
                rect_height,
                edgecolor="black",
                facecolor="red" if node == no_destacado else "skyblue",
                zorder=2,
            )
            ax.add_patch(rect)
            ax.text(
                x, y, node_labels[node],
                verticalalignment="center", horizontalalignment="center",
                fontsize=9, zorder=3, color="black",
            )

        # Ajustar os limites do gráfico
        plt.title("Mapa de Zonas e Conexões", fontsize=16)
        plt.axis("off")
        plt.xlim(min(x for x, y in pos.values()) - 1, max(x for x, y in pos.values()) + 1)
        plt.ylim(min(y for x, y in pos.values()) - 1, max(y for x, y in pos.values()) + 1)

        plt.show(block=False)  # Exibe o grafo sem bloquear o programa
        plt.pause(0.1)

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

        # Atualizar heurísticas com base no nó de maior prioridade
        no_destino = self.get_no_maior_prioridade()
        if no_destino:
            self.atualizar_heuristicas(no_destino)
        else:
            print("[INFO] Nenhum nó de maior prioridade disponível no momento.")

    def get_node_by_name(self, nome_no):
        """
        Retorna o nó pelo nome, ou None se o nó não existir.
        """
        for node in self.m_nodes:
            if node.getNome() == nome_no:
                return node
        return None

    def _get_or_create_node(self, nome_no):
        """
        Obtém um nó existente ou cria um novo nó se ele não existir.
        """
        for node in self.m_nodes:
            if node.getNome() == nome_no:
                return node

        new_node = No(nome_no)
        new_node.setId(len(self.m_nodes))
        self.m_nodes.append(new_node)
        self.m_graph[nome_no] = []
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

        return custo_total_arestas


    def calcula_custo(self, caminho, veiculo):
        """
        Calcula o custo total de um caminho no grafo considerando:
        - Soma dos pesos das arestas (calculada por calcula_acumulado_arestas).
        - Custo do veículo.
        - Número de pessoas socorridas (respeitando o limite de carga do veículo).
        """
        custo_total_arestas = self.calcula_acumulado_arestas(caminho, veiculo)
        if custo_total_arestas == float('inf'):
            return float('inf')

        origem = self.get_node_by_name(caminho[0])
        destino = self.get_node_by_name(caminho[-1])

        if origem and destino:
            medicamentos_disponiveis = origem.get_medicamento()
            populacao_por_assistir = destino.populacao
            limite_carga = veiculo.get_limite_carga()

            print(f"[DEBUG] Medicamentos em {caminho[0]}: {medicamentos_disponiveis}, "
                f"População em {caminho[-1]}: {populacao_por_assistir}, Limite do veículo: {limite_carga}")

            pessoas_socorridas = min(medicamentos_disponiveis, populacao_por_assistir, limite_carga)

            if pessoas_socorridas == 0:
                return float('inf'), 0

            custo_veiculo = veiculo.get_custo()
            custo_final = custo_total_arestas * (custo_veiculo / pessoas_socorridas)
            print(f"[DEBUG] Veículo: {veiculo.get_tipo()}, Soma das arestas: {custo_total_arestas}, "
                f"Custo do veículo: {custo_veiculo}, Pessoas socorridas: {pessoas_socorridas}, "
                f"Custo final ajustado: {custo_final}")

            return custo_final, pessoas_socorridas

    def atualizar_heuristicas(self, no_destino):
        """
        Atualiza a heurística de cada nó no grafo, considerando o nó de maior prioridade como destino.
        Nós com população igual a 0 recebem heurística infinita.
        """
        if no_destino is None:
            print("[ERRO] Nenhum nó de destino válido para calcular heurísticas.")
            return

        self.m_h = {}
        for no in self.m_nodes:
            if no.populacao == 0 or no.janela_tempo == 0:  # Nós com população ou tempo esgotado recebem inf
                heuristica = float('inf')
            else:
                heuristica = self.calcula_heuristica(no, no_destino)
            
            self.m_h[no.getNome()] = heuristica
            print(f"[DEBUG] Heurística do nó '{no.getNome()}': {heuristica:.6f}")

    def calcula_heuristica(self, no_origem, no_destino):
        """
        Calcula a heurística de um nó como a combinação da distância euclidiana ao destino
        multiplicada pela prioridade do próprio nó de origem.

        Fórmula: distância_euclidiana * prioridade_no_origem
        """
        x_origem, y_origem = no_origem.x, no_origem.y
        x_destino, y_destino = no_destino.x, no_destino.y

        # Distância euclidiana entre os nós
        distancia_euclidiana = ((x_destino - x_origem) ** 2 + (y_destino - y_origem) ** 2) ** 0.5

        # Prioridade do nó de origem
        prioridade_no_origem = no_origem.calcula_prioridade()

        if prioridade_no_origem == float('inf'):
            return float('inf')

        # Heurística final
        return distancia_euclidiana * prioridade_no_origem

    def get_no_maior_prioridade(self):
        menor_prioridade = float('inf')
        no_maior_prioridade = None

        for no in self.m_nodes:
            prioridade = no.calcula_prioridade()
            if prioridade < menor_prioridade:
                menor_prioridade = prioridade
                no_maior_prioridade = no

        return no_maior_prioridade

    def get_veiculos_no(self, no_nome):
        """
        Retorna os veículos associados a um nó específico no grafo, ordenados por custo.
        """
        for node in self.m_nodes:
            if node.getNome() == no_nome:
                veiculos = node.get_veiculos()
                veiculos.sort(key=lambda v: v.get_custo())  # Ordenar por custo
                return veiculos
        return []

    def set_custos_veiculos(self, custos):
        """
        Define os custos globais dos veículos.
        """
        self.custos_veiculos = custos

    def atualizar_medicamentos_e_populacao(self):
        """
        Ajusta os valores de medicamentos e população para cada nó.
        Se o número de medicamentos é suficiente para atender parte da população,
        os medicamentos são subtraídos e a população restante é ajustada.
        Quando a população de um nó é 0, a janela_tempo é ajustada para 24.
        """
        for no in self.m_nodes:
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

            # Ajustar janela_tempo para 24 se a população for 0
            if no.populacao == 0:
                no.janela_tempo = 24

            print(
                f"Nó {no.getNome()}: População atualizada = {no.populacao}, "
                f"Medicamentos restantes = {no.get_medicamento()}, "
                f"Janela de tempo = {no.janela_tempo}"
            )

    def transferir_valores(grafo, valor, no_origem, no_destino):
        origem = grafo.get_node_by_name(no_origem)
        destino = grafo.get_node_by_name(no_destino)

        if not origem or not destino:
            print(f"Erro: Não foi possível encontrar os nós '{no_origem}' ou '{no_destino}'.")
            return False

        # Determinar a quantidade que pode ser transferida
        quantidade_transferir = min(origem.get_medicamento(), valor, destino.populacao)

        if quantidade_transferir <= 0:
            print(f"Transferência impossível entre '{no_origem}' e '{no_destino}'. "
                f"Medicamentos disponíveis: {origem.get_medicamento()}, População no destino: {destino.populacao}.")
            return False

        # Realizar a transferência
        origem.set_medicamento(origem.get_medicamento() - quantidade_transferir)
        destino.populacao -= quantidade_transferir

        print(f"Transferidos {quantidade_transferir} medicamentos de '{no_origem}' para '{no_destino}'.")
        print(f"Medicamentos restantes no nó de origem '{no_origem}': {origem.get_medicamento()}.")
        print(f"População restante no nó de destino '{no_destino}': {destino.populacao}.")
        
        return True

    def desenha(self, destaque_azul=False):
        """
        Atualiza a visualização do grafo, incluindo informações adicionais como janela de tempo,
        com retângulos maiores para os nós.
        """
        plt.ion()  # Ativa o modo interativo

        # Limpar a figura atual antes de redesenhar
        plt.clf()

        # Atualizar as heurísticas para todos os nós
        no_destino = self.get_no_maior_prioridade()
        if no_destino:
            self.atualizar_heuristicas(no_destino)
        else:
            print("[ERRO] Não foi possível determinar o nó de maior prioridade para calcular heurísticas.")

        g = nx.Graph()

        # Adicionar nós ao grafo NetworkX com coordenadas e informações
        pos = {}
        node_labels = {}
        for node in self.m_nodes:
            g.add_node(node.getNome())
            pos[node.getNome()] = node.get_coordenadas()  # Usa as coordenadas do JSON
            vehicles = ', '.join([veiculo.get_tipo() for veiculo in node.get_veiculos()])
            medicamentos = node.get_medicamento()  # Obtém o número de medicamentos corretamente
            populacao = node.populacao  # Obtém a população do nó
            janela = node.janela_tempo  # Obtém a janela de tempo do nó
            node_labels[node.getNome()] = (
                f"{node.getNome()}\n"
                f"População: {populacao}\n"
                f"Medicamentos: {medicamentos}\n"
                f"Janela: {janela}\n"
                f"Veículos: {vehicles}"
            )

        # Identificar o nó de maior prioridade
        no_destacado = no_destino.getNome() if no_destino else None

        # Adicionar arestas ao grafo NetworkX
        edge_colors = []
        edge_labels = {}
        for node in self.m_nodes:
            for adjacente, peso, bloqueada, permitidos in self.m_graph[node.getNome()]:
                if not g.has_edge(node.getNome(), adjacente):
                    g.add_edge(node.getNome(), adjacente)
                    edge_colors.append("red" if bloqueada else "black")
                    edge_labels[(node.getNome(), adjacente)] = f"{peso} ({', '.join(permitidos)})"

        # Criar a figura do grafo
        plt.figure(1)  # Usa a mesma figura

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
        rect_width = 1.2  # Aumentar largura do retângulo
        rect_height = 0.8  # Aumentar altura do retângulo
        for node, (x, y) in pos.items():
            if destaque_azul:
                cor = "blue"
            elif node == no_destacado:
                cor = "red"
            elif self.get_node_by_name(node).janela_tempo == 0:  # Nó com tempo 0 fica preto
                cor = "black"
            else:
                cor = "skyblue"

            rect = plt.Rectangle(
                (x - rect_width / 2, y - rect_height / 2),  # Posição inicial (centro menos metade da largura/altura)
                rect_width,
                rect_height,
                edgecolor="black",
                facecolor=cor,
                zorder=2,
            )
            ax.add_patch(rect)
            ax.text(
                x, y, node_labels[node],
                verticalalignment="center", horizontalalignment="center",
                fontsize=9, zorder=3, color="white" if cor == "black" else "black",
            )

        # Adicionar a lista de heurísticas no canto inferior esquerdo
        heuristicas_texto = "Heurísticas:\n"
        for no, heuristica in self.m_h.items():
            heuristicas_texto += f"{no}: {heuristica:.5f}\n"

        plt.text(
            0.01, 0.01,  # Coordenadas no canto inferior esquerdo
            heuristicas_texto,
            fontsize=10,
            color="black",
            ha="left",
            va="bottom",
            transform=plt.gcf().transFigure,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="black"),
        )

        # Adicionar a lista de prioridades no canto superior esquerdo
        prioridades_texto = "Prioridades:\n"
        for no in sorted(self.m_nodes, key=lambda n: n.calcula_prioridade()):
            prioridade = no.calcula_prioridade()
            prioridades_texto += f"{no.getNome()}: {prioridade:.5f}\n"

        plt.text(
            0.01, 0.99,  # Coordenadas no canto superior esquerdo
            prioridades_texto,
            fontsize=10,
            color="black",
            ha="left",
            va="top",
            transform=plt.gcf().transFigure,
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="black"),
        )

        # Ajustar os limites do gráfico
        plt.title("Mapa de Zonas e Conexões", fontsize=16)
        plt.axis("off")
        plt.xlim(min(x for x, y in pos.values()) - 1, max(x for x, y in pos.values()) + 1)
        plt.ylim(min(y for x, y in pos.values()) - 1, max(y for x, y in pos.values()) + 1)

        plt.draw()  # Atualiza o gráfico
        plt.pause(0.1)

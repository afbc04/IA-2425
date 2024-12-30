import math
from queue import Queue
from collections import deque
from grafo import Grafo  

def procura_DFS(grafo, inicio, fim, path=None, visited=None, veiculo_atual=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    path = path + [inicio]
    visited.add(inicio)

    # Verifica destino
    if inicio == fim:
        custo = grafo.calcula_custo(path, veiculo_atual)
        return {veiculo_atual.get_tipo(): (path, custo)}

    if veiculo_atual is None:
        veiculos_disponiveis = grafo.get_veiculos_no(inicio)
        veiculos_disponiveis.sort(key=lambda v: v.get_custo())  # Ordenar veículos por custo
    else:
        veiculos_disponiveis = [veiculo_atual]  # Continuar com o veículo já em uso

    for veiculo in veiculos_disponiveis:
        # Explorar vizinhos do nó atual
        for (adjacente, peso, bloqueada, permitidos) in grafo.m_graph[inicio]:
            if adjacente not in visited:
                # Validar veículo permitido na aresta
                if not bloqueada and veiculo.get_tipo() in permitidos:
                    # Chamada recursiva com o veículo atual
                    novo_caminho = procura_DFS(grafo, adjacente, fim, path, visited, veiculo)
                    if novo_caminho:
                        return novo_caminho

    return None  # Nenhum caminho válido encontrado

def procura_BFS(grafo, inicio, fim):
    queue = [(inicio, [inicio], None)]  # (nó atual, caminho até agora, veículo usado)
    visited = set()

    while queue:
        nodo_atual, path, veiculo_atual = queue.pop(0)  # Retira o primeiro elemento da fila
        visited.add(nodo_atual)

        # Verifica se já chegamos ao destino
        if nodo_atual == fim:
            custo = grafo.calcula_custo(path, veiculo_atual)
            return {veiculo_atual.get_tipo(): (path, custo)}

        # Obter veículos disponíveis no nó inicial apenas na primeira iteração
        if veiculo_atual is None:
            veiculos_disponiveis = grafo.get_veiculos_no(nodo_atual)
            veiculos_disponiveis.sort(key=lambda v: v.get_custo())  # Ordenar veículos por custo
        else:
            veiculos_disponiveis = [veiculo_atual]

        # Explorar vizinhos
        for veiculo in veiculos_disponiveis:
            for (adjacente, peso, bloqueada, permitidos) in grafo.m_graph[nodo_atual]:
                if adjacente not in visited:
                    # Validar veículo permitido na aresta
                    if not bloqueada and veiculo.get_tipo() in permitidos:
                        # Adiciona o vizinho à fila com o veículo atual
                        queue.append((adjacente, path + [adjacente], veiculo))

    return None  # Nenhum caminho válido encontrado

# Algoritmo A*
def procura_aStar(grafo, start, end):
    open_list = {start}
    closed_list = set()
    g = {start: 0}
    parents = {start: start}

    # Obtém os veículos disponíveis no nó inicial
    veiculos_disponiveis = grafo.get_veiculos_no(start)
    if not veiculos_disponiveis:
        print(f"Nó {start} não possui veículos disponíveis.")
        return None, math.inf

    for veiculo_atual in veiculos_disponiveis:
        print(f"Tentar a procura com o veículo: {veiculo_atual}")

        #reiniciar as listas
        open_list = {start}
        closed_list = set()
        g = {start: 0}
        parents = {start: start}

        while open_list:
            # Usa a heurística baseada em calculaDist
            n = min(open_list, key=lambda v: g[v] + grafo.calculaDist(v, end))
            if n == end:
                caminho = []
                while parents[n] != n:
                    caminho.append(n)
                    n = parents[n]
                caminho.append(start)
                return caminho[::-1], grafo.calcula_custo(caminho[::-1], veiculo_atual)

            open_list.remove(n)
            closed_list.add(n)

            for m, weight in grafo.getNeighbours(n, veiculo_atual):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                elif g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n
                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

    return None, math.inf

# Algoritmo procura gulosa
def greedy(grafo, start, end):
    open_list = {start}
    closed_list = set()
    parents = {start: start}

    # Obtém os veículos disponíveis no nó inicial
    veiculos_disponiveis = grafo.get_veiculos_no(start)
    if not veiculos_disponiveis:
        print(f"Nó {start} não possui veículos disponíveis.")
        return None, math.inf

    for veiculo_atual in veiculos_disponiveis:
        print(f"Tentando a procura com o veículo: {veiculo_atual}")

        # Reiniciar as listas para cada veículo
        open_list = {start}
        closed_list = set()
        parents = {start: start}

        while open_list:
            # Pega o nó com o menor custo (com base na heurística de distância para o final)
            n = min(open_list, key=lambda v: grafo.calculaDist(v, end))

            # Se o destino for alcançado, construa o caminho
            if n == end:
                caminho = []
                while parents[n] != n:
                    caminho.append(n)
                    n = parents[n]
                caminho.append(start)
                caminho.reverse()
                return caminho, grafo.calcula_custo(caminho, veiculo_atual)

            open_list.remove(n)
            closed_list.add(n)

            # Explora os vizinhos do nó atual
            for m, weight in grafo.getNeighbours(n, veiculo_atual):
                # Verifica se o vizinho não foi visitado e não está na lista de fechados
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

    return None, math.inf
import math
from queue import Queue
from grafo import Grafo  

# Algoritmo de procura em profundidade (DFS)
def procura_DFS(grafo, start, end, path=None, visited=None):
    if path is None:
        path = []
    if visited is None:
        visited = set()

    # Adiciona o nó atual ao caminho e marca como visitado
    path = path + [start]
    visited.add(start)

    # Obtém os veículos disponíveis no nó atual
    veiculos_disponiveis = grafo.get_veiculos_no(start)
    if not veiculos_disponiveis:
        print(f"Nó {start} não possui veículos disponíveis.")
        return None, math.inf

    # Itera por todos os veículos disponíveis
    for veiculo_atual in veiculos_disponiveis:
        print(f"Visitando: {start} com o veículo: {veiculo_atual}, Caminho atual: {path}")

        # Caso base: destino encontrado
        if start == end:
            print(f"Destino encontrado: {end}")
            custo = grafo.calcula_custo(path, veiculo_atual)
            if custo == float('inf'):
                print(f"O veículo '{veiculo_atual}' não pode ser usado em todas as arestas do caminho.")
                continue  # Tenta o próximo veículo
            return path, custo

        # Explora os vizinhos do nó atual
        caminho_valido = False
        for adjacente, peso in grafo.getNeighbours(start, veiculo_atual):
            if adjacente not in visited:
                resultado = procura_DFS(grafo, adjacente, end, path, visited)
                if resultado[0] is not None:  # Caminho encontrado
                    caminho_valido = True
                    return resultado

        # Se nenhum vizinho for válido, tenta o próximo veículo
        if not caminho_valido:
            print(f"Nó {start} não possui caminhos válidos para o destino {end} com o veículo {veiculo_atual}.")

    return None, math.inf

# Algoritmo de procura em largura (BFS)
def procura_BFS(grafo, start, end):
    visited = set()
    fila = Queue()
    fila.put((start, [start]))  # A fila mantém o nó atual e o caminho até ele

    # Obtém os veículos disponíveis no nó inicial
    veiculos_disponiveis = grafo.get_veiculos_no(start)
    if not veiculos_disponiveis:
        print(f"Nó {start} não possui veículos disponíveis.")
        return None, math.inf

    for veiculo_atual in veiculos_disponiveis:
        print(f"Tentar a procura com o veículo: {veiculo_atual}")

        while not fila.empty():
            nodo_atual, path = fila.get()
            
            if nodo_atual == end:
                custo = grafo.calcula_custo(path, veiculo_atual)
                if custo == float('inf'): # veículo atual não é capaz de percorrer a aresta
                    print(f"O veículo '{veiculo_atual}' não pode ser usado em todas as arestas do caminho.")
                    break  # Tenta o próximo veículo
                return path, custo

            for adjacente, peso in grafo.getNeighbours(nodo_atual, veiculo_atual):
                if adjacente not in visited:
                    visited.add(adjacente)
                    fila.put((adjacente, path + [adjacente]))

    return None, math.inf

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
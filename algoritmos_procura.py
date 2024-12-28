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

    # Imprime o progresso para depuração
    print(f"Visitando: {start}, Caminho atual: {path}")

    # Caso base: destino encontrado
    if start == end:
        print(f"Destino encontrado: {end}")
        return path, grafo.calcula_custo(path)

    # Explora os vizinhos do nó atual
    for adjacente, peso in grafo.getNeighbours(start):
        if adjacente not in visited:
            resultado = procura_DFS(grafo, adjacente, end, path, visited)
            if resultado[0] is not None:  # Caminho encontrado
                return resultado

    # Se não encontrar o caminho, retorna None
    print(f"Retornando sem sucesso de: {start}")
    return None, math.inf

# Algoritmo de procura em largura (BFS)
def procura_BFS(grafo, start, end):
    visited = set()
    fila = Queue()
    fila.put((start, [start]))

    while not fila.empty():
        nodo_atual, path = fila.get()
        if nodo_atual == end:
            return path, grafo.calcula_custo(path)

        for adjacente, peso in grafo.getNeighbours(nodo_atual):
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

    while open_list:
        n = min(open_list, key=lambda v: g[v] + grafo.getH(v))
        if n == end:
            caminho = []
            while parents[n] != n:
                caminho.append(n)
                n = parents[n]
            caminho.append(start)
            return caminho[::-1], grafo.calcula_custo(caminho[::-1])

        open_list.remove(n)
        closed_list.add(n)

        for m, weight in grafo.getNeighbours(n):
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

# Algoritmo Greedy usando a heurística definida no grafo
def greedy(grafo, start, end):
    open_list = {start}
    closed_list = set()
    parents = {start: start}

    while open_list:
        n = min(open_list, key=lambda v: grafo.getH(v))

        if n == end:
            caminho = []
            while parents[n] != n:
                caminho.append(n)
                n = parents[n]
            caminho.append(start)
            caminho.reverse()
            return caminho, grafo.calcula_custo(caminho)

        open_list.remove(n)
        closed_list.add(n)

        for m, weight in grafo.getNeighbours(n):
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n

    return None, math.inf  

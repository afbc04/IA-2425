import math
from queue import Queue
from mapa.grafo import Grafo  

# Algoritmo de procura em profundidade (DFS)
def procura_DFS(grafo, start, end, path=[], visited=set()):
    path = path + [start]
    visited.add(start)

    if start == end:
        return path, grafo.calcula_custo(path)

    for adjacente, peso in grafo.getNeighbours(start):
        if adjacente not in visited:
            resultado = procura_DFS(grafo, adjacente, end, path, visited)
            if resultado is not None:
                return resultado
    return None

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

# Algoritmo A* usando a heurística definida no grafo
def procura_aStar(grafo, start, end):
    open_list = {start}
    closed_list = set()
    g = {start: 0}
    parents = {start: start}

    while open_list:
        n = min(open_list, key=lambda v: g[v] + grafo.getH(v))

        if n == end:
            reconst_path = []
            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]
            reconst_path.append(start)
            reconst_path.reverse()
            return reconst_path, grafo.calcula_custo(reconst_path)

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

    return None

# Algoritmo Greedy usando a heurística definida no grafo
def greedy(grafo, start, end):
    open_list = {start}
    closed_list = set()
    parents = {start: start}

    while open_list:
        n = min(open_list, key=lambda v: grafo.getH(v))

        if n == end:
            reconst_path = []
            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]
            reconst_path.append(start)
            reconst_path.reverse()
            return reconst_path, grafo.calcula_custo(reconst_path)

        open_list.remove(n)
        closed_list.add(n)

        for m, weight in grafo.getNeighbours(n):
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n

    return None

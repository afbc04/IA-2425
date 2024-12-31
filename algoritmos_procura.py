import math
from queue import Queue
from collections import deque
from grafo import Grafo  

import math
from queue import Queue
from collections import deque
from grafo import Grafo

def procura_DFS(grafo, inicio, fim):
    """
    Realiza a busca em profundidade (DFS) para encontrar o melhor caminho
    considerando todos os veículos disponíveis no nó inicial.
    Retorna o melhor caminho com base no custo mais baixo.
    """
    no_origem = grafo.get_node_by_name(inicio)
    if no_origem.janela_tempo == 0:
        print(f"[ERRO] O nó de origem '{inicio}' não pode ser utilizado porque o tempo esgotou.")
        return None

    if no_origem.get_medicamento() == 0:
        print(f"[ERRO] NINGUÉM FOI SOCORRIDO, NÓ ORIGEM SEM MEDICAMENTOS: '{inicio}'")
        return None

    veiculos_disponiveis = grafo.get_veiculos_no(inicio)
    if not veiculos_disponiveis:
        print(f"Nó {inicio} não possui veículos disponíveis.")
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"Usando veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()})")
        stack = [(inicio, [inicio])]  # Pilha para DFS (nó atual, caminho até agora)
        visited = set()

        while stack:
            nodo_atual, caminho = stack.pop()
            if nodo_atual in visited:
                continue

            visited.add(nodo_atual)
            print(f"DFS: Visitando {nodo_atual}, Caminho atual: {caminho}")

            # Se o destino foi alcançado
            if nodo_atual == fim:
                custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
                if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}. ")
                else:
                    destino = grafo.get_node_by_name(fim)
                    tempo_destino = destino.janela_tempo
                    if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}. ")
                        continue

                    custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                    if custo_final == float('inf'):
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho: {caminho}.")
                    else:
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} PODE COMPLETAR o caminho: {caminho}. Custo final: {custo_final}")

                        melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas))
                continue

            # Adicionar vizinhos acessíveis à pilha
            vizinhos = [
                (adjacente, caminho + [adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]
            for adjacente, novo_caminho in reversed(vizinhos):
                stack.append((adjacente, novo_caminho))
                print(f"Vizinho {adjacente} adicionado à pilha com caminho: {novo_caminho}")

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")

        # Transferir valores apenas para o melhor veículo
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)

        capacidade_restante = veiculo.get_limite_carga() - pessoas_socorridas

        nos_intermediarios = sorted(
            caminho[1:-1],
            key=lambda no: grafo.get_node_by_name(no).calcula_prioridade()
        )

        for no_intermediario in nos_intermediarios:
            if capacidade_restante <= 0:
                break

            no_intermediario_obj = grafo.get_node_by_name(no_intermediario)
            if no_intermediario_obj.populacao == 0:
                continue

            medicamentos_para_transferir = min(
                capacidade_restante,
                no_intermediario_obj.populacao
            )

            if medicamentos_para_transferir > 0:
                grafo.transferir_valores(
                    medicamentos_para_transferir,
                    caminho[0],
                    no_intermediario
                )
                capacidade_restante -= medicamentos_para_transferir

        grafo.desenha()

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None


def procura_BFS(grafo, inicio, fim):
    """
    Realiza a busca em largura (BFS) para encontrar o melhor caminho
    considerando todos os veículos disponíveis no nó inicial.
    Retorna o melhor caminho com base no custo mais baixo.
    """
    # Obter veículos disponíveis no nó inicial
    veiculos_disponiveis = grafo.get_veiculos_no(inicio)
    if not veiculos_disponiveis:
        print(f"Nó {inicio} não possui veículos disponíveis.")
        return None

    print(f"Veículos disponíveis em {inicio}: {[v.get_tipo() for v in veiculos_disponiveis]}")

    melhores_caminhos = []

    # Iterar sobre cada veículo disponível
    for veiculo in veiculos_disponiveis:
        print(f"Usando veículo: {veiculo.get_tipo()}")
        queue = [(inicio, [inicio])]  # Fila para BFS (nó atual, caminho até agora)
        visited = set()

        while queue:
            nodo_atual, caminho = queue.pop(0)
            if nodo_atual in visited:
                continue

            visited.add(nodo_atual)
            print(f"BFS: Visitando {nodo_atual}, Caminho atual: {caminho}")

            # Se o destino foi alcançado
            if nodo_atual == fim:
                custo_arestas = grafo.calcula_custo(caminho, veiculo.get_tipo())
                # Verificar se o custo acumulado excede o combustível disponível
                if custo_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho: {caminho}. Custo acumulado ({custo_arestas}) excede o combustível disponível ({veiculo.get_combustivel_disponivel()}).")
                else:
                    custo_final = custo_arestas * veiculo.get_custo()
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} PODE COMPLETAR o caminho: {caminho}. Custo acumulado: {custo_arestas}, Custo final: {custo_final}")

                    grafo.transferir_medicamentos(caminho, veiculo)

                    melhores_caminhos.append((veiculo.get_tipo(), caminho, custo_final))
                continue  # Continuar para outros caminhos possíveis

            # Adicionar vizinhos acessíveis à fila
            for (adjacente, peso, bloqueada, permitidos) in grafo.m_graph[nodo_atual]:
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada:
                    queue.append((adjacente, caminho + [adjacente]))
                    print(f"Vizinho {adjacente} adicionado à fila com caminho: {caminho + [adjacente]}")

    # Escolher o melhor caminho (menor custo) entre todos os veículos
    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        print(f"Melhor caminho: {melhor_caminho[1]} com veículo {melhor_caminho[0]} e custo {melhor_caminho[2]}")
        return {melhor_caminho[0]: (melhor_caminho[1], melhor_caminho[2])}

    print("Nenhum caminho válido encontrado.")
    return None


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
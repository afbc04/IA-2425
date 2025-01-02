import math
from queue import Queue
from collections import deque
import random
import numpy as np
from grafo import Grafo  
import time 
from queue import Queue

def procura_DFS(grafo, inicio, fim):
    """
    Realiza a busca em profundidade (DFS) para encontrar o melhor caminho
    e socorrer o nó de destino em prioridade máxima.
    Nós intermediários são socorridos apenas se sobrarem medicamentos,
    priorizando pela ordem de prioridade crescente.
    """
    start_time = time.time()
    no_origem = grafo.get_node_by_name(inicio)
    no_destino = grafo.get_node_by_name(fim)

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

            if nodo_atual == fim:
                custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
                if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
                    continue

                tempo_destino = no_destino.janela_tempo
                if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
                    continue

                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                if custo_final != float('inf'):
                    # **Primeiro socorrer o nó de destino**
                    medicamentos_disponiveis = min(no_origem.get_medicamento(), veiculo.get_limite_carga())
                    socorro_destino = min(no_destino.populacao, medicamentos_disponiveis)
                    if socorro_destino > 0:
                        grafo.transferir_valores(socorro_destino, no_origem.getNome(), fim)
                        medicamentos_disponiveis -= socorro_destino
                        print(f"[INFO] {socorro_destino} medicamentos transferidos para o nó de destino '{fim}'.")

                    # **Depois socorrer nós intermediários por prioridade**
                    if medicamentos_disponiveis > 0:
                        nos_intermediarios = [grafo.get_node_by_name(no) for no in caminho[1:-1]]
                        nos_intermediarios.sort(key=lambda no: no.calcula_prioridade())  # Ordenar por prioridade

                        for no in nos_intermediarios:
                            if medicamentos_disponiveis > 0 and no.populacao > 0:
                                qtd = min(no.populacao, medicamentos_disponiveis)
                                if grafo.transferir_valores(qtd, no_origem.getNome(), no.getNome()):
                                    medicamentos_disponiveis -= qtd
                                    print(f"[INFO] {qtd} medicamentos transferidos para o nó intermediário '{no.getNome()}'.")

                    grafo.desenha()

                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, custo_acumulado_arestas))
                continue

            vizinhos = [
                (adjacente, caminho + [adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]
            for adjacente, novo_caminho in reversed(vizinhos):
                stack.append((adjacente, novo_caminho))

    end_time = time.time()
    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        print(f"Distância percorrida: {distancia}")
        print(f"Tempo de execução: {end_time - start_time:.6f} segundos")

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None

def procura_BFS(grafo, inicio, fim):
    """
    Realiza a busca em largura (BFS) para encontrar o melhor caminho
    e socorrer o nó de destino em prioridade máxima.
    Nós intermediários são socorridos apenas se sobrarem medicamentos,
    priorizando pela ordem de prioridade crescente.
    """
    start_time = time.time()
    no_origem = grafo.get_node_by_name(inicio)
    no_destino = grafo.get_node_by_name(fim)

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
        queue = [(inicio, [inicio])]  # Fila para BFS (nó atual, caminho até agora)
        visited = set()

        while queue:
            nodo_atual, caminho = queue.pop(0)
            if nodo_atual in visited:
                continue

            visited.add(nodo_atual)
            print(f"BFS: Visitando {nodo_atual}, Caminho atual: {caminho}")

            if nodo_atual == fim:
                custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
                if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
                    continue

                tempo_destino = no_destino.janela_tempo
                if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
                    continue

                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                if custo_final != float('inf'):
                    # **Primeiro socorrer o nó de destino**
                    medicamentos_disponiveis = min(no_origem.get_medicamento(), veiculo.get_limite_carga())
                    socorro_destino = min(no_destino.populacao, medicamentos_disponiveis)
                    if socorro_destino > 0:
                        grafo.transferir_valores(socorro_destino, no_origem.getNome(), fim)
                        medicamentos_disponiveis -= socorro_destino
                        print(f"[INFO] {socorro_destino} medicamentos transferidos para o nó de destino '{fim}'.")

                    # **Depois socorrer nós intermediários por prioridade**
                    if medicamentos_disponiveis > 0:
                        nos_intermediarios = [grafo.get_node_by_name(no) for no in caminho[1:-1]]
                        nos_intermediarios.sort(key=lambda no: no.calcula_prioridade())  # Ordenar por prioridade

                        for no in nos_intermediarios:
                            if medicamentos_disponiveis > 0 and no.populacao > 0:
                                qtd = min(no.populacao, medicamentos_disponiveis)
                                if grafo.transferir_valores(qtd, no_origem.getNome(), no.getNome()):
                                    medicamentos_disponiveis -= qtd
                                    print(f"[INFO] {qtd} medicamentos transferidos para o nó intermediário '{no.getNome()}'.")

                    grafo.desenha()

                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, custo_acumulado_arestas))
                continue

            vizinhos = [
                (adjacente, caminho + [adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]
            for adjacente, novo_caminho in vizinhos:
                queue.append((adjacente, novo_caminho))

    end_time = time.time()
    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        print(f"Distância percorrida: {distancia}")
        print(f"Tempo de execução: {end_time - start_time:.6f} segundos")

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None

def procura_aStar(grafo, inicio, fim):
    """
    Realiza a busca A* para encontrar o melhor caminho com base na soma do custo acumulado e da heurística,
    priorizando o socorro ao nó de destino e, se possível, socorrendo nós intermediários por ordem de prioridade.
    """
    start_time = time.time()
    no_origem = grafo.get_node_by_name(inicio)
    no_destino = grafo.get_node_by_name(fim)

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

        open_list = {inicio}
        closed_list = set()
        g = {inicio: 0}
        parents = {inicio: None}

        while open_list:
            n = min(open_list, key=lambda v: g[v] + grafo.m_h.get(v, float('inf')))
            open_list.remove(n)
            closed_list.add(n)

            if n == fim:
                # Construir o caminho
                caminho = []
                while parents[n] is not None:
                    caminho.append(n)
                    n = parents[n]
                caminho.append(inicio)
                caminho.reverse()

                custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
                if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
                    break

                tempo_destino = no_destino.janela_tempo
                if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
                    break

                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                if custo_final != float('inf'):
                    # **Primeiro socorrer o nó de destino**
                    medicamentos_disponiveis = min(no_origem.get_medicamento(), veiculo.get_limite_carga())
                    socorro_destino = min(no_destino.populacao, medicamentos_disponiveis)
                    if socorro_destino > 0:
                        grafo.transferir_valores(socorro_destino, no_origem.getNome(), fim)
                        medicamentos_disponiveis -= socorro_destino
                        print(f"[INFO] {socorro_destino} medicamentos transferidos para o nó de destino '{fim}'.")

                    # **Depois socorrer nós intermediários por prioridade**
                    if medicamentos_disponiveis > 0:
                        nos_intermediarios = [grafo.get_node_by_name(no) for no in caminho[1:-1]]
                        nos_intermediarios.sort(key=lambda no: no.calcula_prioridade())  # Ordenar por prioridade

                        for no in nos_intermediarios:
                            if medicamentos_disponiveis > 0 and no.populacao > 0:
                                qtd = min(no.populacao, medicamentos_disponiveis)
                                if grafo.transferir_valores(qtd, no_origem.getNome(), no.getNome()):
                                    medicamentos_disponiveis -= qtd
                                    print(f"[INFO] {qtd} medicamentos transferidos para o nó intermediário '{no.getNome()}'.")

                    grafo.desenha()

                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, custo_acumulado_arestas))
                break

            for m, peso in grafo.getNeighbours(n, veiculo.get_tipo()):
                if m in closed_list:
                    continue

                custo_possivel = g[n] + peso

                if m not in open_list or custo_possivel < g.get(m, float('inf')):
                    g[m] = custo_possivel
                    parents[m] = n
                    open_list.add(m)

    end_time = time.time()
    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho

        print(f"Melhor caminho: {caminho}")
        print(f"Veículo: {veiculo.get_tipo()}")
        print(f"Custo total: {custo}")
        print(f"Distância percorrida: {distancia}")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None

def greedy(grafo, inicio, fim):
    """
    Realiza a busca gulosa para encontrar o melhor caminho com base na heurística.
    Prioriza socorrer o nó de destino e, se possível, os nós intermediários em ordem de prioridade.
    """
    start_time = time.time()
    no_origem = grafo.get_node_by_name(inicio)
    no_destino = grafo.get_node_by_name(fim)

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
        nodo_atual = inicio
        caminho = [inicio]
        visited = set()

        while nodo_atual != fim:
            visited.add(nodo_atual)
            vizinhos = [
                (adjacente, grafo.m_h.get(adjacente, float('inf')))
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]

            if not vizinhos:
                print(f"[ERRO] Sem vizinhos acessíveis a partir de {nodo_atual}.")
                break

            # Seleciona o vizinho com menor heurística
            vizinho_escolhido = min(vizinhos, key=lambda x: x[1])[0]
            caminho.append(vizinho_escolhido)
            nodo_atual = vizinho_escolhido

        custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
        if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
            print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
            continue

        tempo_destino = no_destino.janela_tempo
        if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
            print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
            continue

        custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

        if custo_final != float('inf'):
            # **Primeiro socorrer o nó de destino**
            medicamentos_disponiveis = min(no_origem.get_medicamento(), veiculo.get_limite_carga())
            socorro_destino = min(no_destino.populacao, medicamentos_disponiveis)
            if socorro_destino > 0:
                grafo.transferir_valores(socorro_destino, no_origem.getNome(), fim)
                medicamentos_disponiveis -= socorro_destino
                print(f"[INFO] {socorro_destino} medicamentos transferidos para o nó de destino '{fim}'.")

            # **Depois socorrer nós intermediários por prioridade**
            if medicamentos_disponiveis > 0:
                nos_intermediarios = [grafo.get_node_by_name(no) for no in caminho[1:-1]]
                nos_intermediarios.sort(key=lambda no: no.calcula_prioridade())  # Ordenar por prioridade

                for no in nos_intermediarios:
                    if medicamentos_disponiveis > 0 and no.populacao > 0:
                        qtd = min(no.populacao, medicamentos_disponiveis)
                        if grafo.transferir_valores(qtd, no_origem.getNome(), no.getNome()):
                            medicamentos_disponiveis -= qtd
                            print(f"[INFO] {qtd} medicamentos transferidos para o nó intermediário '{no.getNome()}'.")

            grafo.desenha()

            melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, custo_acumulado_arestas))

    end_time = time.time()
    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho

        print(f"Melhor caminho: {caminho}")
        print(f"Veículo: {veiculo.get_tipo()}")
        print(f"Custo total: {custo}")
        print(f"Distância percorrida: {distancia}")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None
    
# algorithm simulated annealing
def simulated_annealing(grafo, destino, temperatura_inicial=10, numero_iteracoes=10):
    start_time = time.time()

    # Filtra nós disponíveis (exceto o destino)
    nos_disponiveis = [no for no in grafo.m_nodes if no.getName() != destino]
    if not nos_disponiveis:
        print("Nenhum nó inicial disponível.")
        return None

    # Escolher um nó inicial aleatório
    no_origem = random.choice(nos_disponiveis)
    print(f"Ponto inicial aleatório escolhido: {no_origem.getName()}")

    if no_origem.janela_tempo == 0:
        print(f"[ERRO] O nó de origem '{no_origem.getName()}' não pode ser utilizado porque o tempo esgotou.")
        return None

    if no_origem.get_medicamento() == 0:
        print(f"[ERRO] NINGUÉM FOI SOCORRIDO, NÓ ORIGEM SEM MEDICAMENTOS: '{no_origem.getName()}'")
        return None

    veiculos_disponiveis = grafo.get_veiculos_no(no_origem.getName())
    if not veiculos_disponiveis:
        print(f"Nó {no_origem.getName()} não possui veículos disponíveis.")
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"Testando Simulated Annealing com o veículo: {veiculo.get_tipo()}")

        atual = no_origem
        caminho_atual = [no_origem.getName()]
        custo_atual = 0
        melhor_custo = float('inf')
        melhor_caminho = []
        pessoas_socorridas = 0

        for i in range(numero_iteracoes):
            # Encerrar se o nó atual for o destino
            if atual.getName() == destino:
                print(f"Destino {destino} alcançado na iteração {i}.")
                break

            # Obter vizinhos acessíveis
            vizinhos = [
                (adjacente, peso)
                for adjacente, peso in grafo.getNeighbours(atual.getName(), veiculo.get_tipo())
                if adjacente not in caminho_atual
            ]

            if not vizinhos:
                print(f"Nó {atual.getName()} não possui vizinhos acessíveis para o veículo {veiculo.get_tipo()}.")
                break

            # Escolher próximo nó baseado na heurística
            candidato_nome, peso = min(
                vizinhos,
                key=lambda v: grafo.calcula_heuristica(
                    grafo.get_node_by_name(v[0]), grafo.get_node_by_name(destino)
                )
            )
            candidato = grafo.get_node_by_name(candidato_nome)

            # Calcular custo temporário
            custo_temporario, pessoas_socorridas_temp = grafo.calcula_custo(
                caminho_atual + [candidato.getName()], veiculo
            )

            # Verificar combustível e velocidade
            if custo_temporario == float('inf') or custo_temporario > veiculo.get_combustivel_disponivel():
                print(f"[DEBUG] Veículo {veiculo.get_tipo()} não pode acessar {candidato.getName()}.")
                continue
            if candidato.janela_tempo > 0 and (custo_temporario / candidato.janela_tempo) > veiculo.get_velocidade():
                print(f"[DEBUG] Veículo {veiculo.get_tipo()} não pode acessar {candidato.getName()} devido à velocidade.")
                continue

            # Calcular probabilidade de aceitação
            candidato_avaliacao = grafo.calcula_heuristica(candidato, grafo.get_node_by_name(destino))
            atual_avaliacao = grafo.calcula_heuristica(atual, grafo.get_node_by_name(destino))
            diferenca = candidato_avaliacao - atual_avaliacao

            temperatura = temperatura_inicial / float(i + 1)
            probabilidade_aceitacao = np.exp(-diferenca / temperatura) if temperatura > 0 else 0

            if diferenca < 0 or random.random() < probabilidade_aceitacao:
                atual = candidato
                caminho_atual.append(candidato.getName())
                custo_atual = custo_temporario
                pessoas_socorridas = pessoas_socorridas_temp

            # Atualizar melhor caminho
            if custo_atual < melhor_custo:
                melhor_custo = custo_atual
                melhor_caminho = list(caminho_atual)

        if melhor_caminho:
            melhores_caminhos.append((veiculo, melhor_caminho, melhor_custo, pessoas_socorridas))

    # Determinar melhor resultado
    end_time = time.time()
    if melhores_caminhos:
        melhor_resultado = min(melhores_caminhos, key=lambda x: x[2])
        veiculo, caminho, custo, pessoas_socorridas = melhor_resultado

        # Realizar distribuição de medicamentos após determinar o melhor caminho
        medicamentos_disponiveis = min(no_origem.get_medicamento(), veiculo.get_limite_carga())
        nos_caminho = [
            grafo.get_node_by_name(no_nome)
            for no_nome in caminho[1:]
            if grafo.get_node_by_name(no_nome).janela_tempo > 0
            and grafo.get_node_by_name(no_nome).populacao > 0
        ]
        nos_caminho.sort(key=lambda x: x.calcula_prioridade())
        for no in nos_caminho:
            if medicamentos_disponiveis > 0:
                qtd = min(no.populacao, medicamentos_disponiveis)
                if grafo.transferir_valores(qtd, no_origem.getName(), no.getName()):
                    medicamentos_disponiveis -= qtd

        print(f"Melhor caminho: {caminho}")
        print(f"Veículo: {veiculo.get_tipo()}")
        print(f"Custo total: {custo}")
        print(f"Pessoas socorridas: {pessoas_socorridas}")
        print(f"Tempo de execução: {end_time - start_time:.6f} segundos")

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None

def hill_climbing(grafo, destino, max_restarts, max_iteracoes):
    start_time = time.time()
    melhor_caminho_global = None
    melhor_custo_global = float('inf')
    melhor_veiculo_global = None
    melhor_pessoas_socorridas = 0
    melhor_distancia = 0
    
    destino_node = grafo.get_node_by_name(destino)
    
    for tentativa in range(max_restarts):
        print(f"\n{'=' * 30}")
        print(f"Tentativa {tentativa+1} de {max_restarts}")
        
        todos_nos = [no for no in grafo.m_nodes if no.getNome()!=destino]
            
        no_origem = random.choice(todos_nos)
        print(f"Ponto inicial escolhido: {no_origem.getNome()} (Medicamentos: {no_origem.get_medicamento()})")

        if no_origem.janela_tempo==0:
            continue

        veiculos_disponiveis = grafo.get_veiculos_no(no_origem.getNome())
        if not veiculos_disponiveis:
            continue

        for veiculo in veiculos_disponiveis:
            medicamentos_disponiveis = no_origem.get_medicamento()
            if medicamentos_disponiveis == 0 or veiculo.get_limite_carga() == 0:
                continue
                
            print(f"\nA testar {veiculo.get_tipo()}")
            
            caminho_atual = [no_origem.getNome()]
            ultimo_no = no_origem
            distancia_atual = grafo.calcula_heuristica(no_origem, destino_node)
            
            for iteracao in range(max_iteracoes):
                ultimo_no = caminho_atual[-1]
                ultimo_no_obj = grafo.get_node_by_name(ultimo_no)

                print(f"Iteração {iteracao}: Explorar a partir de {ultimo_no}")
                
                if ultimo_no == destino:

                    custo_acumulado = grafo.calcula_acumulado_arestas(caminho_atual, veiculo)
                    if custo_acumulado==float('inf') or custo_acumulado>veiculo.get_combustivel_disponivel():
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho_atual}.")
                        continue

                    tempo_destino = destino_node.janela_tempo
                    if tempo_destino > 0 and (custo_acumulado / tempo_destino) > veiculo.get_velocidade():
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho_atual}.")
                        continue
                    
                    
                    custo_final, pessoas_socorridas = grafo.calcula_custo(caminho_atual, veiculo)
                        
                    if custo_final < melhor_custo_global:
                        melhor_caminho_global = caminho_atual.copy()
                        melhor_custo_global = custo_final
                        melhor_pessoas_socorridas = pessoas_socorridas
                        melhor_veiculo_global = veiculo
                        print(f"\nNovo melhor caminho encontrado!")
                        print(f"Caminho: {' -> '.join(caminho_atual)}")
                        print(f"Custo: {custo_final}")
                            
                        # Distribuição de medicamentos por prioridade calculada
                        medicamentos_disponiveis = min(no_origem.get_medicamento(), veiculo.get_limite_carga())
                            
                        # Cria lista de nós que estão no caminho
                        nos_caminho = []
                        for no_nome in caminho_atual[1:]:
                            no = grafo.get_node_by_name(no_nome)
                            if no.janela_tempo > 0 and no.populacao > 0:
                                nos_caminho.append(no)
                            
                        # Ordena os nós por prioridade
                        nos_caminho.sort(key=lambda x: x.calcula_prioridade())
                            
                        #Distribui, se possível, medicamentos pelos nos
                        for no in nos_caminho:
                            if medicamentos_disponiveis > 0:
                                qtd = min(no.populacao, medicamentos_disponiveis)
                                if grafo.transferir_valores(qtd, no_origem.getNome(), no.getNome()):
                                    medicamentos_disponiveis -= qtd
                        grafo.desenha()
                    break
                
                todos_vizinhos = []
                for vizinho, peso, bloqueada, permitidos in grafo.m_graph[ultimo_no]:
                    if (vizinho not in caminho_atual and 
                        veiculo.get_tipo() in permitidos and 
                        not bloqueada):
                        todos_vizinhos.append((vizinho, peso))
                
                melhor_vizinho = None
                menor_distancia = distancia_atual
                
                for vizinho, _ in todos_vizinhos:
                    vizinho_obj = grafo.get_node_by_name(vizinho)
                    dist = grafo.calcula_heuristica(vizinho_obj, destino_node)
                    if dist < menor_distancia or (menor_distancia==dist):
                        melhor_vizinho = vizinho
                        menor_distancia = dist
                
                if melhor_vizinho:
                    caminho_atual.append(melhor_vizinho)
                    distancia_atual = menor_distancia
                else:
                    break     
    end_time = time.time()
    if melhor_caminho_global is None:
        return None
    else:
        melhor_distancia = grafo.calcula_acumulado_arestas(melhor_caminho_global, melhor_veiculo_global)
        print(f"Melhor caminho: {melhor_caminho_global}")
        print(f"Veículo: {melhor_veiculo_global.get_tipo()}")
        print(f"Custo total: {melhor_custo_global}")
        print(f"Pessoas socorridas: {melhor_pessoas_socorridas}")
        print(f"Distância percorrida: {melhor_distancia}")
        print(f"Tempo de execução: {end_time - start_time:.2f} segundos")
        
    
    return {melhor_veiculo_global.get_tipo(): (melhor_caminho_global, melhor_custo_global)}
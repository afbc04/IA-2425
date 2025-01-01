import math
from queue import Queue
from collections import deque
import random
import numpy as np
from grafo import Grafo  
import time 
from queue import Queue

def procura_DFS(grafo, inicio, fim):
    start_time = time.time()  # Início da medição do tempo
    print(f"[INFO] Início da busca em profundidade (DFS) de {inicio} para {fim}.")

    no_origem = grafo.get_node_by_name(inicio)
    if no_origem.janela_tempo == 0:
        print(f"[ERRO] O nó de origem '{inicio}' não pode ser utilizado porque a janela de tempo terminou.")
        return None

    if no_origem.get_medicamento() == 0:
        print(f"[ERRO] Ninguém foi socorrido. O nó de origem '{inicio}' não possui medicamentos.")
        return None

    veiculos_disponiveis = grafo.get_veiculos_no(inicio)
    if not veiculos_disponiveis:
        print(f"[ERRO] O nó '{inicio}' não possui veículos disponíveis.")
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"[INFO] A tentar com o veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()}).")
        stack = [(inicio, [inicio])]
        visitados = set()

        while stack:
            nodo_atual, caminho = stack.pop()
            if nodo_atual in visitados:
                continue

            visitados.add(nodo_atual)

            if nodo_atual == fim:
                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)
                if custo_final != float('inf'):
                    distancia = grafo.calcula_acumulado_arestas(caminho, veiculo)
                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, distancia))
                continue

            vizinhos = [
                (adjacente, caminho + [adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visitados and veiculo.get_tipo() in permitidos and not bloqueada
            ]
            for adjacente, novo_caminho in reversed(vizinhos):
                stack.append((adjacente, novo_caminho))

    melhor_caminho = min(melhores_caminhos, key=lambda x: x[2]) if melhores_caminhos else None

    end_time = time.time()
    print(f"Tempo de execução (DFS): {end_time - start_time:.6f} segundos.")

    if melhor_caminho:
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho
        print(f"[RESULTADO] Veículo: {veiculo.get_tipo()}\n"
              f"Caminho: {caminho}\n"
              f"Custo: {custo}\n"
              f"Pessoas socorridas: {pessoas_socorridas}\n"
              f"Distância percorrida: {distancia}.")
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)
        grafo.desenha()
        return {veiculo.get_tipo(): (caminho, custo)}

    print("[ERRO] Nenhum caminho válido encontrado.")
    return None


def procura_BFS(grafo, inicio, fim):
    start_time = time.time()
    print(f"[INFO] Início da busca em largura (BFS) de {inicio} para {fim}.")

    no_origem = grafo.get_node_by_name(inicio)
    if no_origem.janela_tempo == 0:
        print(f"[ERRO] O nó de origem '{inicio}' não pode ser utilizado porque a janela de tempo terminou.")
        return None

    if no_origem.get_medicamento() == 0:
        print(f"[ERRO] Ninguém foi socorrido. O nó de origem '{inicio}' não possui medicamentos.")
        return None

    veiculos_disponiveis = grafo.get_veiculos_no(inicio)
    if not veiculos_disponiveis:
        print(f"[ERRO] O nó '{inicio}' não possui veículos disponíveis.")
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"[INFO] A tentar com o veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()}).")
        queue = [(inicio, [inicio])]
        visitados = set()

        while queue:
            nodo_atual, caminho = queue.pop(0)
            if nodo_atual in visitados:
                continue

            visitados.add(nodo_atual)

            if nodo_atual == fim:
                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)
                if custo_final != float('inf'):
                    distancia = grafo.calcula_acumulado_arestas(caminho, veiculo)
                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, distancia))
                continue

            vizinhos = [
                (adjacente, caminho + [adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visitados and veiculo.get_tipo() in permitidos and not bloqueada
            ]
            for adjacente, novo_caminho in vizinhos:
                queue.append((adjacente, novo_caminho))

    melhor_caminho = min(melhores_caminhos, key=lambda x: x[2]) if melhores_caminhos else None

    end_time = time.time()
    print(f"Tempo de execução (BFS): {end_time - start_time:.6f} segundos.")

    if melhor_caminho:
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho
        print(f"[RESULTADO] Veículo: {veiculo.get_tipo()}\n"
              f"Caminho: {caminho}\n"
              f"Custo: {custo}\n"
              f"Pessoas socorridas: {pessoas_socorridas}\n"
              f"Distância percorrida: {distancia}.")
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)
        grafo.desenha()
        return {veiculo.get_tipo(): (caminho, custo)}

    print("[ERRO] Nenhum caminho válido encontrado.")
    return None

def procura_aStar(grafo, inicio, fim):
    start_time = time.time()
    print(f"[INFO] Início do algoritmo A* de {inicio} para {fim}.")

    no_origem = grafo.get_node_by_name(inicio)
    if no_origem.janela_tempo == 0:
        print(f"[ERRO] O nó de origem '{inicio}' não pode ser utilizado porque a janela de tempo terminou.")
        return None

    veiculos_disponiveis = grafo.get_veiculos_no(inicio)
    if not veiculos_disponiveis:
        print(f"[ERRO] O nó '{inicio}' não possui veículos disponíveis.")
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"[INFO] A tentar com o veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()}).")
        open_list = {inicio}
        closed_list = set()
        g = {inicio: 0}
        parents = {inicio: None}

        while open_list:
            n = min(open_list, key=lambda v: g[v] + grafo.m_h.get(v, float('inf')))
            open_list.remove(n)
            closed_list.add(n)

            if n == fim:
                caminho = []
                while parents[n] is not None:
                    caminho.append(n)
                    n = parents[n]
                caminho.append(inicio)
                caminho.reverse()

                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)
                if custo_final != float('inf'):
                    distancia = grafo.calcula_acumulado_arestas(caminho, veiculo)
                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, distancia))
                break

            for m, peso in grafo.getNeighbours(n, veiculo.get_tipo()):
                if m in closed_list:
                    continue

                custo_possivel = g[n] + peso

                if m not in open_list or custo_possivel < g.get(m, float('inf')):
                    g[m] = custo_possivel
                    parents[m] = n

                    if m not in open_list:
                        open_list.add(m)

    melhor_caminho = min(melhores_caminhos, key=lambda x: x[2]) if melhores_caminhos else None

    end_time = time.time()
    print(f"Tempo de execução (A*): {end_time - start_time:.6f} segundos.")

    if melhor_caminho:
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho
        print(f"[RESULTADO] Veículo: {veiculo.get_tipo()}\n"
              f"Caminho: {caminho}\n"
              f"Custo: {custo}\n"
              f"Pessoas socorridas: {pessoas_socorridas}\n"
              f"Distância percorrida: {distancia}.")
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)
        grafo.desenha()
        return {veiculo.get_tipo(): (caminho, custo)}

    print("[ERRO] Nenhum caminho válido encontrado.")
    return None


def greedy(grafo, inicio, fim):
    start_time = time.time()
    print(f"[INFO] Início do algoritmo Greedy de {inicio} para {fim}.")

    no_origem = grafo.get_node_by_name(inicio)
    if no_origem.janela_tempo == 0:
        print(f"[ERRO] O nó de origem '{inicio}' não pode ser utilizado porque a janela de tempo terminou.")
        return None

    veiculos_disponiveis = grafo.get_veiculos_no(inicio)
    if not veiculos_disponiveis:
        print(f"[ERRO] O nó '{inicio}' não possui veículos disponíveis.")
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"[INFO] A tentar com o veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()}).")

        caminho = [inicio]
        nodo_atual = inicio
        visitados = set()

        while nodo_atual != fim:
            visitados.add(nodo_atual)

            vizinhos = [
                (adjacente, grafo.m_h[adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visitados and veiculo.get_tipo() in permitidos and not bloqueada
            ]

            if not vizinhos:
                print(f"[ERRO] Sem vizinhos acessíveis para o nó {nodo_atual}.")
                break

            vizinho_escolhido = min(vizinhos, key=lambda x: x[1])[0]
            caminho.append(vizinho_escolhido)
            nodo_atual = vizinho_escolhido

        if nodo_atual == fim:
            custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)
            if custo_final != float('inf'):
                distancia = grafo.calcula_acumulado_arestas(caminho, veiculo)
                melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, distancia))

    melhor_caminho = min(melhores_caminhos, key=lambda x: x[2]) if melhores_caminhos else None

    end_time = time.time()
    print(f"Tempo de execução (Greedy): {end_time - start_time:.6f} segundos.")

    if melhor_caminho:
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho
        print(f"[RESULTADO] Veículo: {veiculo.get_tipo()}\n"
              f"Caminho: {caminho}\n"
              f"Custo: {custo}\n"
              f"Pessoas socorridas: {pessoas_socorridas}\n"
              f"Distância percorrida: {distancia}.")
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)
        grafo.desenha()
        return {veiculo.get_tipo(): (caminho, custo)}

    print("[ERRO] Nenhum caminho válido encontrado.")
    return None

# algorithm simulated annealing
def simulated_annealing(grafo, destino, temperatura_inicial=10, numero_iteracoes=10):
    """
    Simulated Annealing para encontrar o melhor caminho em um grafo considerando veículos.

    Args:
        grafo: O grafo representando os nós e arestas.
        destino: O nó de destino.
        temperatura_inicial: A temperatura inicial para o algoritmo.
        numero_iteracoes: Número de iterações a executar.

    Returns:
        Um dicionário contendo o veículo usado, o caminho encontrado e o custo do caminho.
    """

    # Escolher um nó inicial aleatório
    nos_disponiveis = [no for no in grafo.m_nodes if no.getName() != destino]
    if not nos_disponiveis:
        print("Nenhum nó inicial disponível.")
        return None

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
        print(f"Testar Simulated Annealing com o veículo: {veiculo.get_tipo()}")

        atual = no_origem  # Começa no nó inicial
        caminho_atual = [no_origem.getName()]
        custo_atual = 0
        melhor_custo = float('inf')
        melhor_caminho = []

        for i in range(numero_iteracoes):
            # Encerrar se o nó atual for o destino
            if atual.getName() == destino:
                print(f"Destino {destino} alcançado na iteração {i}.")
                break

            vizinhos = [
                (adjacente, peso)
                for adjacente, peso in grafo.getNeighbours(atual.getName(), veiculo.get_tipo())
                if adjacente not in caminho_atual
            ]

            if not vizinhos:
                print(f"Nó {atual.getName()} não possui vizinhos acessíveis para o veículo {veiculo.get_tipo()}.")
                break

            # Distribuição de medicamentos por prioridade calculada
            medicamentos_disponiveis = min(
            no_origem.get_medicamento(),
            veiculo.get_limite_carga()
            )
                            
            # Criar lista de nós que estão no caminho
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
                    if grafo.transferir_valores(qtd, no_origem.getName(), no.getName()):
                        medicamentos_disponiveis -= qtd
            grafo.desenha()           
            
            # Escolher próximo nó baseado na heurística (calculaDist)
            candidato_nome, peso = min(
            vizinhos, key=lambda v: grafo.calcula_heuristica(grafo.get_node_by_name(v[0]), grafo.get_node_by_name(destino)))

            candidato = grafo.get_node_by_name(candidato_nome)

            custo_temporario, _ = grafo.calcula_custo(caminho_atual + [candidato.getName()], veiculo)

            if custo_temporario == float('inf') or custo_temporario > veiculo.get_combustivel_disponivel():
                print(f"[DEBUG] Veículo {veiculo.get_tipo()} não pode acessar {candidato.getName()} com o caminho {caminho_atual + [candidato.getName()]}.")
                continue
            

            candidato_avaliacao = grafo.calcula_heuristica(candidato, grafo.get_node_by_name(destino))
            candidato_atual = grafo.calcula_heuristica(atual, grafo.get_node_by_name(destino))

            diferenca = candidato_avaliacao - candidato_atual
            temperatura = temperatura_inicial / float(i + 1)
            probabilidade_aceitacao = np.exp(-diferenca / temperatura) if temperatura > 0 else 0

            if diferenca < 0 or random.random() < probabilidade_aceitacao:
                atual = candidato
                caminho_atual.append(candidato.getName())
                custo_atual = custo_temporario

            if custo_atual < melhor_custo:
                melhor_custo = custo_atual
                melhor_caminho = list(caminho_atual)

        if melhor_caminho:
            melhores_caminhos.append((veiculo, melhor_caminho, melhor_custo))

    if melhores_caminhos:
        melhor_resultado = min(melhores_caminhos, key=lambda x: x[2])
        veiculo, caminho, custo = melhor_resultado
        print(f"Melhor caminho encontrado: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None


def hill_climbing(grafo, destino, max_restarts, max_iteracoes):
    melhor_caminho_global = None
    melhor_custo_global = float('inf')
    melhor_veiculo_global = None
    
    destino_node = grafo.get_node_by_name(destino)
    
    for tentativa in range(max_restarts):
        print(f"\n{'=' * 30}")
        print(f"Tentativa {tentativa+1} de {max_restarts}")
        
        todos_nos = [no for no in grafo.m_nodes if no.getName()!=destino]
            
        no_origem = random.choice(todos_nos)
        print(f"Ponto inicial escolhido: {no_origem.getName()} (Medicamentos: {no_origem.get_medicamento()})")

        if no_origem.janela_tempo==0:
            continue

        veiculos_disponiveis = grafo.get_veiculos_no(no_origem.getName())
        if not veiculos_disponiveis:
            continue

        for veiculo in veiculos_disponiveis:
            medicamentos_disponiveis = no_origem.get_medicamento()
            if medicamentos_disponiveis == 0 or veiculo.get_limite_carga() == 0:
                continue
                
            print(f"\nA testar {veiculo.get_tipo()}")
            
            caminho_atual = [no_origem.getName()]
            ultimo_no = no_origem
            distancia_atual = grafo.calcula_heuristica(no_origem, destino_node)
            
            for iteracao in range(max_iteracoes):
                ultimo_no = caminho_atual[-1]
                ultimo_no_obj = grafo.get_node_by_name(ultimo_no)

                print(f"Iteração {iteracao}: Explorando a partir de {ultimo_no}")
                
                if ultimo_no == destino:
                    tempo_total = 0
                    no_anterior = None
                    
                    for no in caminho_atual:
                        if no_anterior:
                            for viz, peso, _, _ in grafo.m_graph[no_anterior]:
                                if viz == no:
                                    tempo_total += peso / veiculo.get_velocidade()
                                    break
                        no_anterior = no
                    
                    if tempo_total <= destino_node.janela_tempo:
                        custo_final, _ = grafo.calcula_custo(caminho_atual, veiculo)
                        
                        if custo_final < melhor_custo_global:
                            melhor_caminho_global = caminho_atual.copy()
                            melhor_custo_global = custo_final
                            melhor_veiculo_global = veiculo.get_tipo()
                            print(f"\nNovo melhor caminho encontrado!")
                            print(f"Caminho: {' -> '.join(caminho_atual)}")
                            print(f"Tempo total: {tempo_total:.2f}")
                            print(f"Custo: {custo_final}")
                            
                            # Distribuição de medicamentos por prioridade calculada
                            medicamentos_disponiveis = min(
                                no_origem.get_medicamento(),
                                veiculo.get_limite_carga()
                            )
                            
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
                                    if grafo.transferir_valores(qtd, no_origem.getName(), no.getName()):
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
                    if dist < menor_distancia:
                        melhor_vizinho = vizinho
                        menor_distancia = dist
                
                if melhor_vizinho:
                    caminho_atual.append(melhor_vizinho)
                    distancia_atual = menor_distancia
                else:
                    break     

    if melhor_caminho_global is None:
        return None, None, float('inf')
        
    return melhor_veiculo_global, melhor_caminho_global, melhor_custo_global
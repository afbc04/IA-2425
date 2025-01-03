import math
from queue import Queue
from collections import deque
import random
import numpy as np
from grafo import Grafo  
import time 
from queue import Queue
import heapq

def procura_DFS(grafo, inicio, fim):
    """
    Realiza a busca em profundidade (DFS) para encontrar o melhor caminho
    considerando todos os veículos disponíveis no nó inicial.
    Retorna o melhor caminho com base no custo mais baixo.
    """
    start_time = time.time()

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
        if veiculo.get_velocidade() == 0:
            print(f"[AVISO] Veículo {veiculo.get_tipo()} ignorado devido à velocidade ser 0.")
            continue

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
            vizinhos.sort(key=lambda x: x[0])  # Ordenar alfabeticamente os vizinhos
            for adjacente, novo_caminho in reversed(vizinhos):
                stack.append((adjacente, novo_caminho))
                print(f"Vizinho {adjacente} adicionado à pilha com caminho: {novo_caminho}")

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        end_time = time.time()
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
            if no_intermediario_obj.populacao == 0 or no_intermediario_obj.janela_tempo == 0:
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

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        print(f"Tempo total de execução: {end_time - start_time:.6f} segundos")

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None

def procura_BFS(grafo, inicio, fim):
    """
    Realiza a busca em largura (BFS) para encontrar o melhor caminho
    considerando todos os veículos disponíveis no nó inicial.
    Retorna o melhor caminho com base no custo mais baixo.
    """
    import time
    start_time = time.time()

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
        if veiculo.get_velocidade() == 0:
            print(f"[AVISO] Veículo {veiculo.get_tipo()} ignorado devido à velocidade ser 0.")
            continue

        print(f"Usando veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()})")
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
                custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
                print(f"[DEBUG] Caminho completo para veículo {veiculo.get_tipo()}: {caminho} com custo acumulado: {custo_acumulado_arestas}")

                if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
                else:
                    destino = grafo.get_node_by_name(fim)
                    tempo_destino = destino.janela_tempo
                    if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
                        continue

                    custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                    if custo_final == float('inf'):
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho: {caminho}.")
                    else:
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} PODE COMPLETAR o caminho: {caminho}. Custo final: {custo_final}")

                        melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas))
                continue

            # Adicionar vizinhos acessíveis à fila
            vizinhos = [
                (adjacente, caminho + [adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]
            for adjacente, novo_caminho in vizinhos:
                queue.append((adjacente, novo_caminho))
                print(f"Vizinho {adjacente} adicionado à fila com caminho: {novo_caminho}")

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        end_time = time.time()
        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        print(f"Tempo total de execução: {end_time - start_time:.6f} segundos")

        # Transferir valores para o destino e nós intermediários
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)

        capacidade_restante = veiculo.get_limite_carga() - pessoas_socorridas

        # Distribuir medicamentos para nós intermediários
        nos_intermediarios = sorted(
            caminho[1:-1],
            key=lambda no: grafo.get_node_by_name(no).calcula_prioridade()
        )

        for no_intermediario in nos_intermediarios:
            no_intermediario_obj = grafo.get_node_by_name(no_intermediario)
            if no_intermediario_obj.janela_tempo == 0:  # Ignorar nós com janela_tempo == 0
                print(f"[DEBUG] Ignorar nó '{no_intermediario}' devido a janela_tempo = 0.")
                continue

            if capacidade_restante <= 0:
                break

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

def procura_Iterativa(grafo, inicio, fim, max_profundidade):
    
    veiculos_disponiveis = grafo.get_veiculos_no(inicio)
    if not veiculos_disponiveis:
        print(f"Nó {inicio} não possui veículos disponíveis.")
        return None

    caminhos = {}

    #Fazer procura por veículo
    for veiculo in veiculos_disponiveis:
        
        #Aumentar a profundidade iterativamente
        for profundidade in range(max_profundidade + 1):

            resultado = procura_Iterativa_aux(grafo, inicio, fim, veiculo.get_tipo(), profundidade)

            #Encontrou a solução, retorna-a
            if resultado:
                print("Solução encontrada")
                caminhos[(veiculo.get_tipo(),profundidade)] = resultado
                break
    
    if caminhos:
        #return caminhos
    
        melhores_caminhos = []
        for k,v in caminhos.items():
            melhores_caminhos.append(v)    
        
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas, distancia, end_time, start_time = melhor_caminho

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        print(f"Distância percorrida: {distancia}")
        print(f"Tempo de execução: {end_time - start_time:.6f} segundos")
        
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
            if no_intermediario_obj.populacao == 0 or no_intermediario_obj.janela_tempo == 0:
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
        
        return {veiculo.get_tipo(): (caminho,custo)}

    else:
        print("[ERRO] Não foi achado solução :/")
        return None 

def procura_Iterativa_aux(grafo, inicio, fim, veiculoAtual, limite):
    """
    Realiza a busca em profundidade (Iterativa) para encontrar o melhor caminho.
    """
    start_time = time.time()
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
        
        if veiculoAtual != veiculo.get_tipo():
            continue
        
        stack = [(inicio, [inicio])]  # Pilha para DFS (nó atual, caminho até agora)
        visited = set()

        while stack:
            nodo_atual, caminho = stack.pop()
            if nodo_atual in visited:
                continue

            visited.add(nodo_atual)

            if nodo_atual == fim:
                custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
                if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
                    continue

                destino = grafo.get_node_by_name(fim)
                tempo_destino = destino.janela_tempo
                if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
                    continue

                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                if custo_final != float('inf'):
                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas, custo_acumulado_arestas))
                continue

            vizinhos = [
                (adjacente, caminho + [adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]
            if limite > 0:
                limite = limite - 1
                for adjacente, novo_caminho in reversed(vizinhos):
                    stack.append((adjacente, novo_caminho))
                    print(f"Vizinho {adjacente} adicionado à pilha com caminho: {novo_caminho}")

    end_time = time.time()
    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas, distancia = melhor_caminho
        return (veiculo, caminho, custo_final, pessoas_socorridas, custo_acumulado_arestas,end_time,start_time)

    return None

def procura_CustoUniforme(grafo, inicio, fim):
    """
    Realiza o algoritmo de Dijkstra para encontrar o melhor caminho
    considerando todos os veículos disponíveis no nó inicial.
    Retorna o melhor caminho com base no custo mais baixo.
    """
    start_time = time.time()

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

        heap = [(0, inicio, [])]  # (custo acumulado, nó atual, caminho)
        visitados = {}

        while heap:
            custo_atual, nodo_atual, caminho = heapq.heappop(heap)

            # Se o nó já foi visitado com um custo menor, ignore
            if nodo_atual in visitados and visitados[nodo_atual] <= custo_atual:
                continue
            visitados[nodo_atual] = custo_atual

            caminho = caminho + [nodo_atual]
            print(f"Custo uniforme: Visitando {nodo_atual}, Custo acumulado: {custo_atual}, Caminho: {caminho}")

            if nodo_atual == fim:
                custo_acumulado_arestas = custo_atual
                if custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
                    continue

                destino = grafo.get_node_by_name(fim)
                tempo_destino = destino.janela_tempo
                if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
                    continue

                custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                if custo_final == float('inf'):
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho: {caminho}.")
                else:
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} PODE COMPLETAR o caminho: {caminho}. Custo final: {custo_final}")

                    melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas))
                continue

            for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]:
                if veiculo.get_tipo() in permitidos and not bloqueada:
                    novo_custo = custo_atual + peso
                    heapq.heappush(heap, (novo_custo, adjacente, caminho))
                    print(f"Vizinho {adjacente} adicionado ao heap com custo acumulado: {novo_custo}")

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        end_time = time.time()
        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        print(f"Tempo total de execução: {end_time - start_time:.6f} segundos")

        # Transferir valores para o destino e nós intermediários
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)

        capacidade_restante = veiculo.get_limite_carga() - pessoas_socorridas

        # Distribuir medicamentos para nós intermediários
        nos_intermediarios = sorted(
            caminho[1:-1],
            key=lambda no: grafo.get_node_by_name(no).calcula_prioridade()
        )

        for no_intermediario in nos_intermediarios:
            no_intermediario_obj = grafo.get_node_by_name(no_intermediario)
            if no_intermediario_obj.janela_tempo == 0:  # Ignorar nós com janela_tempo = 0
                print(f"[DEBUG] Ignorar nó '{no_intermediario}' devido a janela_tempo = 0.")
                continue

            if capacidade_restante <= 0:
                break

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

def procura_aStar(grafo, inicio, fim):
    """
    Implementação do algoritmo A* com validações de combustível e velocidade,
    e cálculo correto de f(n) = g(n) + h(n).
    """
    import heapq
    import time

    start_time = time.time()

    # Validações iniciais
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
        if veiculo.get_velocidade() == 0:
            print(f"[AVISO] Veículo {veiculo.get_tipo()} ignorado devido à velocidade ser 0.")
            continue

        print(f"Usando veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()}, Combustível: {veiculo.get_combustivel_disponivel()})")

        fronteira = []
        heapq.heappush(fronteira, (0, inicio))  # Fila de prioridade: (f(n), nó)
        custos_acumulados = {inicio: 0}  # g(n)
        caminhos = {inicio: [inicio]}  # Caminhos acumulados
        expandidos = []  # Ordem de expansão

        while fronteira:
            f_atual, atual = heapq.heappop(fronteira)

            if atual in expandidos:
                continue
            expandidos.append(atual)
            print(f"[EXPANSÃO] Nó atual: {atual}, f(n): {f_atual}")

            if atual == fim:
                custo_final, pessoas_socorridas = grafo.calcula_custo(caminhos[atual], veiculo)
                if custo_final == float('inf'):
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho.")
                else:
                    print(f"[SUCESSO] Caminho encontrado: {caminhos[atual]} com custo: {custo_final}")
                    print(f"[INFO] Ordem de expansão dos nós: {expandidos}")
                    melhores_caminhos.append((veiculo, caminhos[atual], custo_final, pessoas_socorridas))
                break

            for vizinho, peso in grafo.getNeighbours(atual, veiculo.get_tipo()):
                novo_custo = custos_acumulados[atual] + peso  # g(n)
                heuristica = grafo.calcula_heuristica(
                    grafo.get_node_by_name(vizinho),
                    grafo.get_node_by_name(fim)
                )
                f_novo = novo_custo + heuristica  # f(n)

                # Validação de combustível
                if novo_custo > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho devido a falta de combustível: {caminhos[atual] + [vizinho]}")
                    continue

                # Validação de velocidade
                tempo_estimado = peso / veiculo.get_velocidade()  # Tempo necessário para a aresta
                if tempo_estimado > no_origem.janela_tempo:
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho devido à velocidade insuficiente: {caminhos[atual] + [vizinho]}")
                    continue

                if vizinho not in custos_acumulados or novo_custo < custos_acumulados[vizinho]:
                    custos_acumulados[vizinho] = novo_custo
                    heapq.heappush(fronteira, (f_novo, vizinho))
                    caminhos[vizinho] = caminhos[atual] + [vizinho]
                    print(f"[VISITA] Vizinho: {vizinho}, g(n): {novo_custo}, h(n): {heuristica}, f(n): {f_novo}")

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Selecionar caminho de menor custo
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        end_time = time.time()
        print(f"Tempo total de execução: {end_time - start_time:.6f} segundos")

        # Transferir valores e ajustar o estado
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

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")
        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None

def greedy(grafo, inicio, destino):
    """
    Realiza a busca gulosa para encontrar o melhor caminho considerando todos os veículos disponíveis no nó inicial.
    Prioriza o nó com menor heurística em cada iteração.
    """
    no_origem = grafo.get_node_by_name(inicio)
    no_destino = grafo.get_node_by_name(destino)

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

    grafo.atualizar_heuristicas(no_destino)

    for veiculo in veiculos_disponiveis:
        print(f"Usando veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()}, Combustível: {veiculo.get_combustivel_disponivel()})")

        caminho = [inicio]
        nodo_atual = inicio
        custo_acumulado = 0
        visited = set()

        while nodo_atual != destino:
            visited.add(nodo_atual)
            print(f"[DEBUG] Gulosa: Visitando {nodo_atual}, Caminho atual: {caminho}, Custo acumulado: {custo_acumulado}")

            vizinhos = [
                (adjacente, peso)
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]

            vizinhos_validos = []
            for adjacente, peso in vizinhos:
                novo_custo = custo_acumulado + peso
                if novo_custo <= veiculo.get_combustivel_disponivel():
                    vizinhos_validos.append((adjacente, peso))

            if not vizinhos_validos:
                print(f"[ERRO] Sem vizinhos válidos acessíveis a partir de {nodo_atual}.")
                break

            vizinho_escolhido, peso = min(
                vizinhos_validos,
                key=lambda v: grafo.m_h[v[0]]
            )

            caminho.append(vizinho_escolhido)
            nodo_atual = vizinho_escolhido
            custo_acumulado += peso

        if nodo_atual == destino:
            tempo_estimado = custo_acumulado / veiculo.get_velocidade()
            if tempo_estimado > no_destino.janela_tempo:
                print(f"[AVISO] Veículo {veiculo.get_tipo()} descartado por velocidade insuficiente para cumprir a janela de tempo do destino.")
                continue

            custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)
            if custo_final == float('inf'):
                print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho: {caminho}.")
            else:
                print(f"[DEBUG] Veículo: {veiculo.get_tipo()} PODE COMPLETAR o caminho: {caminho}. Custo final: {custo_final}")
                melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas))

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")

        capacidade_restante = veiculo.get_limite_carga()
        medicamentos_disponiveis = no_origem.get_medicamento()

        medicamentos_para_transferir = min(
            capacidade_restante,
            medicamentos_disponiveis,
            no_destino.populacao
        )
        if medicamentos_para_transferir > 0:
            grafo.transferir_valores(medicamentos_para_transferir, caminho[0], caminho[-1])
            medicamentos_disponiveis -= medicamentos_para_transferir
            capacidade_restante -= medicamentos_para_transferir

        for no_intermediario in sorted(caminho[1:-1], key=lambda no: grafo.get_node_by_name(no).calcula_prioridade()):
            no_intermediario_obj = grafo.get_node_by_name(no_intermediario)
            if no_intermediario_obj.populacao > 0 and capacidade_restante > 0 and no_intermediario_obj.janela_tempo > 0:
                medicamentos_para_transferir = min(
                    capacidade_restante,
                    medicamentos_disponiveis,
                    no_intermediario_obj.populacao
                )
                if medicamentos_para_transferir > 0:
                    grafo.transferir_valores(
                        medicamentos_para_transferir,
                        caminho[0],
                        no_intermediario
                    )
                    medicamentos_disponiveis -= medicamentos_para_transferir
                    capacidade_restante -= medicamentos_para_transferir

        grafo.atualizar_heuristicas(no_destino)
        grafo.desenha()

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
    return None

# algorithm simulated annealing
def simulated_annealing(grafo, inicio, destino, temperatura_inicial=10, numero_iteracoes=10):
    start_time = time.time()

    # Filtra nós disponíveis (exceto o destino)
    nos_disponiveis = [no for no in grafo.m_nodes if no.getNome() != destino]
    if not nos_disponiveis:
        print("Nenhum nó inicial disponível.")
        return None

    no_origem = None
    origem_tentativas = numero_iteracoes

    while origem_tentativas > 0 and no_origem is None:
        origem_tentativas -= 1
        # Escolher um nó inicial
        no_origem = grafo.get_node_by_name(inicio)
        print(f"Ponto inicial escolhido: {no_origem.getNome()}")

        if no_origem.janela_tempo == 0:
            print(f"[ERRO] O nó de origem '{no_origem.getNome()}' não pode ser utilizado porque o tempo esgotou.")
            no_origem = None
            continue

        if no_origem.get_medicamento() == 0:
            print(f"[ERRO] NINGUÉM FOI SOCORRIDO, NÓ ORIGEM SEM MEDICAMENTOS: '{no_origem.getNome()}'")
            no_origem = None
            continue

        veiculos_disponiveis = grafo.get_veiculos_no(no_origem.getNome())
        if not veiculos_disponiveis:
            print(f"Nó {no_origem.getNome()} não possui veículos disponíveis.")
            no_origem = None
            continue

    if no_origem is None:
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"Testando Simulated Annealing com o veículo: {veiculo.get_tipo()}")

        atual = no_origem
        caminho_atual = [no_origem.getNome()]
        custo_atual = 0
        melhor_custo = float('inf')
        melhor_caminho = []
        pessoas_socorridas = 0
        

        for i in range(numero_iteracoes):
            # Encerrar se o nó atual for o destino
            if atual.getNome() == destino:
                print(f"Destino {destino} alcançado na iteração {i}.")
                break

            # Obter vizinhos acessíveis
            vizinhos = [
                (adjacente, peso)
                for adjacente, peso in grafo.getNeighbours(atual.getNome(), veiculo.get_tipo())
                if adjacente not in caminho_atual
            ]

            if not vizinhos:
                print(f"Nó {atual.getNome()} não possui vizinhos acessíveis para o veículo {veiculo.get_tipo()}.")
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
            custo_temporario, pessoas_socorridas_temp = grafo.calcula_custo(caminho_atual + [candidato.getNome()], veiculo)
            #destino_no = grafo.get_node_by_name(destino)
            # Verificar combustível e velocidade
            if custo_temporario == float('inf') or custo_temporario > veiculo.get_combustivel_disponivel():
                print(f"[DEBUG] Veículo {veiculo.get_tipo()} não pode acessar {candidato.getNome()}.")
                continue
            if candidato.janela_tempo > 0 and (custo_temporario / candidato.janela_tempo) > veiculo.get_velocidade():
                print(f"[DEBUG] Veículo {veiculo.get_tipo()} não pode acessar {candidato.getNome()} devido à velocidade.")
                continue

            # Calcular probabilidade de aceitação
            candidato_avaliacao = grafo.calcula_heuristica(candidato, grafo.get_node_by_name(destino))
            atual_avaliacao = grafo.calcula_heuristica(atual, grafo.get_node_by_name(destino))
            diferenca = candidato_avaliacao - atual_avaliacao

            temperatura = temperatura_inicial / float(i + 1)
            probabilidade_aceitacao = np.exp(-diferenca / temperatura) if temperatura > 0 else 0

            # Imprimir o nó visitado
            print(f"Nó atual: {atual.getNome()}, Visitando nó candidato: {candidato.getNome()}")

            if diferenca < 0 or random.random() < probabilidade_aceitacao:
                print(f"[ACEITO] Movendo para {candidato.getNome()} com custo {custo_temporario}")
                atual = candidato
                caminho_atual.append(candidato.getNome())
                custo_atual = custo_temporario
                pessoas_socorridas = pessoas_socorridas_temp

            # Atualizar melhor caminho
            if custo_atual < melhor_custo and destino in caminho_atual:
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
                if grafo.transferir_valores(qtd, no_origem.getNome(), no.getNome()):
                    medicamentos_disponiveis -= qtd
        grafo.desenha()
        melhor_distancia = grafo.calcula_acumulado_arestas(caminho, veiculo)
        print(f"Melhor caminho: {caminho}")
        print(f"Veículo: {veiculo.get_tipo()}")
        print(f"Custo total: {custo}")
        print(f"Pessoas socorridas: {pessoas_socorridas}")
        print(f"Distância percorrida: {melhor_distancia}")
        print(f"Tempo de execução: {end_time - start_time:.6f} segundos")

        return (caminho, custo)

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
            distancia_atual = 5 if (no_origem.populacao == 0 or no_origem.janela_tempo == 0) else grafo.calcula_heuristica(no_origem, destino_node)
            
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
                        melhor_veiculo_global = veiculo
                        print(f"\nNovo melhor caminho encontrado!")
                        print(f"Caminho: {' -> '.join(caminho_atual)}")
                        print(f"Custo: {custo_final}")
                        
                        total_pessoas_socorridas = 0
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
                                    total_pessoas_socorridas += qtd
                        grafo.desenha()

                        melhor_pessoas_socorridas = total_pessoas_socorridas
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
                    dist = 5 if (vizinho_obj.populacao == 0 or vizinho_obj.janela_tempo == 0) else grafo.calcula_heuristica(vizinho_obj, destino_node)
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
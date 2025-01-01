import math
from queue import Queue
from collections import deque
import random

import numpy as np
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

        # Transferir valores apenas para o melhor caminho
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)

        capacidade_restante = veiculo.get_limite_carga() - pessoas_socorridas

        for no_intermediario in caminho[1:-1]:
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

def procura_BFS(grafo, inicio, fim):
    """
    Realiza a busca em largura (BFS) para encontrar o melhor caminho
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

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")

        # Transferir valores apenas para o melhor caminho
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)

        capacidade_restante = veiculo.get_limite_carga() - pessoas_socorridas

        for no_intermediario in caminho[1:-1]:
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


# Algoritmo A*
def procura_aStar(grafo, inicio, fim):
    """
    Implementa o algoritmo A* para encontrar o melhor caminho entre os nós 'inicio' e 'fim' no grafo.
    Utiliza:
      - Heurística (h) do grafo.m_h, como no algoritmo Greedy.
      - Custo acumulado das arestas (g).
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
        print(f"[ERRO] Nó '{inicio}' não possui veículos disponíveis.")
        return None

    melhores_caminhos = []

    for veiculo in veiculos_disponiveis:
        print(f"[INFO] Tentando com o veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()})")

        # Inicialização do A*
        open_list = {inicio}
        closed_list = set()
        g = {inicio: 0}
        parents = {inicio: None}

        while open_list:
            # Seleciona o nó com menor f(n) = g(n) + h(n)
            try:
                n = min(open_list, key=lambda v: g[v] + grafo.m_h.get(v, float('inf')))
            except ValueError:
                print(f"[ERRO] Não foi possível calcular f(n) para os nós na lista aberta.")
                break

            open_list.remove(n)
            closed_list.add(n)

            print(f"[DEBUG] Visitando nó: {n}, f(n): {g[n] + grafo.m_h.get(n, float('inf'))}")

            # Verifica se o destino foi alcançado
            if n == fim:
                caminho = []
                while parents[n] is not None:
                    caminho.append(n)
                    n = parents[n]
                caminho.append(inicio)
                caminho.reverse()

                custo_acumulado_arestas = grafo.calcula_acumulado_arestas(caminho, veiculo)
                if custo_acumulado_arestas == float('inf') or custo_acumulado_arestas > veiculo.get_combustivel_disponivel():
                    print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por falta de combustível: {caminho}.")
                    break  # Sai do loop para este veículo
                else:
                    destino = grafo.get_node_by_name(fim)
                    tempo_destino = destino.janela_tempo
                    if tempo_destino > 0 and (custo_acumulado_arestas / tempo_destino) > veiculo.get_velocidade():
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho por velocidade insuficiente: {caminho}.")
                        break  # Sai do loop para este veículo

                    custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)

                    if custo_final == float('inf'):
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho: {caminho}.")
                    else:
                        print(f"[DEBUG] Veículo: {veiculo.get_tipo()} PODE COMPLETAR o caminho: {caminho}. Custo final: {custo_final}")
                        melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas))
                break

            # Expande os vizinhos
            for m, peso in grafo.getNeighbours(n, veiculo.get_tipo()):
                if m in closed_list:
                    continue

                custo_possivel = g[n] + peso

                if m not in open_list or custo_possivel < g.get(m, float('inf')):
                    g[m] = custo_possivel
                    parents[m] = n

                    if m not in open_list:
                        open_list.add(m)

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordena pelo custo
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        print(f"[RESULTADO] Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")

        # Transfere valores para o melhor caminho
        grafo.transferir_valores(pessoas_socorridas, caminho[0], fim)

        capacidade_restante = veiculo.get_limite_carga() - pessoas_socorridas

        for no_intermediario in caminho[1:-1]:
            no_intermediario_obj = grafo.get_node_by_name(no_intermediario)
            if no_intermediario_obj.janela_tempo == 0:
                continue

            if capacidade_restante <= 0:
                break

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

    print("[ERRO] Nenhum caminho válido encontrado com A*.")
    return None

def greedy(grafo, inicio, destino):
    """
    Realiza a busca gulosa para encontrar o melhor caminho considerando todos os veículos disponíveis no nó inicial.
    Prioriza a transferência para o destino e, com os medicamentos restantes, socorre outros nós do caminho por prioridade.
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

    for veiculo in veiculos_disponiveis:
        print(f"Usando veículo: {veiculo.get_tipo()} (Velocidade: {veiculo.get_velocidade()})")

        # Inicializa o caminho atual e o nó de partida
        caminho = [inicio]
        nodo_atual = inicio
        visited = set()

        while nodo_atual != destino:
            visited.add(nodo_atual)
            print(f"Gulosa: Visitando {nodo_atual}, Caminho atual: {caminho}")

            # Obter vizinhos acessíveis
            vizinhos = [
                (adjacente, grafo.m_h[adjacente])
                for adjacente, peso, bloqueada, permitidos in grafo.m_graph[nodo_atual]
                if adjacente not in visited and veiculo.get_tipo() in permitidos and not bloqueada
            ]

            if not vizinhos:
                print(f"[ERRO] Sem vizinhos acessíveis para o nó {nodo_atual}.")
                break

            # Escolher o vizinho com menor heurística
            vizinho_escolhido = min(vizinhos, key=lambda x: x[1])[0]
            caminho.append(vizinho_escolhido)
            nodo_atual = vizinho_escolhido

        # Verificar se chegou ao destino
        if nodo_atual == destino:
            custo_final, pessoas_socorridas = grafo.calcula_custo(caminho, veiculo)
            if custo_final == float('inf'):
                print(f"[DEBUG] Veículo: {veiculo.get_tipo()} NÃO PODE COMPLETAR o caminho: {caminho}.")
            else:
                print(f"[DEBUG] Veículo: {veiculo.get_tipo()} PODE COMPLETAR o caminho: {caminho}. Custo final: {custo_final}")
                melhores_caminhos.append((veiculo, caminho, custo_final, pessoas_socorridas))

    if melhores_caminhos:
        melhor_caminho = min(melhores_caminhos, key=lambda x: x[2])  # Ordenar pelo custo
        veiculo, caminho, custo, pessoas_socorridas = melhor_caminho

        print(f"Melhor caminho: {caminho} com veículo {veiculo.get_tipo()} e custo {custo}")

        # Priorizar transferência para o destino
        capacidade_restante = veiculo.get_limite_carga()
        medicamentos_disponiveis = no_origem.get_medicamento()

        # Transferir medicamentos para o destino primeiro
        medicamentos_para_transferir = min(
            capacidade_restante,
            medicamentos_disponiveis,
            no_destino.populacao
        )
        if medicamentos_para_transferir > 0:
            grafo.transferir_valores(medicamentos_para_transferir, caminho[0], caminho[-1])
            medicamentos_disponiveis -= medicamentos_para_transferir
            capacidade_restante -= medicamentos_para_transferir

        # Transferir medicamentos para nós intermediários ordenados pela prioridade
        for no_intermediario in sorted(caminho[1:-1], key=lambda no: grafo.get_node_by_name(no).calcula_prioridade()):
            no_intermediario_obj = grafo.get_node_by_name(no_intermediario)

            if no_intermediario_obj.populacao > 0 and capacidade_restante > 0:
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

        # Atualizar heurísticas após transferir valores
        grafo.atualizar_heuristicas(no_destino)

        grafo.desenha()

        return {veiculo.get_tipo(): (caminho, custo)}

    print("Nenhum caminho válido encontrado.")
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
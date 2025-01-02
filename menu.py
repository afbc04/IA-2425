import os
import json
import time
import random
from grafo import Grafo
from no import No
import matplotlib.pyplot as plt
from veiculo import Veiculo
from meteorologia import Meteorologia
from condicoesDinamicas import executar_alteracoes_dinamicas
from algoritmos_procura import procura_DFS, procura_BFS, procura_Iterativa, procura_aStar, greedy, simulated_annealing, hill_climbing

def carregar_caracteristicas_veiculos(ficheiro_caracteristicas="data/caracteristicas_dos_veiculos.json"):
    """
    Carrega as características dos veículos (custo, limite de carga e combustível disponível) a partir de um ficheiro JSON.
    """
    try:
        with open(ficheiro_caracteristicas, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERRO] O ficheiro '{ficheiro_caracteristicas}' não foi encontrado.")
    except json.JSONDecodeError:
        print(f"[ERRO] O ficheiro '{ficheiro_caracteristicas}' contém JSON inválido.")
    return {}

def carregar_grafo(ficheiro_grafo="data/grafo2.json", ficheiro_caracteristicas="data/caracteristicas_dos_veiculos.json"):
    """
    Carrega o grafo e as características dos veículos a partir dos ficheiros JSON.
    """
    with open(ficheiro_grafo, "r") as f:
        dados = json.load(f)

    caracteristicas_veiculos = carregar_caracteristicas_veiculos(ficheiro_caracteristicas)

    grafo = Grafo(directed=False)

    for no_data in dados["nos"]:
        nome = no_data["nome"]
        populacao = no_data["populacao"]
        tempo = no_data["tempo"]
        x = no_data.get("x", 0)
        y = no_data.get("y", 0)
        medicamento = no_data.get("medicamento", 0)
        meteo_data = no_data.get("meteorologia", {"chuva": 0, "tempestade": 0, "vento": 0, "nevoeiro": 0})
        meteorologia = Meteorologia(
            chuva=meteo_data["chuva"],
            tempestade=meteo_data["tempestade"],
            vento=meteo_data["vento"],
            nevoeiro=meteo_data["nevoeiro"]
        )

        veiculos = []
        for tipo in no_data.get("veiculos", []):
            if tipo in caracteristicas_veiculos:
                veiculo_data = caracteristicas_veiculos[tipo]
                veiculo = Veiculo(
                    tipo=tipo,
                    custo=veiculo_data["custo"],
                    combustivel_disponivel=veiculo_data["combustivel_disponivel"],
                    limite_carga=veiculo_data["limite_carga"],
                    velocidade=veiculo_data["velocidade"]
                )
                veiculos.append(veiculo)
                # Adicionar veículo à lista global de veículos carregados
                if veiculo.get_tipo() not in grafo.veiculos_carregados:
                    grafo.veiculos_carregados.append(veiculo.get_tipo())
            else:
                print(f"[AVISO] O veículo '{tipo}' não tem características definidas no ficheiro '{ficheiro_caracteristicas}'.")

        no = No(nome, populacao=populacao, janela_tempo=tempo, medicamento=medicamento, veiculos=veiculos, x=x, y=y, meteorologia=meteorologia)
        grafo.m_nodes.append(no)
        grafo.m_graph[nome] = []

    for aresta in dados["arestas"]:
        grafo.add_edge(
            aresta["origem"], aresta["destino"],
            peso=aresta["peso"], blocked=aresta["bloqueada"],
            permitidos=aresta["permitidos"]
        )

    grafo.atualizar_medicamentos_e_populacao()

    return grafo

def listar_mapas_disponiveis(pasta="data"):
    """
    Lista os mapas disponíveis na pasta especificada, excluindo ficheiros que contenham 'caracteristicas' no nome.
    """
    try:
        arquivos = [
            f for f in os.listdir(pasta)
            if f.endswith(".json") and "caracteristicas" not in f.lower()
        ]
        if not arquivos:
            print(f"[ERRO] Nenhum mapa disponível na pasta '{pasta}'.")
            return []
        return arquivos
    except FileNotFoundError:
        print(f"[ERRO] Pasta '{pasta}' não encontrada.")
        return []

def selecionar_mapa():
    """
    Pergunta ao utilizador qual mapa deseja carregar, listando os disponíveis.
    """
    mapas = listar_mapas_disponiveis()
    if not mapas:
        return None  # Nenhum mapa disponível

    print("Mapas disponíveis:")
    for i, mapa in enumerate(mapas, start=1):
        print(f"{i}. {mapa}")

    while True:
        try:
            opcao = int(input("Selecione o número do mapa que deseja carregar: ").strip())
            if 1 <= opcao <= len(mapas):
                return f"data/{mapas[opcao - 1]}"
            else:
                print("[ERRO] Opção inválida. Escolha um número da lista.")
        except ValueError:
            print("[ERRO] Entrada inválida. Por favor, insira um número.")

def selecionar_tipo_experiencia():
    """
    Pergunta ao utilizador se deseja uma experiência estática ou dinâmica.
    """
    while True:
        print("\nSelecione o tipo de experiência:")
        print("1. Estática")
        print("2. Dinâmica")
        opcao = input("Opção: ").strip()

        if opcao == "1":
            return "estatica"
        elif opcao == "2":
            return "dinamica"
        else:
            print("[ERRO] Opção inválida. Por favor, escolha 1 ou 2.")

def mostrar_menu_estatico():
    """
    Mostra o menu estático e retorna a opção escolhida.
    """
    print("\nEscolha uma opção:")
    print("1. DFS (Depth-First Search)")
    print("2. BFS (Breadth-First Search)")
    print("3. Iterativo")
    print("4. A*")
    print("5. Greedy")
    print("6. Simulated Annealing")
    print("7. Hill-Climbing")
    print("8. Imprimir Grafo")
    print("0. Sair")
    return input("Opção: ").strip()

def mostrar_menu_dinamico():
    """
    Mostra o menu dinâmico e retorna a opção escolhida.
    """
    print("\nEscolha uma opção:")
    print("1. DFS (Depth-First Search)")
    print("2. BFS (Breadth-First Search)")
    print("3. Iterativo")
    print("4. A*")
    print("5. Greedy")
    print("6. Simulated Annealing")
    print("7. Hill-Climbing")
    print("8. Imprimir Grafo")
    print("9. Fabricar medicamentos")
    print("10. Executar alterações dinâmicas")
    print("0. Sair")
    return input("Opção: ").strip()

def iniciar_menu():
    ficheiro_mapa = selecionar_mapa()
    if not ficheiro_mapa:
        print("[ERRO] Nenhum mapa disponível. Encerrando o programa.")
        return

    tipo_experiencia = selecionar_tipo_experiencia()
    grafo = carregar_grafo(ficheiro_grafo=ficheiro_mapa)

    if not grafo.m_nodes:
        print("[ERRO] O grafo não possui nós. Verifique os ficheiros de entrada.")
        return

    while True:
        destino = grafo.get_no_maior_prioridade()
        if destino:
            print(f"\nDestino automaticamente escolhido: {destino.getNome()} (prioridade: {destino.calcula_prioridade()})")
        else:
            print("[INFO] Nenhum nó de maior prioridade disponível no momento.")

        # Selecionar o menu correto
        menu_func = mostrar_menu_estatico if tipo_experiencia == "estatica" else mostrar_menu_dinamico
        opcao = menu_func()

        # Processar opções do menu
        if opcao == "1":
            inicio = input("Nó inicial: ")
            veiculos_disponiveis = grafo.get_veiculos_no(inicio.upper())
            if not veiculos_disponiveis:
                print("O nó inicial não possui veículos disponíveis.")
                continue
            resultado = procura_DFS(grafo, inicio.upper(), destino.getNome().upper())
            if resultado:
                print("Caminho DFS:")
                for veiculo, (path, custo) in resultado.items():
                    print("Veículo:", veiculo, " -> ", path, " Custo:", custo)
            else:
                print("Caminho não encontrado com DFS.")

        elif opcao == "2":
            inicio = input("Nó inicial: ")
            resultado = procura_BFS(grafo, inicio.upper(), destino.getNome().upper())
            if resultado:
                print("Caminho BFS:")
                for veiculo, (path, custo) in resultado.items():
                    print("Veículo:", veiculo, " -> ", path, " Custo:", custo)
            else:
                print("Caminho não encontrado com BFS.")

        elif opcao == "3":
            inicio = input("Nó inicial: ")
            profundidade = int(input("Profundidade máxima: "))
            veiculos_disponiveis = grafo.get_veiculos_no(inicio.upper())
            if not veiculos_disponiveis:
                print("O nó inicial não possui veículos disponíveis.")
                continue
            resultado = procura_Iterativa(grafo, inicio.upper(), destino.getNome().upper(),profundidade)
            if resultado:
                print("Caminhos Iterativos:")
                for veiculo, (path, custo) in resultado.items():
                    print("Veículo:", veiculo, " -> ", path, " Custo:", custo)
            else:
                print("Caminho não encontrado com Iterativo.")
                
        elif opcao == "4":
            inicio = input("Nó inicial: ")
            resultado = procura_aStar(grafo, inicio.upper(), destino.getNome().upper())
            if resultado:
                for veiculo, (path, custo) in resultado.items():
                    print(f"Veículo: {veiculo}, Caminho: {path}, Custo: {custo}")
            else:
                print("Caminho não encontrado com A*.")

        elif opcao == "5":
            inicio = input("Nó inicial: ")
            resultado = greedy(grafo, inicio.upper(), destino.getNome().upper())
            if resultado:
                for veiculo, (path, custo) in resultado.items():
                    print(f"Veículo: {veiculo}, Caminho: {path}, Custo: {custo}")
            else:
                print("Caminho não encontrado com Greedy.")

        elif opcao == "6":
            resultado = simulated_annealing(grafo, destino.getNome().upper(), temperatura_inicial=10, numero_iteracoes=10)
            if resultado:
                print("Caminho:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com Simulated Annealing.")

        elif opcao == "7":
            resultado = hill_climbing(grafo, destino.getNome().upper(), max_restarts=6, max_iteracoes=10)
            if resultado:
                for veiculo, (path, custo) in resultado.items():
                    print(f"Veículo: {veiculo}, Caminho: {path}, Custo: {custo}")
            else:
                print("Caminho não encontrado com Hill-Climbing.")

        elif opcao == "8":
            grafo.desenha()
            plt.pause(0.01)

        elif opcao == "9" and tipo_experiencia == "dinamica":
            no = input("Indique o nó onde quer fabricar medicamentos: ").strip()
            quantidade = int(input("Indique a quantidade de medicamentos a fabricar: "))
            no_obj = grafo.get_node_by_name(no.upper())
            if no_obj:
                no_obj.incrementar_medicamentos(quantidade, grafo)
                print(f"Medicamentos fabricados com sucesso no nó {no}.")
                print("Janelas de tempo ajustadas para todos os nós com população > 0.")
            else:
                print(f"Nó {no} não encontrado.")

        elif opcao == "10":
            try:
                vezes = int(input("Quantas alterações dinâmicas deseja realizar? "))
                if vezes > 0:
                    executar_alteracoes_dinamicas(grafo, vezes)
                else:
                    print("[ERRO] O número deve ser maior que 0.")
            except ValueError:
                print("[ERRO] Entrada inválida. Por favor, insira um número inteiro.")

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("Opção inválida. Tente novamente.")
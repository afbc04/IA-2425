import os
import json
from grafo import Grafo
from no import No
from veiculo import Veiculo
from meteorologia import Meteorologia
from algoritmos_procura import procura_DFS, procura_BFS, procura_aStar, greedy, simulated_annealing, hill_climbing

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


def selecionar_mapa(pasta="data"):
    """
    Lista os ficheiros disponíveis na pasta e permite ao utilizador escolher um.
    """
    ficheiros = [f for f in os.listdir(pasta) if f.endswith(".json") and "caracteristicas" not in f]
    if not ficheiros:
        print(f"[ERRO] Nenhum ficheiro de mapa encontrado na pasta '{pasta}'.")
        return None

    print("\nMapas disponíveis:")
    for i, ficheiro in enumerate(ficheiros, 1):
        print(f"{i}. {ficheiro}")

    while True:
        escolha = input("Escolha o número do mapa a carregar: ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(ficheiros):
            return os.path.join(pasta, ficheiros[int(escolha) - 1])
        print("Opção inválida. Tente novamente.")


def carregar_grafo(ficheiro_grafo, ficheiro_caracteristicas="data/caracteristicas_dos_veiculos.json"):
    """
    Carrega o grafo e as características dos veículos a partir dos ficheiros JSON.
    """
    try:
        with open(ficheiro_grafo, "r") as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"[ERRO] O ficheiro '{ficheiro_grafo}' não foi encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"[ERRO] O ficheiro '{ficheiro_grafo}' contém JSON inválido.")
        return None

    caracteristicas_veiculos = carregar_caracteristicas_veiculos(ficheiro_caracteristicas)

    grafo = Grafo(directed=False)

    for no_data in dados["nos"]:
        nome = no_data["nome"].strip().upper()
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
                veiculos.append(Veiculo(
                    tipo=tipo,
                    custo=veiculo_data["custo"],
                    combustivel_disponivel=veiculo_data["combustivel_disponivel"],
                    limite_carga=veiculo_data["limite_carga"],
                    velocidade=veiculo_data["velocidade"]
                ))
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


def mostrar_menu():
    """
    Exibe o menu de opções para o utilizador.
    """
    print("\nEscolha uma opção:")
    print("1. DFS (Depth-First Search)")
    print("2. BFS (Breadth-First Search)")
    print("3. A*")
    print("4. Greedy")
    print("5. Simulated Annealing")
    print("6. Hill-Climbing")
    print("7. Imprimir Grafo")
    print("0. Sair")
    escolha = input("Opção: ")
    return escolha


def iniciar_menu():
    """
    Inicia o menu principal, permitindo a seleção do mapa e a execução dos algoritmos.
    """
    ficheiro_grafo = selecionar_mapa()
    if not ficheiro_grafo:
        print("[ERRO] Não foi possível selecionar um mapa.")
        return

    grafo = carregar_grafo(ficheiro_grafo)
    if not grafo:
        print("[ERRO] Não foi possível carregar o grafo.")
        return

    todos_com_populacao_zero = False

    while True:
        if all(no.populacao == 0 for no in grafo.m_nodes):
            if not todos_com_populacao_zero:
                print("Todos os nós têm população igual a 0. Nenhum algoritmo pode ser executado.")
                grafo.desenha(destaque_azul=True)
                todos_com_populacao_zero = True
            opcao = mostrar_menu()
            if opcao == "5":
                grafo.desenha()
            elif opcao == "0":
                print("A sair...")
                break
            else:
                print("Opção inválida. Não há operações disponíveis.")
            continue

        destino = grafo.get_no_maior_prioridade()
        if destino is None:
            print("Todos os nós foram processados. Escolha uma ação.")
            opcao = mostrar_menu()
            if opcao == "5":
                grafo.desenha()
            elif opcao == "0":
                print("A sair...")
                break
            else:
                print("Opção inválida. Tente novamente.")
            continue

        todos_com_populacao_zero = False
        print(f"\nDestino automaticamente escolhido: {destino.getName()} (prioridade: {destino.calcula_prioridade()})")
        opcao = mostrar_menu()

        if opcao == "1":
            inicio = input("Nó inicial: ")
            veiculos_disponiveis = grafo.get_veiculos_no(inicio.upper())
            if not veiculos_disponiveis:
                print("O nó inicial não possui veículos disponíveis.")
                continue
            resultado = procura_DFS(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                print("Caminho DFS:")
                for veiculo, (path, custo) in resultado.items():
                    print("Veículo:", veiculo, " -> ", path, " Custo:", custo)
            else:
                print("Caminho não encontrado com DFS.")

        elif opcao == "2":
            inicio = input("Nó inicial: ")
            resultado = procura_BFS(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                print("Caminho BFS:")
                for veiculo, (path, custo) in resultado.items():
                    print("Veículo:", veiculo, " -> ", path, " Custo:", custo)
            else:
                print("Caminho não encontrado com BFS.")

        elif opcao == "3":
            inicio = input("Nó inicial: ")
            resultado = procura_aStar(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                for veiculo, (caminho, custo) in resultado.items():
                    print(f"Veículo: {veiculo}, Caminho: {caminho}, Custo: {custo}")
            else:
                print("Caminho não encontrado com A*.")

        elif opcao == "4":
            inicio = input("Nó inicial: ")
            resultado = greedy(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                for veiculo, (path, custo) in resultado.items():
                    print(f"Veículo: {veiculo}, Caminho: {path}, Custo: {custo}")
            else:
                print("Caminho não encontrado com Greedy.")

        elif opcao == "5":
            resultado = simulated_annealing(grafo, destino.getName().upper(), temperatura_inicial=10, numero_iteracoes=10)
            if resultado:
                for veiculo, (caminho, custo) in resultado.items():
                    print(f"Veículo: {veiculo}, Caminho: {caminho}, Custo: {custo}")
            else:
                print("Caminho não encontrado com Simulated Annealing.")

        elif opcao == "6":
            veiculo, caminho, custo = hill_climbing(grafo, destino.getName().upper(), max_restarts=6, max_iteracoes=8)
            if caminho:
                print("Veículo:", veiculo, "\nCaminho:", caminho, "Custo:", custo)
            else:
                print("Caminho não encontrado com Hill-Climbing.")

        elif opcao == "7":
            grafo.desenha()

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("Opção inválida. Tente novamente.")

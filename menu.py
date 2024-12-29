import json
from grafo import Grafo
from no import No
from algoritmos_procura import procura_DFS, procura_BFS, procura_aStar, greedy
from meteorologia import Meteorologia
from condicoesDinamicas import CondicoesDinamicas

# Função para carregar o grafo a partir de um ficheiro JSON na pasta mapa
def carregar_grafo(ficheiro_json="mapa/grafo2.json"):
    """
    Carrega o grafo a partir de um ficheiro JSON.
    """
    with open(ficheiro_json, 'r') as f:
        dados = json.load(f)

    grafo = Grafo(directed=False)

    # Adicionar nós ao grafo
    for no_data in dados["nos"]:
        nome = no_data["nome"]
        populacao = no_data["populacao"]
        tempo = no_data["tempo"]
        x = no_data.get("x", 0)
        y = no_data.get("y", 0)
        meteo_data = no_data.get("meteorologia", {"chuva": 0, "tempestade": 0, "vento": 0, "nevoeiro": 0})
        meteorologia = Meteorologia(
            chuva=meteo_data["chuva"],
            tempestade=meteo_data["tempestade"],
            vento=meteo_data["vento"],
            nevoeiro=meteo_data["nevoeiro"]
        )
        veiculos = no_data.get("veiculos", [])
        no = No(name=nome, populacao=populacao, janela_tempo=tempo, meteorologia=meteorologia, x=x, y=y, veiculos=veiculos)
        grafo.m_nodes.append(no)
        grafo.m_graph[nome] = []

    # Adicionar arestas ao grafo
    for aresta in dados["arestas"]:
        origem = aresta["origem"]
        destino = aresta["destino"]
        peso = aresta["peso"]
        bloqueada = aresta.get("bloqueada", False)
        permitidos = aresta.get("permitidos", [])
        print(f"Processar aresta: {origem} -> {destino}, Peso: {peso}, Bloqueada: {bloqueada}, Permitidos: {permitidos}")
        grafo.add_edge(origem, destino, peso, blocked=bloqueada, permitidos=permitidos)

    return grafo

# Função para mostrar o menu e executar o algoritmo escolhido
def mostrar_menu():
    print("\nEscolha uma opção:")
    print("1. DFS (Depth-First Search)")
    print("2. BFS (Breadth-First Search)")
    print("3. A*")
    print("4. Greedy")
    print("5. Imprimir Grafo")
    print("0. Sair")
    escolha = input("Opção: ")
    return escolha

# Função principal do menu
def iniciar_menu():
    grafo = carregar_grafo()
    #condicoes_dinamicas = CondicoesDinamicas(grafo)
    #condicoes_dinamicas.iniciar_alteracoes()
    #TODO documentado, porque não compila, uma vez que não foram adicionados os veículos

    while True:
        destino = grafo.get_no_maior_prioridade()
        if destino is None:
            print("Não existem nós válidos no grafo.")
            break

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
                print("Caminho DFS:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com DFS.")

        elif opcao == "2":
            inicio = input("Nó inicial: ")
            resultado = procura_BFS(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                print("Caminho BFS:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com BFS.")

        elif opcao == "3":
            inicio = input("Nó inicial: ")
            resultado = procura_aStar(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                print("Caminho A*:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com A*.")

        elif opcao == "4":
            inicio = input("Nó inicial: ")
            resultado = greedy(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                print("Caminho Greedy:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com Greedy.")

        elif opcao == "5":
            grafo.desenha()

        elif opcao == "0":
            print("A sair...")
            break

        else:
            print("Opção inválida. Tente novamente.")



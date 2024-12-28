import json
from grafo import Grafo
from no import No 
from algoritmos_procura import procura_DFS, procura_BFS, procura_aStar, greedy
from meteorologia import Meteorologia

# Função para carregar o grafo a partir de um ficheiro JSON na pasta mapa
# def carregar_grafo2(ficheiro_json="mapa/mapaGrafo.json"):
#     with open(ficheiro_json, 'r') as f:
#         dados = json.load(f)

#     grafo = Grafo(directed=False)

#     # Adicionar nós ao grafo com população e tempo
#     for no_data in dados["nos"]:
#         nome = no_data["nome"]
#         populacao = no_data["populacao"]
#         tempo = no_data["tempo"]
#         no = No(nome, populacao=populacao, janela_tempo=tempo)
#         grafo.m_nodes.append(no)
#         grafo.m_graph[nome] = []  # Inicializa a lista de adjacências do nó

#     # Adicionar arestas ao grafo
#     for aresta in dados["arestas"]:
#         origem = aresta["origem"]
#         destino = aresta["destino"]
#         peso = aresta["peso"]
#         grafo.add_edge(origem, destino, peso)

#     return grafo


# Função para carregar o grafo a partir de um ficheiro JSON na pasta mapa
def carregar_grafo(ficheiro_json="mapa/grafo2.json"):
    with open(ficheiro_json, 'r') as f:
        dados = json.load(f)

    grafo = Grafo(directed=False)

    # Adicionar nós ao grafo
    for no_data in dados["nos"]:
        nome = no_data["nome"]
        populacao = no_data["populacao"]
        tempo = no_data["tempo"]
        meteo_data = no_data.get("meteorologia", {"chuva": 0, "tempestade": 0, "vento": 0, "nevoeiro": 0})
        meteorologia = Meteorologia(
            chuva=meteo_data["chuva"],
            tempestade=meteo_data["tempestade"],
            vento=meteo_data["vento"],
            nevoeiro=meteo_data["nevoeiro"]
        )
        no = No(name=nome, populacao=populacao, janela_tempo=tempo, meteorologia=meteorologia)
        grafo.m_nodes.append(no)
        grafo.m_graph[nome] = []  # Inicializa a lista de adjacências do nó

    # Adicionar arestas ao grafo
    for aresta in dados["arestas"]:
        origem = aresta["origem"]
        destino = aresta["destino"]
        peso = aresta["peso"]
        bloqueada = aresta.get("bloqueada", False)
        grafo.add_edge(origem, destino, peso, blocked=bloqueada)

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

    while True:
        # Encontrar o nó de maior prioridade
        destino = grafo.get_no_maior_prioridade()
        if destino is None:
            print("Não existem nós válidos no grafo.")
            break

        print(f"\nDestino automaticamente escolhido: {destino.getName()} (prioridade: {destino.calcula_prioridade()})")

        opcao = mostrar_menu()

        if opcao == "1":
            inicio = input("Nó inicial: ")
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

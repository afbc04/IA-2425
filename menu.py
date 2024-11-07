import json
from mapa.grafo import Grafo
from algoritmos_procura import procura_DFS, procura_BFS, procura_aStar, greedy

# Função para carregar o grafo a partir de um ficheiro JSON na pasta mapa
def carregar_grafo(ficheiro_json="mapa/grafos.json"):
    with open(ficheiro_json, 'r') as f:
        dados = json.load(f)

    grafo = Grafo(directed=False)
    for no in dados["nos"]:
        grafo.m_graph[no] = []  # Inicializa cada nó no grafo sem arestas

    for aresta in dados["arestas"]:
        origem = aresta["origem"]
        destino = aresta["destino"]
        peso = aresta["peso"]
        grafo.add_edge(origem, destino, peso)

    return grafo

# Função para mostrar o menu e executar o algoritmo escolhido
def mostrar_menu():
    print("Escolha uma opção:")
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
        opcao = mostrar_menu()
        if opcao == "1":
            inicio = input("Nó inicial: ")
            fim = input("Nó final: ")
            resultado = procura_DFS(grafo, inicio.upper(), fim.upper())
            if resultado:
                print("Caminho DFS:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com DFS")

        elif opcao == "2":
            inicio = input("Nó inicial: ")
            fim = input("Nó final: ")
            resultado = procura_BFS(grafo, inicio.upper(), fim.upper())
            if resultado:
                print("Caminho BFS:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com BFS")

        elif opcao == "3":
            inicio = input("Nó inicial: ")
            fim = input("Nó final: ")
            resultado = procura_aStar(grafo, inicio.upper(), fim.upper())
            if resultado:
                print("Caminho A*:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com A*")

        elif opcao == "4":
            inicio = input("Nó inicial: ")
            fim = input("Nó final: ")
            resultado = greedy(grafo, inicio.upper(), fim.upper())
            if resultado:
                print("Caminho Greedy:", resultado[0], "Custo:", resultado[1])
            else:
                print("Caminho não encontrado com Greedy")

        elif opcao == "5":
            grafo.desenha()  

        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("Opção inválida. Tente novamente.")

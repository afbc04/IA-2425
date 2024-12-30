import json
from grafo import Grafo
from no import No
from veiculo import Veiculo
from meteorologia import Meteorologia
from algoritmos_procura import procura_DFS, procura_BFS, procura_aStar, greedy

def carregar_custos_veiculos(ficheiro_custos="data/custos_veiculos.json"):
    """
    Carrega os custos dos veículos a partir de um ficheiro JSON.
    """
    with open(ficheiro_custos, "r") as f:
        return json.load(f)

def carregar_grafo(ficheiro_grafo="data/grafo2.json", ficheiro_custos="data/custos_veiculos.json"):
    """
    Carrega o grafo e os custos dos veículos a partir dos ficheiros JSON.
    """
    with open(ficheiro_grafo, "r") as f:
        dados = json.load(f)

    # Chamar a função carregar_custos_veiculos para obter os custos
    custos_veiculos = carregar_custos_veiculos(ficheiro_custos)

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

        veiculos_data = no_data.get("veiculos", [])
        veiculos = []
        for veiculo_info in veiculos_data:
            tipo = veiculo_info["tipo"]
            combustivel_disponivel = veiculo_info["combustivel_disponivel"]
            custo = custos_veiculos.get(tipo, 1)  # Define um custo padrão caso não esteja no ficheiro
            veiculo = Veiculo(tipo=tipo, custo=custo, combustivel_disponivel=combustivel_disponivel)
            veiculos.append(veiculo)

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

                print("Caminho DFS:")

                for veiculo, (path,custo) in resultado.items():
                    print("veículo:",veiculo," -> ", path, " Custo:", custo)

            else:
                print("Caminho não encontrado com DFS.")

        elif opcao == "2":
            inicio = input("Nó inicial: ")
            resultado = procura_BFS(grafo, inicio.upper(), destino.getName().upper())
            if resultado:
                
                print("Caminho BFS:")

                for veiculo, (path,custo) in resultado.items():
                    print("veículo:",veiculo," -> ", path, " Custo:", custo)

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



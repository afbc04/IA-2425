import random
from meteorologia import Meteorologia
from threading import Timer
from matplotlib import pyplot as plt

class CondicoesDinamicas:
    
    def __init__(self, grafo):
        self.grafo = grafo
        self.running = True
    

    def iniciar_alteracoes(self):
        self.running = True
        self.agendar_alteracao()
        print("\n[DEBUG][INFO] Sistema de alterações dinâmicas iniciado.")
    

    def parar_alteracoes(self):
        self.running = False
        print("\n[DEBUG][INFO] Sistema de alterações dinâmicas parado.")
    
    def agendar_alteracao(self):
        if self.running:
            self.escolhe_condicao_a_alterar()
            #Agenda alterações a cada 20 segundos
            Timer(20, self.agendar_alteracao).start()
    

    #define se vai alterar uma condição meteorológica ou o estado de um caminho
    def escolhe_condicao_a_alterar(self):
        rand = random.random()
        if rand < 0.50 and self.grafo.m_nodes:
            self.alterar_meteo_no()
        elif rand < 0.80:
            self.prod_medicamentos()
        else:
            self.alterar_estado_caminho()
        print("[DEBUG] Pressione \"8\" para atualizar o grafo")
        
        print("\n" + "-" * 50)  # Add separator line
        destino = self.grafo.get_no_maior_prioridade()
        if destino:
            print(f"\nDestino automaticamente escolhido: {destino.getNome()} (prioridade: {destino.calcula_prioridade()})")
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
        print("Opção: ", end = '', flush=True)
    

    def alterar_meteo_no(self):
        #escolhe nó no qual vai alterar condição
        no_a_alterar = random.choice(self.grafo.m_nodes)
 
        #escolhe a condição a alterar e o seu novo valor
        lista_cond_meteo = ["chuva", "tempestade", "vento", "nevoeiro"]
        cond_a_alterar = random.choices(lista_cond_meteo, [0.3, 0.1, 0.3, 0.3], k=1)[0]
        #if cond_a_alterar == "tempestade"
        novo_valor_cond = random.random()

        setattr(no_a_alterar.meteorologia, cond_a_alterar, novo_valor_cond)
        self.grafo.ajustar_janelas_de_tempo()
        print(f"\n[DEBUG]Meteorologia alterada em: {no_a_alterar.getNome()}\nCondição: {cond_a_alterar}\nNovo valor: {novo_valor_cond}")
        #print("[DEBUG] Pressione \"8\" para atualizar o grafo")


    def prod_medicamentos(self):
        no_prod = random.choice(self.grafo.m_nodes)
        quant = random.randint(1,300)
        no_prod.incrementar_medicamentos(quant, self.grafo)
        #print("[DEBUG] Pressione \"8\" para atualizar o grafo")

    
    def alterar_estado_caminho(self):
        #escolhe um nó de origem aleatório
        no_origem = random.choice(self.grafo.m_nodes)
        no_destino = None
        bloqueada = None
        #procura os nós adjacentes ao nó de origem
        adjacentes = self.grafo.m_graph[no_origem.getNome()]
        if adjacentes:
            #escolhe aleatoriamente um nó adjacente ao nó origem
            no_destino, _, bloqueada, _ = random.choice(adjacentes)
            novo_estado = not bloqueada
    
            self.update_estado_caminho(no_origem.getNome(), no_destino, novo_estado)
            self.grafo.ajustar_janelas_de_tempo()
            print(f"\n[DEBUG][ALTERAÇÃO] Estado do caminho alterado:")
            print(f"[DEBUG] Origem: {no_origem.getNome()}")
            print(f"[DEBUG] Destino: {no_destino}")
            print(f"[DEBUG] Novo estado: {'Bloqueado' if novo_estado else 'Desbloqueado'}")
            #print("[DEBUG] Pressione \"8\" para atualizar o grafo")
    
    
    def update_estado_caminho(self, nome_no_origem, nome_no_destino, novo_estado):
        
        #atualiza estado no caminho
        def atualizar(nome_no, nome_adjacente):
            lista = []
            for adj, peso, estado, permit in self.grafo.m_graph[nome_no]:
                if adj == nome_adjacente:
                    lista.append((adj, peso, novo_estado, permit))
                else:
                    lista.append((adj, peso, estado, permit))
            self.grafo.m_graph[nome_no] = lista
        
        atualizar(nome_no_origem, nome_no_destino)
        if not self.grafo.m_directed:
            atualizar(nome_no_destino, nome_no_origem)
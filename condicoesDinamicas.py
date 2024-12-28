import random
import time
from meteorologia import Meteorologia
from threading import Thread

class CondicoesDinamicas:
    def __init__(self, grafo):
        self.grafo = grafo
    

    def iniciar_alteracoes(self):
        def loop_alteracoes():
            while True:
                self.escolhe_condicao_a_alterar()
                time.sleep(20)
        
        thread_alteracoes_dinam = Thread(target=loop_alteracoes, daemon=True)
        thread_alteracoes_dinam.start()


    #define se vai alterar uma condição meteorológica ou o estado de um caminho
    def escolhe_condicao_a_alterar(self):
        if random.random() > 0.10 and self.grafo.m_nodes:
            self.alterar_meteo_no()
        else:
            self.alterar_estado_caminho()

    
    def alterar_meteo_no(self):
        #escolhe nó no qual vai alterar condição
        no_a_alterar = random.choice(self.grafo.m_nodes)
 
        #escolhe a condição a alterar e o seu novo valor
        lista_cond_meteo = ["chuva", "tempestade", "vento", "nevoeiro"]
        cond_a_alterar = random.choices(lista_cond_meteo, [0.3, 0.1, 0.3, 0.3], k=1)[0]

        #if cond_a_alterar == "tempestade"
        novo_valor_cond = random.random()

        setattr(no_a_alterar.meteorologia, cond_a_alterar, novo_valor_cond)
        #print("\nMeteorologia alterada: " + no_a_alterar.getName() + "\nCondição: " + cond_a_alterar + "\nNovo valor: " + str(novo_valor_cond))

    
    def alterar_estado_caminho(self):
        #escolhe um nó de origem aleatório
        no_origem = random.choice(self.grafo.m_nodes)
        no_destino = None
        peso = None
        bloqueada = None

        #procura os nós adjacentes ao nó de origem
        adjacentes = self.grafo.m_graph[no_origem.m_name]
        if adjacentes:
            #escolhe aleatoriamente um nó adjacente ao nó origem
            no_destino, peso, bloqueada = random.choice(adjacentes)
            self.update_estado_caminho(no_origem.m_name, no_destino, peso, not bloqueada)


    def update_estado_caminho(self, nome_no_origem, nome_no_destino, peso, novo_estado):
        
        #atualiza estado no caminho
        def atualizar(nome_no, nome_adjacente):
            lista = []
            for adj, peso, estado in self.grafo.m_graph[nome_no]:
                if adj == nome_adjacente:
                    lista.append((adj, peso, novo_estado))
                else:
                    lista.append((adj, peso, estado))
            self.grafo.m_graph[nome_no] = lista

        atualizar(nome_no_origem, nome_no_destino)
        if not self.grafo.m_directed:
            atualizar(nome_no_destino, nome_no_origem)
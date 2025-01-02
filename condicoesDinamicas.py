import random
import time
from grafo import Grafo

def alterar_dinamicamente(grafo, queue):
    """
    Realiza alterações dinâmicas no grafo e coloca mensagens na fila.
    Utiliza veículos da lista global `grafo.veiculos_carregados`.
    """
    alteracao = random.choice(["estrada", "veiculo", "populacao"])
    mensagem = ""

    if alteracao == "estrada":
        no = random.choice(grafo.m_nodes)
        if grafo.m_graph[no.getNome()]:
            vizinho = random.choice(grafo.m_graph[no.getNome()])
            nome_vizinho = vizinho[0]
            bloqueada = vizinho[2]
            nova_estrada = (vizinho[0], vizinho[1], not bloqueada, vizinho[3])
            grafo.m_graph[no.getNome()] = [
                nova_estrada if v[0] == nome_vizinho else v
                for v in grafo.m_graph[no.getNome()]
            ]
            mensagem = (
                f"[DINÂMICO] A estrada entre {no.getNome()} e {nome_vizinho} "
                f"ficou {'bloqueada' if not bloqueada else 'livre'}."
            )

    elif alteracao == "veiculo":
        no = random.choice(grafo.m_nodes)
        if grafo.m_graph[no.getNome()]:
            vizinho = random.choice(grafo.m_graph[no.getNome()])
            nome_vizinho = vizinho[0]
            veiculos = vizinho[3]  # Veículos associados à aresta como strings

            if random.choice([True, False]):  # Decidir se vai adicionar ou remover
                # Adicionar um veículo da lista global
                veiculo_adicionado = random.choice(grafo.veiculos_carregados)
                veiculos.append(veiculo_adicionado)
                mensagem = f"[DINÂMICO] Veículo '{veiculo_adicionado}' adicionado à estrada entre {no.getNome()} e {nome_vizinho}."
            else:
                # Remover um veículo, se existir algum
                if veiculos:
                    veiculo_removido = veiculos.pop(random.randint(0, len(veiculos) - 1))
                    mensagem = f"[DINÂMICO] Veículo '{veiculo_removido}' removido da estrada entre {no.getNome()} e {nome_vizinho}."
                else:
                    mensagem = f"[DINÂMICO] Nenhum veículo para remover na estrada entre {no.getNome()} e {nome_vizinho}."

    elif alteracao == "populacao":
        no = random.choice(grafo.m_nodes)
        alteracao_pop = random.randint(-10, 50)
        nova_populacao = max(0, no.populacao + alteracao_pop)
        mensagem = (
            f"[DINÂMICO] População do nó {no.getNome()} alterada de {no.populacao} para {nova_populacao}."
        )
        no.populacao = nova_populacao

    if mensagem:
        queue.append(mensagem)

def executar_alteracoes_dinamicas(grafo, vezes):
    """
    Executa alterações dinâmicas no grafo um número de vezes especificado pelo utilizador.
    """
    queue = []
    for _ in range(vezes):
        alterar_dinamicamente(grafo, queue)
        time.sleep(1)

    print("\n[RESULTADO] Alterações dinâmicas realizadas:")
    for mensagem in queue:
        print(mensagem)

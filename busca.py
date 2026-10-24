# Minimax puro e Minimax com poda Alfa-Beta.
# A IA usa o Alfa-Beta; o Minimax puro fica como referência.

import math

from heuristica import avaliar
from regras import fim_de_jogo, utilidade
from tabuleiro import MAX, MIN, colunas_validas, jogar, outro_jogador


# Conta os estados visitados pela busca.
class Contador:
    def __init__(self):
        self.estados = 0


# Valor de um estado final. A profundidade restante entra na conta
# para preferir vitórias rápidas e adiar derrotas.
def valor_terminal(tabuleiro, profundidade):
    valor = utilidade(tabuleiro)
    if valor > 0:
        return valor + profundidade
    if valor < 0:
        return valor - profundidade
    return 0


# Valor do estado supondo que os dois jogadores jogam o melhor possível.
def minimax(tabuleiro, profundidade, jogador, contador):
    contador.estados += 1

    if fim_de_jogo(tabuleiro):
        return valor_terminal(tabuleiro, profundidade)

    # limite de profundidade: usa a heurística
    if profundidade == 0:
        return avaliar(tabuleiro)

    proximo = outro_jogador(jogador)

    if jogador == MAX:
        melhor = -math.inf
        for coluna in colunas_validas(tabuleiro):
            filho = jogar(tabuleiro, coluna, jogador)
            valor = minimax(filho, profundidade - 1, proximo, contador)
            melhor = max(melhor, valor)
        return melhor

    else:
        melhor = math.inf
        for coluna in colunas_validas(tabuleiro):
            filho = jogar(tabuleiro, coluna, jogador)
            valor = minimax(filho, profundidade - 1, proximo, contador)
            melhor = min(melhor, valor)
        return melhor


# Minimax com poda. alfa e beta são os melhores valores já garantidos
# para MAX e MIN; quando alfa >= beta o resto dos filhos é ignorado.
def alfa_beta(tabuleiro, profundidade, alfa, beta, jogador, contador):
    contador.estados += 1

    if fim_de_jogo(tabuleiro):
        return valor_terminal(tabuleiro, profundidade)

    if profundidade == 0:
        return avaliar(tabuleiro)

    proximo = outro_jogador(jogador)

    if jogador == MAX:
        melhor = -math.inf
        for coluna in colunas_validas(tabuleiro):
            filho = jogar(tabuleiro, coluna, jogador)
            valor = alfa_beta(filho, profundidade - 1, alfa, beta, proximo, contador)
            melhor = max(melhor, valor)

            alfa = max(alfa, melhor)
            if alfa >= beta:
                break  # MIN já tem opção melhor em outro ramo

        return melhor

    else:
        melhor = math.inf
        for coluna in colunas_validas(tabuleiro):
            filho = jogar(tabuleiro, coluna, jogador)
            valor = alfa_beta(filho, profundidade - 1, alfa, beta, proximo, contador)
            melhor = min(melhor, valor)

            beta = min(beta, melhor)
            if alfa >= beta:
                break  # MAX já tem opção melhor em outro ramo

        return melhor


# Testa cada coluna e devolve (melhor_coluna, valor_estimado).
def escolher_melhor_coluna(tabuleiro, jogador, profundidade, usar_poda, contador):
    proximo = outro_jogador(jogador)
    melhor_coluna = None

    if jogador == MAX:
        melhor_valor = -math.inf
    else:
        melhor_valor = math.inf

    alfa = -math.inf
    beta = math.inf

    for coluna in colunas_validas(tabuleiro):
        filho = jogar(tabuleiro, coluna, jogador)

        if usar_poda:
            valor = alfa_beta(filho, profundidade - 1, alfa, beta, proximo, contador)
        else:
            valor = minimax(filho, profundidade - 1, proximo, contador)

        if jogador == MAX and valor > melhor_valor:
            melhor_valor = valor
            melhor_coluna = coluna
        elif jogador == MIN and valor < melhor_valor:
            melhor_valor = valor
            melhor_coluna = coluna

        # atualizar a janela na raiz poda mais cedo as próximas colunas
        if usar_poda:
            if jogador == MAX:
                alfa = max(alfa, melhor_valor)
            else:
                beta = min(beta, melhor_valor)

    return melhor_coluna, melhor_valor

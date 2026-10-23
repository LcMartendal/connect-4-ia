"""Algoritmos de busca competitiva: Minimax e Minimax com poda Alfa-Beta.

Os dois algoritmos estão escritos separados de propósito, para que seja
possível ler um e depois o outro e enxergar exatamente o que a poda acrescenta.

Ideia geral do Minimax:
- MAX escolhe a jogada que leva ao MAIOR valor.
- MIN escolhe a jogada que leva ao MENOR valor.
- O valor de um estado é calculado olhando os estados seguintes, recursivamente,
  até chegar em um estado terminal (utilidade) ou no limite de profundidade
  (heurística).

Ideia da poda Alfa-Beta:
- alfa = o melhor valor que MAX já tem garantido no caminho até aqui.
- beta = o melhor valor que MIN já tem garantido no caminho até aqui.
- Se em algum momento alfa >= beta, o resto dos filhos daquele nó não precisa
  ser explorado: o adversário nunca deixaria o jogo chegar ali.
"""

import math

from heuristica import avaliar
from regras import fim_de_jogo, utilidade
from tabuleiro import MAX, MIN, colunas_validas, jogar, outro_jogador


class Contador:
    """Guarda quantos estados (nós da árvore) a busca visitou.

    Serve para comparar o custo do Minimax puro com o do Alfa-Beta.
    """

    def __init__(self):
        self.estados = 0


def valor_terminal(tabuleiro, profundidade):
    """Valor de um estado em que o jogo acabou.

    Somamos a profundidade restante ao resultado para que a busca prefira
    vitórias mais rápidas e, quando for perder, derrotas mais demoradas
    (dando mais chances de o adversário errar).
    """
    valor = utilidade(tabuleiro)
    if valor > 0:
        return valor + profundidade
    if valor < 0:
        return valor - profundidade
    return 0


# ---------------------------------------------------------------------------
# Minimax puro
# ---------------------------------------------------------------------------

def minimax(tabuleiro, profundidade, jogador, contador):
    """Retorna o valor do estado supondo que os dois jogam da melhor forma.

    profundidade: quantas jogadas ainda podem ser exploradas a partir daqui.
    jogador:      quem vai jogar neste estado.
    """
    contador.estados += 1

    # Caso base 1: o jogo acabou.
    if fim_de_jogo(tabuleiro):
        return valor_terminal(tabuleiro, profundidade)

    # Caso base 2: chegou no limite da busca, usa a heurística.
    if profundidade == 0:
        return avaliar(tabuleiro)

    proximo = outro_jogador(jogador)

    if jogador == MAX:
        melhor = -math.inf  # MAX começa com o pior valor possível para ele
        for coluna in colunas_validas(tabuleiro):
            filho = jogar(tabuleiro, coluna, jogador)
            valor = minimax(filho, profundidade - 1, proximo, contador)
            melhor = max(melhor, valor)
        return melhor

    else:  # jogador == MIN
        melhor = math.inf  # MIN começa com o pior valor possível para ele
        for coluna in colunas_validas(tabuleiro):
            filho = jogar(tabuleiro, coluna, jogador)
            valor = minimax(filho, profundidade - 1, proximo, contador)
            melhor = min(melhor, valor)
        return melhor


# ---------------------------------------------------------------------------
# Minimax com poda Alfa-Beta
# ---------------------------------------------------------------------------

def alfa_beta(tabuleiro, profundidade, alfa, beta, jogador, contador):
    """Igual ao minimax, mas corta ramos que não podem mudar a decisão.

    alfa: melhor valor já garantido para MAX no caminho até aqui.
    beta: melhor valor já garantido para MIN no caminho até aqui.
    """
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

            # --- A poda começa aqui ---
            alfa = max(alfa, melhor)
            if alfa >= beta:
                # MIN (acima de nós) já tem uma opção melhor que beta.
                # Ele nunca deixaria o jogo chegar aqui, então paramos.
                break
        return melhor

    else:  # jogador == MIN
        melhor = math.inf
        for coluna in colunas_validas(tabuleiro):
            filho = jogar(tabuleiro, coluna, jogador)
            valor = alfa_beta(filho, profundidade - 1, alfa, beta, proximo, contador)
            melhor = min(melhor, valor)

            # --- A poda começa aqui ---
            beta = min(beta, melhor)
            if alfa >= beta:
                # MAX (acima de nós) já tem uma opção melhor que alfa.
                # Ele nunca deixaria o jogo chegar aqui, então paramos.
                break
        return melhor


# ---------------------------------------------------------------------------
# Raiz da busca: escolher a jogada
# ---------------------------------------------------------------------------

def escolher_melhor_coluna(tabuleiro, jogador, profundidade, usar_poda, contador):
    """Testa cada coluna possível e devolve (melhor_coluna, valor_estimado).

    A raiz é parecida com o corpo do minimax, mas em vez de guardar só o
    melhor VALOR ela precisa lembrar qual COLUNA gerou esse valor.
    """
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

        # Com poda, a raiz também vai apertando a janela [alfa, beta]
        # para que as próximas colunas sejam podadas mais cedo.
        if usar_poda:
            if jogador == MAX:
                alfa = max(alfa, melhor_valor)
            else:
                beta = min(beta, melhor_valor)

    return melhor_coluna, melhor_valor

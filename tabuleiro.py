"""Representação do tabuleiro do Lig 4.

O tabuleiro é uma matriz (lista de listas) com 6 linhas e 7 colunas.
A linha 0 é a de CIMA e a linha 5 é a de BAIXO, onde as peças "caem".
Cada casa guarda um de três valores: VAZIO, MAX ou MIN.

Exemplo de tabuleiro (a peça X caiu na coluna 3, índice 3):

    linha 0:  . . . . . . .
    linha 1:  . . . . . . .
    linha 2:  . . . . . . .
    linha 3:  . . . . . . .
    linha 4:  . . . . . . .
    linha 5:  . . . X . . .
              0 1 2 3 4 5 6   <- índice da coluna

Este módulo só sabe guardar e modificar o tabuleiro. As regras do jogo
(quem venceu, quando acaba) ficam em regras.py.
"""

LINHAS = 6
COLUNAS = 7

# Valores possíveis de uma casa.
VAZIO = 0
MAX = 1  # jogador "X", que começa a partida
MIN = 2  # jogador "O"

# Como cada valor aparece na tela.
SIMBOLOS = {VAZIO: ".", MAX: "X", MIN: "O"}


def criar_tabuleiro():
    """Estado inicial do jogo: todas as casas vazias."""
    tabuleiro = []
    for _ in range(LINHAS):
        linha = [VAZIO] * COLUNAS  # uma linha com 7 casas vazias
        tabuleiro.append(linha)
    return tabuleiro


def copiar_tabuleiro(tabuleiro):
    """Cria uma cópia independente do tabuleiro.

    É preciso copiar linha por linha: copiar só a lista de fora faria as
    duas versões compartilharem as mesmas linhas, e mudar uma mudaria a outra.
    """
    copia = []
    for linha in tabuleiro:
        copia.append(linha[:])  # linha[:] é uma cópia da lista
    return copia


def outro_jogador(jogador):
    """Quem joga depois do jogador informado."""
    if jogador == MAX:
        return MIN
    return MAX


def colunas_validas(tabuleiro):
    """Ações possíveis: colunas onde ainda cabe uma peça.

    Uma coluna ainda tem espaço se a casa de cima (linha 0) está vazia.
    """
    validas = []
    for coluna in range(COLUNAS):
        if tabuleiro[0][coluna] == VAZIO:
            validas.append(coluna)
    return validas


def jogar(tabuleiro, coluna, jogador):
    """Função de transição: devolve um NOVO tabuleiro com a peça solta na coluna.

    O tabuleiro recebido não é alterado. Isso é essencial para a busca
    Minimax, que precisa "imaginar" várias jogadas a partir do mesmo estado
    sem bagunçar o jogo de verdade.
    """
    if coluna not in colunas_validas(tabuleiro):
        raise ValueError(f"Jogada inválida: coluna {coluna} cheia ou inexistente.")

    novo = copiar_tabuleiro(tabuleiro)

    # A peça cai: percorre a coluna de baixo (linha 5) para cima (linha 0)
    # e para na primeira casa vazia que encontrar.
    for linha in range(LINHAS - 1, -1, -1):
        if novo[linha][coluna] == VAZIO:
            novo[linha][coluna] = jogador
            break

    return novo


def imprimir_tabuleiro(tabuleiro):
    """Mostra o tabuleiro na tela, com as colunas numeradas de 1 a 7."""
    print()
    for linha in tabuleiro:
        simbolos = [SIMBOLOS[casa] for casa in linha]
        print("| " + " ".join(simbolos) + " |")
    print("+" + "-" * (COLUNAS * 2 + 1) + "+")
    numeros = [str(coluna + 1) for coluna in range(COLUNAS)]
    print("  " + " ".join(numeros))
    print()

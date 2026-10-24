# Tabuleiro 6x7 como lista de listas, com a linha 0 no topo.
# Cada casa vale VAZIO, MAX ou MIN.

LINHAS = 6
COLUNAS = 7

VAZIO = 0
MAX = 1  # X, começa a partida
MIN = 2  # O

SIMBOLOS = {VAZIO: ".", MAX: "X", MIN: "O"}


def criar_tabuleiro():
    tabuleiro = []
    for _ in range(LINHAS):
        linha = [VAZIO] * COLUNAS
        tabuleiro.append(linha)
    return tabuleiro


# Copia linha por linha para as listas internas não serem compartilhadas.
def copiar_tabuleiro(tabuleiro):
    copia = []
    for linha in tabuleiro:
        copia.append(linha[:])
    return copia


def outro_jogador(jogador):
    if jogador == MAX:
        return MIN
    return MAX


# Colunas com a casa do topo ainda vazia.
def colunas_validas(tabuleiro):
    validas = []
    for coluna in range(COLUNAS):
        if tabuleiro[0][coluna] == VAZIO:
            validas.append(coluna)
    return validas


# Devolve um novo tabuleiro com a peça na coluna; o original não muda.
def jogar(tabuleiro, coluna, jogador):
    if coluna not in colunas_validas(tabuleiro):
        raise ValueError(f"Jogada inválida: coluna {coluna} cheia ou inexistente.")

    novo = copiar_tabuleiro(tabuleiro)

    # a peça cai até a primeira casa vazia de baixo para cima
    for linha in range(LINHAS - 1, -1, -1):
        if novo[linha][coluna] == VAZIO:
            novo[linha][coluna] = jogador
            break

    return novo


def imprimir_tabuleiro(tabuleiro):
    print()
    for linha in tabuleiro:
        simbolos = [SIMBOLOS[casa] for casa in linha]
        print("| " + " ".join(simbolos) + " |")
    print("+" + "-" * (COLUNAS * 2 + 1) + "+")
    numeros = [str(coluna + 1) for coluna in range(COLUNAS)]
    print("  " + " ".join(numeros))
    print()
